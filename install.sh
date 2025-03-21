
#!/bin/bash
echo "Installation des outils nécessaires..."

# Mise à jour des paquets
sudo apt-get update

# Installer les outils Linux nécessaires via apt-get
sudo apt-get install -y python3 python3-pip masscan nikto gobuster nmap binwalk rkhunter chkrootkit snort suricata openvas fimap

# Installation de SQLMap via pip3 si nécessaire
if ! command -v sqlmap &> /dev/null
then
    echo "Installation de SQLMap via pip3..."
    pip3 install sqlmap
fi

# Installation de Commix via pip3 si nécessaire
if ! command -v commix &> /dev/null
then
    echo "Installation de Commix via pip3..."
    pip3 install commix
fi

# Installation de WPScan via Ruby si nécessaire
if ! command -v wpscan &> /dev/null
then
    echo "Installation de WPScan via Ruby..."
    sudo apt-get install ruby-full -y
    sudo gem install wpscan
fi

# Installation de Arachni si nécessaire
if ! command -v arachni &> /dev/null
then
    echo "Installation d'Arachni..."
    sudo apt-get install arachni -y
fi

echo "✅ Installation terminée."
