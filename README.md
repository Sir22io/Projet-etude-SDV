# 🛡️ CyberSecurity Toolbox

**CyberSecurity Toolbox** est une application modulaire et automatisée conçue pour faciliter la réalisation de tests d’intrusion (pentesting).  
Elle permet aux professionnels de la cybersécurité de lancer rapidement différents outils d’analyse depuis une **interface graphique (GUI)** ou en **ligne de commande (CLI)** selon leurs préférences.

---

## 🎯 Objectifs

- Simplifier l’usage d’outils de pentest dans un environnement unifié
- Gagner du temps grâce à l'automatisation des scans
- Générer des rapports personnalisés et horodatés
- Offrir une flexibilité d’utilisation : **GUI ou CLI**
- Centraliser les résultats dans une base de données PostgreSQL
- Archiver les preuves dans un stockage MinIO (API S3)

---

## 🧰 Fonctionnalités clés

- 🖥 Interface graphique en PyQt5 intuitive et interactive
- 💻 Mode terminal CLI pour les utilisateurs expérimentés
- 📦 Intégration d’outils offensifs :
  - Nmap, Nikto, Gobuster, SQLMap, WPScan, Hydra, Commix, BurpSuite, Arachni
- 🗂 Organisation automatique des résultats
- 🐘 Base PostgreSQL pour centraliser les données
- ☁️ MinIO pour stocker les fichiers volumineux (captures, logs…)

---

## 🖥️ Interface ou Terminal : à vous de choisir !

Lorsque vous lancez la toolbox, vous avez deux options :
Interface graphique (GUI)
Mode terminal (CLI)

Chaque mode donne accès aux mêmes outils et fonctionnalités.

---

## 🔧 Installation (à faire une seule fois)

```bash
chmod +x install.sh
./install.sh

Ce script :

Installe tous les outils nécessaires (Python, PostgreSQL, MinIO, outils de pentest)

Configure la base de données toolbox_db

Installe toutes les dépendances Python (PyQt5, psycopg2-binary, minio)

Lancer la toolbox

chmod +x start_toolbox.sh
./start_toolbox.sh
Ce script :

Démarre les services PostgreSQL et MinIO

Lance automatiquement la toolbox

Arborescence du projet

CyberSecurity-Toolbox/
├── install.sh                # Script d'installation complet
├── start_toolbox.sh         # Lancement automatique (services + toolbox)
├── cybersecurity_toolbox.py # Application principale (GUI + CLI)
├── results/                 # Résultats individuels des outils (fichiers .txt)
├── toolbox_log.txt          # Journal global des actions
├── final_report_*.txt       # Rapport global généré automatiquement
├── README.md                # Ce fichier de présentation

Pré-requis

OS : Kali Linux, Debian ou Ubuntu

Python 3.8 ou supérieur

Connexion Internet (pour l’installation)

Privilèges administrateur (sudo)


Développé par
Ce projet a été réalisé dans le cadre du Mastère CYBER à SupdeVinci- Année 2024-2025.

Groupe projet :

Sofiane

Clément

Darwin

⚠️ Usage strictement autorisé
⚠️ Ce projet est fourni à des fins éducatives et professionnelles avec l’accord du client.
❌ Toute utilisation sans autorisation explicite de la cible est interdite.
✅ L’équipe décline toute responsabilité en cas d’usage illégal.
