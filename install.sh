#!/bin/bash

echo "🛠️ Installation de la CyberSecurity Toolbox..."

# 🔄 Mise à jour du système
sudo apt update && sudo apt upgrade -y

# 🐍 Python, pip, venv
sudo apt install -y python3 python3-pip python3-venv

# 🐘 PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# ☁️ MinIO (téléchargement et installation)
if ! command -v minio &> /dev/null
then
    echo "⬇️ Installation de MinIO..."
    wget https://dl.min.io/server/minio/release/linux-amd64/minio -O minio
    chmod +x minio
    sudo mv minio /usr/local/bin/
fi

# 📦 Installation des outils de pentest
sudo apt install -y nmap nikto gobuster sqlmap hydra wpscan

# 🐍 Installation de dépendances Python
pip3 install -U pip
pip3 install PyQt5 psycopg2-binary minio

# 📂 Création du dossier MinIO
sudo mkdir -p /mnt/data
sudo chown $USER:$USER /mnt/data

# 🛠 Création de la base PostgreSQL
echo "🧱 Création de la base PostgreSQL..."
sudo -u postgres psql <<EOF
CREATE DATABASE toolbox_db;
\c toolbox_db
CREATE TABLE IF NOT EXISTS scans (
    id SERIAL PRIMARY KEY,
    ip_target VARCHAR(50),
    url_target TEXT,
    tool_used TEXT,
    log TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
EOF

echo "✅ Installation terminée avec succès !"
