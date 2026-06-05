# kiro-configs — Notes de projet

> Mémoire locale du projet (Principle 10). Mise à jour PENDANT les sessions.

## État actuel (2026-06-05)

- Architecture documentée : `forge/steering/kiro-configs-architecture.md`
- Conventions documentées : `forge/steering/conventions-kiro-configs.md`
- README réécrit, zzz/ documenté, memory-supervisor.jsonl créé
- Doublon categories.json nettoyé

## Décisions prises

- Les steering files d'architecture restent dans `forge/steering/` (pas shared/, pas meta/)
- IT-Supervisor = garant unique de la cohérence globale
- Mémoire : max 50 entités, confirmation obligatoire avant écriture

## À faire (prochaines sessions)

- [ ] Auditer les prompts compass/exp2/forge pour homogénéité de structure
- [ ] Vérifier que les wrappers obsolètes (mural, n8n, lza) sont documentés comme désactivés
- [ ] Considérer nettoyage mémoire trimestriel (memory-compass a 11 entités, OK)
