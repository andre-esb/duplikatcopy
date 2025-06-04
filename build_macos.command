#!/bin/bash

echo "🚀 Baue Duplikatcopy als macOS App..."

# venv aktivieren (optional)
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Cleanup & Build
rm -rf dist build Duplikatcopy.app
python3 setup.py py2app

echo "✅ Fertig! App liegt in ./dist/Duplikatcopy.app"

