#!/bin/bash
# LZA MCP Server wrapper — launches the Docker container with AWS credentials
# Profile and region are read from ~/.kiro/.env (sourced below)
source /home/nizar/.kiro/.env

export AWS_PROFILE="${LZA_AWS_PROFILE}"
export AWS_REGION="${LZA_AWS_REGION}"

REPO_PATH="/home/nizar/HomeWspce/lza-mcp-server"
CONFIG_PATH="/home/nizar/HomeWspce/lza-config"

exec "$REPO_PATH/scripts/extract-aws-credentials.sh" \
  docker run \
  --security-opt=no-new-privileges:true \
  --cap-drop=ALL \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=200m \
  --rm -i \
  -v "$CONFIG_PATH:/app/lza-config:rw" \
  -e "LZA_CONFIG_HOST_PATH=$CONFIG_PATH" \
  -e AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY \
  -e AWS_SESSION_TOKEN \
  -e AWS_REGION \
  lza-mcp-server:local
