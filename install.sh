
#!/bin/bash
echo "Installation des outils nécessaires..."

# Update package list
 apt-get update

# Installer les outils
 apt-get install -y python3 python3-pip masscan nikto gobuster nmap commix binwalk rkhunter chkrootkit

# Installer SQLMap
if ! command -v sqlmap &> /dev/null
then
    echo "Installation de SQLMap..."
     apt-get install -y sqlmap
fi

# Installer WPScan (via Ruby)
if ! command -v wpscan &> /dev/null
then
    echo "Installation de WPScan..."
     apt-get install ruby-full
     gem install wpscan
fi

# Installer OpenVAS
if ! command -v gvm &> /dev/null
then
    echo "Installation d'OpenVAS..."
     apt-get install -y openvas
fi

# Installer Suricata
if ! command -v suricata &> /dev/null
then
    echo "Installation de Suricata..."
     apt-get install -y suricata
fi

# Installer Arachni
if ! command -v arachni &> /dev/null
then
    echo "Installation d'Arachni..."
     apt-get install -y arachni
fi

# Installer Fimap
if ! command -v fimap &> /dev/null
then
    echo "Installation de Fimap..."
     apt-get install -y fimap
fi

# Installer Clusterd
if ! command -v clusterd &> /dev/null
then
    echo "Installation de Clusterd..."
     apt-get install -y clusterd
fi

# Installation des packages Python requis
pip3 install -r requirements.txt

echo "✅ Installation terminée."
