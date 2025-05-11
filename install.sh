#!/bin/bash
echo "Installation des outils nécessaires..."

# Update package list (assure-toi que le système est bien configuré)
echo "Mise à jour des paquets..."
sudo apt-get update -y

# Installer les outils nécessaires
echo "Installation des outils de base..."
sudo apt-get install -y python3 python3-pip masscan nikto gobuster nmap commix binwalk rkhunter chkrootkit

# Installer SQLMap
if ! command -v sqlmap &> /dev/null
then
    echo "Installation de SQLMap..."
    sudo apt-get install -y sqlmap
fi

# Installer WPScan (via Ruby)
if ! command -v wpscan &> /dev/null
then
    echo "Installation de WPScan..."
    sudo apt-get install ruby-full
    sudo gem install wpscan
fi

# Installer OpenVAS
if ! command -v gvm &> /dev/null
then
    echo "Installation d'OpenVAS..."
    sudo apt-get install -y openvas
fi

# Installer Suricata
if ! command -v suricata &> /dev/null
then
    echo "Installation de Suricata..."
    sudo apt-get install -y suricata
fi

# Installer Arachni
if ! command -v arachni &> /dev/null
then
    echo "Installation d'Arachni..."
    sudo apt-get install -y arachni
fi

# Installer Fimap
if ! command -v fimap &> /dev/null
then
    echo "Installation de Fimap..."
    sudo apt-get install -y fimap
fi

# Installer Clusterd
if ! command -v clusterd &> /dev/null
then
    echo "Installation de Clusterd..."
    sudo apt-get install -y clusterd
fi

# Installation des packages Python requis via requirements.txt
echo "Installation des packages Python..."
pip3 install -r requirements.txt

echo "✅ Installation terminée."

xdg-open README.md 2>/dev/null || cat README.md

