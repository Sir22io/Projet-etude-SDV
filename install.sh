#!/bin/bash

echo "==============================="
echo "🔧 Installation de la Toolbox"
echo "==============================="

# Mise à jour des paquets
echo "📦 Mise à jour du système..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Installation de Python3 et pip
echo "🐍 Installation de Python3 et pip..."
sudo apt-get install -y python3 python3-pip

# Installation de PyQt5 pour l'interface graphique
echo "🎨 Installation de PyQt5 pour l’interface graphique..."
pip3 install PyQt5
python3 -c "from PyQt5.QtWidgets import QApplication; print('✅ PyQt5 est prêt !')"

# Installation des outils de pentest
echo "🛠️ Installation des outils de pentest..."
sudo apt-get install -y nmap nikto gobuster sqlmap wpscan metasploit-framework hydra commix burpsuite arachni

# Vérification des outils installés
echo "🔍 Vérification des outils installés..."

tools=("nmap" "nikto" "gobuster" "sqlmap" "wpscan" "msfconsole" "hydra" "commix" "burpsuite" "arachni")

for tool in "${tools[@]}"
do
  if command -v $tool &> /dev/null
  then
    echo "✅ $tool est installé"
  else
    echo "❌ $tool n'a pas pu être installé"
  fi
done

echo "✅ Installation terminée avec succès !"
echo "👉 Vous pouvez maintenant lancer la toolbox avec : python3 cybersecurity_toolbox.py"
