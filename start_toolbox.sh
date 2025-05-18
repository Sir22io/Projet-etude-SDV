#!/bin/bash

echo "🚀 Démarrage de la CyberSecurity Toolbox"

# 🔐 Démarrage de PostgreSQL
echo "📡 Lancement de PostgreSQL..."
sudo service postgresql start

# ☁️ Démarrage de MinIO dans un terminal séparé
echo "☁️ Lancement de MinIO..."
gnome-terminal -- bash -c "minio server /mnt/data; exec bash"

# ⏳ Petite pause pour laisser les services démarrer
sleep 3

# 📦 Lancement de la toolbox
echo "🖥️ Lancement de l'interface..."
python3 cybersecurity_toolbox.py
