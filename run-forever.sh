#!/bin/bash

# Start the bot and wait until it starts
until python3 -m disco.cli --config constants.yaml --run-bot --log-level INFO; do

# alert console
echo "[BOT] crashed with exit code $?.  Respawning..." >&2

# sleep so we don't get an insane crash loop
sleep 2

# If exited cleanly, don't restart
done