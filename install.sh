#!/bin/bash
echo "Installation des outils nécessaires..."

# Update package list
sudo apt-get update

# Installer les outils de base
sudo apt-get install -y python3 python3-pip masscan nikto gobuster nmap binwalk rkhunter chkrootkit ruby-full

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

# Installer Arachni (nécessite un téléchargement manuel)
if ! command -v arachni &> /dev/null
then
    echo "Installation d'Arachni..."
    git clone https://github.com/Arachni/arachni.git
    cd arachni && sudo ruby install.rb && cd ..
fi

# Installer Fimap
if ! command -v fimap &> /dev/null
then
    echo "Installation de Fimap..."
    git clone https://github.com/kurobeats/fimap.git
    # fimap est un script Python, pas besoin d'installation complexe
    echo "Fimap installé depuis GitHub"
fi

# Installer Clusterd
if ! command -v clusterd &> /dev/null
then
    echo "Installation de Clusterd..."
    git clone https://github.com/hatRiot/clusterd.git
    cd clusterd && sudo pip3 install -r requirements.txt && cd ..
fi

# Installer Commix
if ! command -v commix &> /dev/null
then
    echo "Installation de Commix..."
    git clone https://github.com/commixproject/commix.git
    cd commix && sudo python3 setup.py install && cd ..
fi

# Installer des packages Python supplémentaires pour les outils
pip3 install -r requirements.txt

echo "✅ Installation terminée."
