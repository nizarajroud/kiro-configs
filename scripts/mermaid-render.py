#!/usr/bin/env python3
"""Rend du code Mermaid via l'API api.mermaid.ai et range le fichier au bon endroit.

Usage typique (l'agent ecrit le code Mermaid lui-meme, puis appelle ce script) :

    mermaid-render.py --name flux-login --domain work --subject gnl --file /chemin/code.mmd
    cat code.mmd | mermaid-render.py --name flux-login --domain work --subject gnl

Sortie (stdout), une valeur par ligne :
    ARTIFACT=<chemin absolu a referencer dans la reponse de l'agent>
    ARCHIVE=<copie d'archivage dans AI-GENERATED>
    CREDITS_REMAINING=<n>

Codes de sortie :
    0 OK | 2 usage / entree invalide | 3 quota bas (demander a l'utilisateur, voir --force)
    4 code Mermaid invalide (corriger le code, ne pas reessayer tel quel)
    5 cle API refusee | 6 erreur reseau/serveur

Pieges deja rencontres (voir skills/mermaid-diagrams/SKILL.md) :
    - l'API est derriere une redirection CloudFront : urllib perd le header Authorization
      (401 ERR_KEY_MISSING). On utilise donc curl -L.
    - burst limite a 20 requetes / 60 s : espacement + retry sur 429.
    - la cle ne doit jamais apparaitre dans la ligne de commande (ps) : header via fichier 0600.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

API = "https://api.mermaid.ai/v1"
ROOT = Path(__file__).resolve().parent.parent
AI_GENERATED = Path("/mnt/c/Users/nizar/Documents/AI-GENERATED")
LOG_DIR = ROOT / "logs"
USAGE_LOG = LOG_DIR / "mermaid-usage.jsonl"
LAST_CALL = LOG_DIR / ".mermaid-last-call"
MIN_SPACING_S = 3.2  # 20 req / 60 s => une requete toutes les 3 s au maximum
MONTHS_FR = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet",
             "aout", "septembre", "octobre", "novembre", "decembre"]
OPENABLE = {"svg", "png", "pdf"}
EXIT_OK, EXIT_USAGE, EXIT_QUOTA, EXIT_INVALID, EXIT_KEY, EXIT_NET = 0, 2, 3, 4, 5, 6


def die(code, msg):
    print(msg, file=sys.stderr)
    sys.exit(code)


def load_key():
    """Cle depuis l'environnement, sinon depuis kiro-configs/.env (lignes `export X=...`)."""
    key = os.environ.get("MERMAID_API_KEY", "").strip()
    if key:
        return key
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            m = re.match(r"\s*(?:export\s+)?MERMAID_API_KEY\s*=\s*(.+?)\s*$", line)
            if m:
                return m.group(1).strip("'\"")
    die(EXIT_KEY, "MERMAID_API_KEY introuvable (ni dans l'environnement ni dans kiro-configs/.env)")


def in_kiro_web():
    """KIRO_WEB=1 (methode fiable), sinon un ancetre de process contient 'kiro_web'."""
    if os.environ.get("KIRO_WEB") == "1":
        return True
    pid = os.getpid()
    for _ in range(10):
        try:
            stat = Path(f"/proc/{pid}/stat").read_text()
            ppid = int(stat.rsplit(")", 1)[1].split()[1])
            if ppid <= 1:
                return False
            if b"kiro_web" in Path(f"/proc/{ppid}/cmdline").read_bytes():
                return True
            pid = ppid
        except (OSError, ValueError, IndexError):
            return False
    return False


def throttle():
    """Espace les appels entre invocations (plusieurs agents peuvent appeler en parallele)."""
    LOG_DIR.mkdir(exist_ok=True)
    try:
        wait = MIN_SPACING_S - (time.time() - float(LAST_CALL.read_text()))
    except (OSError, ValueError):
        wait = 0
    if wait > 0:
        time.sleep(wait)
    LAST_CALL.write_text(str(time.time()))


