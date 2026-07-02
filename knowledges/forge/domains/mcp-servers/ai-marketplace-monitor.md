---
name: ai-marketplace-monitor
description: Surveillance automatique de Facebook Marketplace avec IA — notifications Telegram quand une annonce correspond aux critères.
---
# AI Marketplace Monitor

- **Status**: installed
- **JSON key**: N/A (Docker standalone, pas un MCP server)
- **Type**: Docker container (`aimm`)
- **Image**: `ghcr.io/bopeng/ai-marketplace-monitor:latest`
- **Source**: https://github.com/BoPeng/ai-marketplace-monitor (⭐257)
- **Docs**: https://ai-marketplace-monitor.readthedocs.io/
- **Verdict**: adopted — monitoring FB Marketplace avec notifications Telegram

## Accès

- Web UI: http://localhost:8467
- noVNC (browser view): via Web UI → bouton "Browser"
- Config: `~/.ai-marketplace-monitor/config.toml`

## Commandes Docker

```bash
# Démarrer
docker start aimm

# Arrêter
docker stop aimm

# Voir les logs
docker exec aimm cat /root/.ai-marketplace-monitor/ai-marketplace-monitor.log | grep -v "in-event" | tail -30

# Redémarrer
docker restart aimm

# Supprimer et recréer
docker stop aimm && docker rm aimm
docker run -d --name aimm \
  -p 8467:8467 \
  -v "$HOME/.ai-marketplace-monitor:/root/.ai-marketplace-monitor" \
  -e FACEBOOK_USERNAME="nizar.ajroud@gmail.com" \
  -e FACEBOOK_PASSWORD="<MOT_DE_PASSE>" \
  -e TELEGRAM_BOT_TOKEN="<TOKEN>" \
  --restart unless-stopped \
  ghcr.io/bopeng/ai-marketplace-monitor:latest
```

## Configuration actuelle

- Items: climatiseur Hisense 6000 BTU (50-250$) + climatiseur 8000 BTU (100-350$)
- Zone: Montreal + rayon 40 km
- Fréquence: 30-60 minutes
- Notification: Telegram (chat 1267288999)

## Notes

- Premier login Facebook: se connecter manuellement via noVNC (Web UI → Browser)
- Les cookies sont persistés dans `~/.ai-marketplace-monitor/`
- Hot-reload: modifier config.toml = rechargement automatique (pas besoin de restart)
- Pour ajouter un item: ajouter une section `[item.nom]` dans config.toml
