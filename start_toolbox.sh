#!/bin/bash

echo "🚀 Démarrage de la CyberSecurity Toolbox"

# 🔐 Démarrage de PostgreSQL
echo "📡 Lancement de PostgreSQL..."
sudo service postgresql start

# ⏳ Petite pause pour laisser les services démarrer
sleep 3

# 📦 Lancement de la toolbox
echo "🖥️ Lancement de l'interface..."
python3 cybersecurity_toolbox.py