def call(key, method, path, body=None, want_headers=False, accept=None):
    """Appel curl -L. Retourne (http_code, headers_dict, bytes). Retry sur 429."""
    with tempfile.TemporaryDirectory() as tmp:
        hdr_cfg = Path(tmp) / "auth.hdr"
        hdr_cfg.write_text(f"Authorization: Bearer {key}\n")
        hdr_cfg.chmod(0o600)
        out_file, dump_file = Path(tmp) / "out.bin", Path(tmp) / "headers.txt"
        cmd = ["curl", "-sS", "-L", "-X", method, f"{API}{path}", "-H", f"@{hdr_cfg}",
               "-D", str(dump_file), "-o", str(out_file), "-w", "%{http_code}",
               "--max-time", "90"]
        if accept:
            cmd += ["-H", f"Accept: {accept}"]
        if body is not None:
            body_file = Path(tmp) / "body.json"
            body_file.write_text(json.dumps(body))
            cmd += ["-H", "Content-Type: application/json", "--data-binary", f"@{body_file}"]
        for attempt in range(4):
            throttle()
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=100)
            except subprocess.TimeoutExpired:
                die(EXIT_NET, "Timeout reseau vers api.mermaid.ai")
            if res.returncode != 0:
                die(EXIT_NET, f"curl a echoue: {res.stderr.strip()[:200]}")
            code = int(res.stdout.strip() or 0)
            headers = {}
            # -L : le fichier contient les en-tetes de chaque saut, on garde le dernier bloc
            blocks = dump_file.read_text(errors="replace").strip().split("\r\n\r\n")
            for line in blocks[-1].splitlines()[1:]:
                if ":" in line:
                    k, v = line.split(":", 1)
                    headers[k.strip().lower()] = v.strip()
            if code == 429 and attempt < 3:
                time.sleep(min(float(headers.get("retry-after", 5)), 30) * (attempt + 1))
                continue
            return code, headers, out_file.read_bytes()
    return 0, {}, b""


def error_of(raw):
    try:
        e = json.loads(raw)["error"]
        det = e.get("details") or {}
        where = f" (ligne {det['line']}, colonne {det['column']})" if "line" in det else ""
        return f"{e.get('code')}: {e.get('message')}{where}"
    except (ValueError, KeyError, TypeError):
        return raw[:300].decode("utf-8", "replace")


def get_balance(key):
    code, _, raw = call(key, "GET", "/balance")
    if code == 401:
        die(EXIT_KEY, f"Cle refusee: {error_of(raw)}")
    if code != 200:
        die(EXIT_NET, f"/balance HTTP {code}: {error_of(raw)}")
    b = json.loads(raw)
    remaining = b.get("remaining", 0) + b.get("purchased", {}).get("remaining", 0)
    costs = {c["path"]: c["cost"] for c in b.get("costs", [])}
    return b, remaining, costs


