#!/bin/bash
./orchestrator "server" && poetry run gunicorn -c gunicorn_config.py server:app