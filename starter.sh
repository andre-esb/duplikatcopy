#!/bin/bash

echo "🌀 Starte Duplikatcopy..."

# Virtuelles Environment prüfen/anlegen
if [ ! -d "venv" ]; then
    echo "🔧 Erstelle virtuelles Environment..."
    python3 -m venv venv
fi

# Environment aktivieren
source venv/bin/activate

# Dependencies prüfen/aktualisieren
echo "📦 Installiere Anforderungen aus requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# App starten
echo "🚀 Starte App..."
python3 main.py

