
# CyberSecurity Toolbox

## 📌 Description
Ce projet est une boîte à outils de cybersécurité complète, comprenant des outils offensifs et défensifs prêts à être utilisés. Il permet d'analyser, d'attaquer et de défendre des systèmes à des fins éducatives uniquement.

## 🔍 Installation
1. Clonez le dépôt :
```bash
git clone https://github.com/VOTRE-NOM-UTILISATEUR/Projet-etude-SDV.git
```
2. Rendez le script d'installation exécutable :
```bash
chmod +x install.sh
```
3. Exécutez le script d'installation :
```bash
./install.sh
```

## 💡 Utilisation
Lancez le script Python principal :
```bash
python3 cybersecurity_toolbox.py
```
Un menu interactif vous permettra de choisir les outils à utiliser.

## 📑 Outils inclus
### 🔒 Offensifs :
- **Commix** (Injection de commandes)
- **SQLMap** (Injection SQL)
- **WPScan** (Scanner WordPress)
- **Masscan** (Scanner réseau rapide)
- **Nikto** (Scanner d'applications web)
- **Gobuster** (Scanner de répertoires et fichiers cachés)
- **Arachni** (Scanner de vulnérabilités d'applications web)
- **Fimap** (Détection de LFI - Local File Inclusion)
- **Clusterd** (Attaques sur serveurs d'applications)

### 🛡️ Défensifs :
- **Snort** (Détection d'intrusions réseau - IDS)
- **Suricata** (Moteur IDS/IPS avancé)
- **OpenVAS** (Scanner de vulnérabilités complet)
- **Binwalk** (Analyse et extraction de firmwares)
- **Rkhunter** (Détection de rootkits Linux)
- **Chkrootkit** (Scanner de rootkits Linux)
- **Iptables** (Pare-feu intégré à Linux)
- **Log Analysis** (Analyse des logs système)

## 📊 Résultats
- Les résultats de chaque outil sont enregistrés dans un dossier nommé `results/`.
- Les logs d'exécution sont enregistrés dans `toolbox_log.txt`.
- Un rapport complet est généré sous `final_report.txt`.

## 📄 Licence
Projet éducatif réalisé dans le cadre d'un projet d'étude.

## 📄 Schéma de l'infrastructure du projet

![schema draw io toolbox final](https://github.com/user-attachments/assets/5b21f8d0-aec8-45d5-8bd5-3513295bd446)