def slug(value, label):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", value):
        die(EXIT_USAGE, f"--{label} doit etre en kebab-case minuscule (recu: {value!r})")
    return value


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--name", help="nom descriptif kebab-case (sans extension)")
    p.add_argument("--domain", choices=["personal", "work"])
    p.add_argument("--subject", help="sujet semantique kebab-case (ex: gnl, bnc, demenagement)")
    p.add_argument("--file", help="fichier .mmd ; sinon le code est lu sur stdin")
    p.add_argument("--format", default="svg", choices=["svg", "png", "pdf"])
    p.add_argument("--theme", help="theme Mermaid (default, neutral, forest, dark, base)")
    p.add_argument("--config", help="objet config Mermaid en JSON (fusionne avec --theme)")
    p.add_argument("--mermaid-version", choices=["12.1.0", "11.17.2"])
    p.add_argument("--validate", action="store_true", help="valider d'abord (1 credit)")
    p.add_argument("--min-credits", type=int, default=50, help="seuil sous lequel on s'arrete (defaut 50)")
    p.add_argument("--force", action="store_true", help="ignorer le seuil (accord explicite de l'utilisateur)")
    p.add_argument("--no-open", action="store_true", help="ne pas ouvrir le fichier (CLI)")
    p.add_argument("--balance", action="store_true", help="afficher le solde et quitter")
    a = p.parse_args()

    key = load_key()
    balance, remaining, costs = get_balance(key)
    if a.balance:
        print(json.dumps({"remaining": remaining, "allowance": balance.get("allowance"),
                          "spent": balance.get("spent"), "resetAt": balance.get("resetAt"),
                          "costs": costs}, ensure_ascii=False))
        return

    for flag in ("name", "domain", "subject"):
        if not getattr(a, flag):
            die(EXIT_USAGE, f"--{flag} est obligatoire")
    name, subject = slug(a.name, "name"), slug(a.subject, "subject")

    code_text = Path(a.file).read_text() if a.file else sys.stdin.read()
    if not code_text.strip():
        die(EXIT_USAGE, "Code Mermaid vide")

    need = costs.get("/v1/render", 5) + (costs.get("/v1/validate", 1) if a.validate else 0)
    if remaining < need or (remaining < a.min_credits and not a.force):
        die(EXIT_QUOTA, f"QUOTA_LOW remaining={remaining} seuil={a.min_credits} cout={need} "
                        f"reset={balance.get('resetAt')}. Demander a l'utilisateur ou utiliser --force.")

    config = json.loads(a.config) if a.config else {}
    if a.theme:
        config["theme"] = a.theme
    common = {"code": code_text}
    if config:
        common["config"] = config
    if a.mermaid_version:
        common["mermaidVersion"] = a.mermaid_version

    if a.validate:
        code, _, raw = call(key, "POST", "/validate", common)
        if code != 200:
            die(EXIT_NET, f"/validate HTTP {code}: {error_of(raw)}")
        v = json.loads(raw)
        if not v.get("valid"):
            die(EXIT_INVALID, f"CODE_INVALID {error_of(json.dumps({'error': v.get('error', {})}).encode())}")

    body = dict(common, format=a.format)
    if a.format == "png":
        body["png"] = {"scale": 2, "background": "white"}
    code, headers, raw = call(key, "POST", "/render", body)
    if code == 400:
        die(EXIT_INVALID, f"CODE_INVALID {error_of(raw)}")
    if code == 401:
        die(EXIT_KEY, f"Cle refusee: {error_of(raw)} (ne pas reessayer)")
    if code != 200:
        die(EXIT_NET, f"/render HTTP {code}: {error_of(raw)} [x-request-id={headers.get('x-request-id')}]")

    # --- Rangement ---------------------------------------------------------------
    now = datetime.now()
    month = f"{MONTHS_FR[now.month - 1]}-{now.year}"
    base = AI_GENERATED / month / a.domain / subject
    archive = base / a.format / f"{name}.{a.format}"
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_bytes(raw)
    src = base / "mmd" / f"{name}.mmd"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(code_text)

    kiro_web = in_kiro_web()
    if kiro_web:
        artifact = Path.cwd() / ".kiro-web-artifacts" / f"{name}.{a.format}"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(archive, artifact)
    else:
        artifact = archive
        if a.format in OPENABLE and not a.no_open and shutil.which("cmd.exe"):
            win = subprocess.run(["wslpath", "-w", str(archive)], capture_output=True, text=True).stdout.strip()
            subprocess.Popen(["cmd.exe", "/c", "start", "", win],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    _, remaining_after, _ = get_balance(key)
    LOG_DIR.mkdir(exist_ok=True)
    with USAGE_LOG.open("a") as f:
        f.write(json.dumps({"ts": now.isoformat(timespec="seconds"), "name": name, "domain": a.domain,
                            "subject": subject, "format": a.format, "kiro_web": kiro_web,
                            "cache": headers.get("x-render-cache"), "request_id": headers.get("x-request-id"),
                            "mermaid_version": headers.get("x-mermaid-version"),
                            "credits_before": remaining, "credits_after": remaining_after}) + "\n")

    print(f"ARTIFACT={artifact}")
    print(f"ARCHIVE={archive}")
    print(f"SOURCE={src}")
    print(f"CREDITS_REMAINING={remaining_after}")


if __name__ == "__main__":
    main()
