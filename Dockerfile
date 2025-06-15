# Utilise une image de base Python légère avec Debian Buster
FROM python:3.9-slim-bullseye

# Empêche Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Force la sortie des logs de Python vers stdout/stderr
ENV PYTHONUNBUFFERED 1

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances Python et installe-les
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Installe les dépendances système et les outils de sécurité
# Utilise DEBIAN_FRONTEND=noninteractive pour éviter les invites de dialogue
ENV DEBIAN_FRONTEND=noninteractive

RUN echo "deb http://deb.debian.org/debian bullseye main non-free" > /etc/apt/sources.list.d/non-free.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    unzip \
    p7zip-full \
    default-jre \
    perl \
    ruby \
    ruby-dev \
    build-essential \
    libpcap-dev \
    nmap \
    john \
    aircrack-ng \
    nikto \
    hydra \
    gobuster \
    postgresql-client \
    tshark \
    sqlmap \
    ettercap-common \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Crée un répertoire pour les certificats SSL et génère les certificats auto-signés
RUN mkdir -p /usr/local/etc/ssl/ && \
    openssl req -x509 -newkey rsa:4096 -nodes -out /usr/local/etc/ssl/cert.pem -keyout /usr/local/etc/ssl/key.pem -days 365 -subj "/CN=localhost"

# Installation de Shodan CLI
RUN pip install shodan

# Installation de SSLyze
RUN pip install sslyze

# Crée le répertoire des outils
RUN mkdir -p /app/tools/

# Téléchargement et extraction de DirBuster (JAR)
ARG DIRBUSTER_URL="https://sourceforge.net/projects/dirbuster/files/latest/download"
RUN wget -qO dirbuster.jar "$DIRBUSTER_URL" && \
    mv dirbuster.jar /app/tools/

# Téléchargement de Burp Suite Community (JAR)
ARG BURP_URL="https://portswigger.net/burp/releases/download?product=community&version=latest&type=jar"
RUN wget -qO burpsuite_community.jar "$BURP_URL" && \
    mv burpsuite_community.jar /app/tools/

# Téléchargement de OWASP ZAP (JAR)
ARG ZAP_URL="https://github.com/zaproxy/zaproxy/releases/download/v2.16.1/ZAP_2.16.1_Core.zip"
RUN wget -qO zap_core.zip "$ZAP_URL" && \
    unzip zap_core.zip -d /tmp/zap_install && \
    mv /tmp/zap_install/ZAP_2.16.1/zap-2.16.1.jar /app/tools/zap.jar && \
    rm -rf /tmp/zap_install zap_core.zip

# Copie le reste du code de l'application
COPY app/ .

# Expose le port sur lequel Flask écoute
EXPOSE 5000

# Commande par défaut pour exécuter l'application Flask
CMD ["python", "app.py"]