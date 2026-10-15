---
name: gnl-video-deck
description: Traite les jobs « deck vidéo » de la file d'attente agent de GNL Process. Pour chaque question ratée d'un examen, l'agent conçoit une architecture AWS draw.io (skill aws-architecture-diagram), l'exporte en PNG, écrit un speech d'animateur (architecture + chaque option commentée), génère l'audio TTS Polly, et assemble un .apkg Anki (image + audio par carte). Activates when the user says "traite les jobs deck vidéo", "process video deck jobs", "génère les decks vidéo des ratées", or any equivalent.
---

# GNL — Deck vidéo des questions ratées (traitement agent)

## Déclencheur
L'utilisateur dit « traite les jobs deck vidéo » (ou équivalent). Un bouton
« 🎬 Deck vidéo (ratées) » du dashboard GNL a créé un ou plusieurs jobs dans la
file d'attente agent.

## Contexte
- File des jobs : `<repo gnl-process>/.agent-jobs/pending/*.json`
  (ou `$GNL_JOBS_DIR/pending`). Repo prod : `/mnt/d/PERSONAL/SKILLS/Technical/workspace/gnl-process`.
- Chaque job : `{id, type:"video_deck", exam, failed_nums:[...], theme, subtheme}`.
- Profil AWS : Bedrock = `csna-operations-sso-828` / `ca-central-1` ;
  Polly = `personal-production-sso-760` / `us-east-1`.
- Python : `env -u VIRTUAL_ENV PATH=/usr/bin:/bin /usr/bin/python3`.

## Procédure (pour CHAQUE job pending)

1. **Lire le job** et charger le markdown source de l'examen
   (`gnl_core.anki_review._find_exam_markdown(exam, theme, subtheme)`),
   puis `parse_exam_questions(md)` pour obtenir, par question ratée :
   l'énoncé, les options, et l'explication par option.

2. **Pour chaque question ratée** (dans `failed_nums`) :
   a. **Comprendre** la question (énoncé + options + explication).
   b. **Concevoir l'architecture AWS** de la solution correcte et la dessiner
      avec la skill `aws-architecture-diagram` (draw.io, icônes mxgraph.aws4
      officielles, couleurs par catégorie, liens console si IDs connus).
   c. **Exporter en PNG** (draw.io desktop/CLI ou rendu). Nommer `Q{num}.png`.
   d. **Écrire le speech d'animateur** (anglais), structuré :
      « Here is the architecture for this question. It is about <sujet>. »
      puis, pour CHAQUE option : « Option A is correct/incorrect because … »,
      « Option B is … », etc. (reprendre l'explication par option du markdown).
   e. **Générer l'audio** : `gnl_core.anki_tts.synthesize(speech, out_mp3,
      voice='Matthew', engine='neural', profile='personal-production-sso-760')`.

3. **Assembler le .apkg** : un deck où chaque carte = l'image `Q{num}.png`
   (recto, visible) + le tag `[sound:Q{num}.mp3]`, les PNG+MP3 dans
   `media_files`. Réutiliser le modèle genanki de `step5_anki` ou un modèle
   minimal « révision » (pas de test : image + audio seulement).
   Sortie : `{EXAM_BASE}/Anki-generation/anki/<exam>-video.apkg`
   (emplacement STANDARD Anki — ne PAS créer de sous-dossier `video-deck/`).
   Les PNG/MP3 intermédiaires peuvent vivre dans
   `{EXAM_BASE}/Anki-generation/video-assets/<exam>/` mais le `.apkg` final va
   TOUJOURS dans `Anki-generation/anki/`.

4. **Marquer le job terminé** :
   `gnl_core.agent_jobs.mark_done(job_id, result={'apkg': <path>})`.

5. **Rendre compte** à l'utilisateur : par examen, nombre de questions
   traitées + chemin du `.apkg`.

## Règles
- Respecter la règle d'or : NE PAS toucher le pipeline exam existant ; ce deck
  est un artefact séparé (`-video.apkg`).
- Si la génération d'une architecture échoue pour une question, continuer les
  autres (best-effort) et le signaler.
- Valider le `.apkg` (média embarqués + tags `[sound:]`) avant de conclure.
- Nettoyer les fichiers temporaires.
