#!/bin/bash

echo "🔧 Lancement de l'installation de la CyberSecurity Toolbox..."

# === 🔁 Mise à jour des dépôts ===
sudo apt update && sudo apt upgrade -y

# === 🧰 Installation des outils de pentest nécessaires ===
echo "🛠 Installation des outils de base..."
sudo apt install -y nmap nikto gobuster hydra \
                    python3 python3-pip python3-venv \
                    ruby-full curl unzip default-jre

# === 📦 Installation de SQLMap via pip ===
echo "📦 Installation de SQLMap..."
pip install sqlmap --break-system-packages

# === 💎 Installation de WPScan via Ruby ===
if ! command -v wpscan &> /dev/null; then
  echo "🔧 Installation de WPScan..."
  sudo gem install wpscan
else
  echo "✅ WPScan déjà installé"
fi

# === 🧪 Vérification de PyQt5 ===
echo "🔍 Vérification de PyQt5..."
if ! python3 -c "import PyQt5" &> /dev/null; then
  echo "🔧 PyQt5 non détecté. Installation..."
  pip install PyQt5 --break-system-packages
else
  echo "✅ PyQt5 déjà installé"
fi

# === 🔐 Module cryptography (pour chiffrement Fernet) ===
echo "🔒 Vérification du module cryptography..."
if ! python3 -c "from cryptography.fernet import Fernet" &> /dev/null; then
  pip install cryptography --break-system-packages
fi

# === 📁 Création des dossiers nécessaires ===
echo "📁 Création des dossiers..."
mkdir -p results templates

# === 📄 Modèle HTML de rapport (Jinja2) ===
if [ ! -f templates/report_template.html ]; then
  echo "📄 Création du modèle de rapport HTML..."
  cat <<EOT > templates/report_template.html
<!DOCTYPE html>
<html>
<head><title>Rapport de Sécurité</title></head>
<body>
  <h1>Rapport de la CyberSecurity Toolbox</h1>
  <pre>{{ logs }}</pre>
</body>
</html>
EOT
fi

# === ✅ Message final pour le client ===
echo ""
echo "🚀 La CyberSecurity Toolbox a bien été installée."
echo ""
echo "📁 Vous pouvez maintenant l'utiliser avec les commandes suivantes :"
echo ""
echo "👉 Pour lancer l'application :"
echo "   python3 cybersecurity_toolbox.py"
echo ""
echo "👉 Vous aurez le choix entre l'interface graphique (GUI) et la version ligne de commande (CLI)."
echo ""
echo "📂 Tous les résultats seront enregistrés automatiquement dans le dossier ./results/"
echo "📄 Un rapport final chiffré sera généré dans final_report.txt (chiffrement automatique avec Fernet)."
echo ""
echo "✅ Installation terminée. Bon test d'intrusion !"
