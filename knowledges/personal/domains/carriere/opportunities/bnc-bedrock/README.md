# 🎯 CV Builder — Format Alithya

> Génère automatiquement une nouvelle version du CV Alithya (format .docx) en injectant de nouvelles expériences dans la dernière version existante.

## Quick Access

```bash
# Générer la prochaine version du CV
cd /home/nizar/HomeWspce/kiro-configs/knowledges/personal/domains/carriere/opportunities/bnc-bedrock
python3 build-cv-format-alithya.py
```

Le script :
1. Détecte automatiquement la dernière version (ex: V17)
2. Injecte les expériences depuis `assets/experiences/*.md`
3. Génère V18 dans `output/`
4. Copie le résultat dans Dropbox (`CV_officiels-Format-Alithya/`)

## Ce que fait le script

| Étape | Action |
|-------|--------|
| 1 | Scan `output/` et `assets/` pour trouver le CV avec le numéro de version le plus élevé |
| 2 | Lit les fichiers `.md` dans `assets/experiences/` (triés par nom = ordre d'insertion) |
| 3 | Convertit chaque expérience en XML Word avec les styles Alithya (Gras, Puce1, NormalArial) |
| 4 | Injecte les expériences **avant** la première expérience existante dans le template |
| 5 | Sauvegarde `output/...v{N+1}.docx` + copie dans Dropbox |

## Structure

```
bnc-bedrock/
├── build-cv-format-alithya.py       ← script principal
├── README.md                         ← ce fichier
├── assets/
│   ├── Alithya - AJROUD Nizar - CV FR-v16.docx   ← version de base initiale
│   ├── perso-v7-en.docx                           ← CV anglais (référence)
│   └── experiences/                                ← 1 fichier = 1 expérience
│       ├── 01-poste-actuel-beneva-salsa.md
│       ├── 02-bixi.md
│       └── 03-bedrock.md
├── output/
│   └── Alithya - AJROUD Nizar - CV FR-v17.docx   ← dernière version générée
└── notes.md                                        ← notes stratégie opportunité
```

## Ajouter une nouvelle expérience

1. Créer un fichier `.md` dans `assets/experiences/`
2. Nommer avec un préfixe numérique (ex: `00-nouvelle-mission.md` pour qu'elle apparaisse en premier)
3. Exécuter le script → nouvelle version générée

### Format du fichier .md

```markdown
> Client : NomClient 01/2026 à ce jour

# 11 Titre du Rôle

**Projet :** Description du projet

Paragraphe de contexte...

* Bullet point 1
* Bullet point 2

Environnement technologique :

* Tech 1
* Tech 2

**Méthodologies :** Agile/Scrum
```

**Règles :**
- `> ...` → Ligne client/dates (date alignée à droite automatiquement)
- `# N Titre` → Titre d'expérience (format `# ` + numéro + TAB + titre)
- `* ...` → Puces (style Puce1, interligne 1.5)
- Ligne finissant par `:` → Sous-titre gras (Environnement technologique)
- `**...**` → Texte bold

## Numérotation

- Les **nouvelles** expériences portent les numéros suivants après le dernier existant (V16 finit à #7 → nouvelles = #8, #9, #10)
- Les expériences **existantes** ne sont jamais renumérotées

## Sortie

- `output/` — version locale
- `C:\Users\nizar\Dropbox\AAA_PRIVATE_LIFE\Job\NIZAR\CVs\CV_officiels-Format-Alithya\` — copie Dropbox (sync auto)

## Prérequis

- Python 3.x (pas de dépendances externes)
- Accès au chemin Dropbox via `/mnt/c/...` (WSL)
