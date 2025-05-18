#!/bin/bash

echo "==============================="
echo "🔧 INSTALLATION DE LA TOOLBOX"
echo "==============================="

# 📦 Mise à jour du système
echo "📦 Mise à jour des dépôts..."
sudo apt update && sudo apt upgrade -y

# 📁 Création des dossiers nécessaires
echo "📁 Création des dossiers..."
mkdir -p results
touch toolbox_log.txt
touch final_report.txt

# 🐘 Installation de PostgreSQL
echo "🐘 Installation de PostgreSQL..."
sudo apt install postgresql postgresql-contrib -y

# ☁️ Installation de MinIO
echo "☁️ Installation de MinIO..."
wget https://dl.min.io/server/minio/release/linux-amd64/minio -O minio
chmod +x minio
sudo mv minio /usr/local/bin/
sudo mkdir -p /mnt/data

# 🧪 Installation des outils de Pentest de base
echo "🛠️ Installation des outils de pentest..."
sudo apt install -y nmap nikto gobuster hydra wpscan sqlmap

# 📦 Installation de Python & pip si manquant
echo "🐍 Installation de Python3 et pip..."
sudo apt install python3 python3-pip -y

# 🧠 Installation des bibliothèques Python requises
echo "📚 Installation des bibliothèques Python (PyQt5, psycopg2, minio)..."
pip3 install --break-system-packages PyQt5 psycopg2-binary minio

# ✅ Vérification des outils installés
echo "🔍 Vérification des installations..."
tools=("nmap" "nikto" "gobuster" "hydra" "sqlmap" "wpscan" "minio")
for tool in "${tools[@]}"
do
  if command -v $tool &> /dev/null
  then
    echo "✅ $tool est installé"
  else
    echo "❌ $tool n'a pas pu être installé"
  fi
done

echo "🎉 Installation terminée avec succès !"
echo "👉 Tu peux maintenant démarrer MinIO avec :"
echo "   minio server /mnt/data"
