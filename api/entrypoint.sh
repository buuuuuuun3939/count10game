#!/bin/bash
set -e

echo "=== Starting API container ==="

# DBを待つ
until nc -z db 5432; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

echo "Database ready! 🚀"

# アプリ起動
exec gunicorn \
  -w 4 \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  app:app

