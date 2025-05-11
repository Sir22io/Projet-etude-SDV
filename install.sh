#!/bin/bash

# Mise à jour des dépôts
sudo apt-get update -y
sudo apt-get upgrade -y

# Installation des outils nécessaires pour le pentesting
echo "Installation des outils de pentesting..."

# Installation des outils de base
sudo apt-get install nmap nikto gobuster sqlmap wpscan metasploit-framework hydra commix burpsuite arachni -y

# Vérification que chaque outil est bien installé
echo "Vérification des installations..."

# Liste des outils à vérifier
tools=("nmap" "nikto" "gobuster" "sqlmap" "wpscan" "msfconsole" "hydra" "commix" "burpsuite" "arachni")

# Vérification que chaque outil est installé
for tool in "${tools[@]}"
do
  if command -v $tool &> /dev/null
  then
    echo "$tool est installé"
  else
    echo "$tool n'a pas pu être installé"
  fi
done

# Finalisation de l'installation
echo "Installation terminée!"
echo "Vous pouvez maintenant tester les outils en lançant des scans via leurs commandes respectives."
