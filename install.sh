#!/bin/bash
echo "📦 Installation des outils nécessaires..."

# Mise à jour des paquets
sudo apt-get update

# Outils installables directement
sudo apt-get install -y python3 python3-pip git \
    sqlmap nikto gobuster nmap \
    binwalk rkhunter chkrootkit \
    ruby-full

# WPScan (via Ruby)
if ! command -v wpscan &> /dev/null; then
    echo "📥 Installation de WPScan..."
    gem install wpscan
fi

# OpenVAS
if ! command -v gvm &> /dev/null; then
    echo "📥 Installation de OpenVAS..."
    sudo apt-get install -y openvas
fi

# Suricata
if ! command -v suricata &> /dev/null; then
    echo "📥 Installation de Suricata..."
    sudo apt-get install -y suricata
fi

# Commix
if ! command -v commix &> /dev/null; then
    echo "📥 Installation de Commix..."
    git clone https://github.com/commixproject/commix.git /opt/commix
    ln -s /opt/commix/commix.py /usr/local/bin/commix
    chmod +x /usr/local/bin/commix
fi

# Masscan
if ! command -v masscan &> /dev/null; then
    echo "📥 Installation de Masscan..."
    sudo apt-get install -y masscan
fi

# Fimap
if ! command -v fimap &> /dev/null; then
    echo "📥 Installation de Fimap..."
    git clone https://github.com/kurobeats/fimap.git /opt/fimap
    ln -s /opt/fimap/fimap.py /usr/local/bin/fimap
    chmod +x /usr/local/bin/fimap
fi

# Clusterd
if ! command -v clusterd &> /dev/null; then
    echo "📥 Installation de Clusterd..."
    git clone https://github.com/hatRiot/clusterd.git /opt/clusterd
    ln -s /opt/clusterd/clusterd.py /usr/local/bin/clusterd
    chmod +x /usr/local/bin/clusterd
fi

# (Optionnel) Arachni (obsolète, à installer manuellement si nécessaire)
if ! command -v arachni &> /dev/null; then
    echo "⚠️ Arachni non installé : ce scanner est obsolète et difficile à installer."
    echo "ℹ️ Vous pouvez le retirer du projet ou l’installer manuellement si besoin."
fi

# Installer les dépendances Python
if [ -f requirements.txt ]; then
    echo "📦 Installation des dépendances Python..."
    pip3 install -r requirements.txt
fi

echo "✅ Installation terminée avec succès."
