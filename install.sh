#!/bin/bash

echo "==============================="
echo "🔧 Installation de la Toolbox Cybersécurité"
echo "==============================="

# Mise à jour des paquets
echo "📦 Mise à jour du système..."
sudo apt-get update -y && sudo apt-get upgrade -y

# Installation de Python3, pip3, et venv
echo "🐍 Installation de Python3, pip et venv..."
sudo apt-get install -y python3 python3-pip python3-venv

# Création de l'environnement virtuel
if [ ! -d "venv" ]; then
  echo "🔒 Création de l'environnement virtuel..."
  python3 -m venv venv
fi

# Activation de l'environnement virtuel
source venv/bin/activate

# Mise à jour de pip dans le venv
pip install --upgrade pip

# Installation de PyQt5 et outils via pip
echo "🎨 Installation de PyQt5, commix, wpscan..."
pip install PyQt5 commix wpscan

# Installation des outils système disponibles
echo "🛠️ Installation des outils via apt..."
sudo apt-get install -y nmap nikto gobuster sqlmap hydra

# Vérification des outils installés
echo "🔍 Vérification des outils installés..."

tools=("nmap" "nikto" "gobuster" "sqlmap" "hydra")
for tool in "${tools[@]}"
do
  if command -v $tool &> /dev/null
  then
    echo "✅ $tool est installé"
  else
    echo "❌ $tool n'a pas pu être installé"
  fi
done

# Vérification de l'environnement virtuel et PyQt5
python3 -c "from PyQt5.QtWidgets import QApplication; print('✅ PyQt5 est prêt dans le venv !')"

echo "✅ Installation terminée !"
echo "👉 Active ton environnement avec : source venv/bin/activate"
echo "👉 Lance la toolbox avec       : python3 cybersecurity_toolbox.py"
