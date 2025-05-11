#!/bin/bash

# Mise à jour du système et mise à niveau
echo "Mise à jour du système et mise à niveau des paquets..."
apt update && apt upgrade -y

# Liste des outils à installer
TOOLS=("commix" "wpscan" "masscan" "gobuster" "nikto" "arachni" "fimap" "clusterd" "git" "curl" "python3-pip")

# Installation des outils nécessaires
for TOOL in "${TOOLS[@]}"; do
    if ! command -v $TOOL &> /dev/null
    then
        echo "$TOOL n'est pas installé. Installation en cours..."
        apt install -y $TOOL
    else
        echo "$TOOL est déjà installé."
    fi
done

# Installation de dépendances supplémentaires pour les outils basés sur Python
echo "Installation de dépendances Python..."
pip3 install --upgrade pip
pip3 install requests beautifulsoup4

# Vérification et installation de git et curl si nécessaire
if ! command -v git &> /dev/null
then
    echo "Git n'est pas installé. Installation de Git..."
    apt install -y git
fi

if ! command -v curl &> /dev/null
then
    echo "Curl n'est pas installé. Installation de Curl..."
    apt install -y curl
fi

# Confirmation de l'installation
echo "Installation terminée avec succès !"
