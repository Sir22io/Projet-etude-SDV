import os
import sys
from datetime import datetime
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QMessageBox, QComboBox
)
from PyQt5.QtCore import QProcess
import psycopg2
from minio import Minio

# === Configuration de base ===
RESULTS_DIR = "results"
LOG_FILE = "toolbox_log.txt"
REPORT_FILE = f"final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
os.makedirs(RESULTS_DIR, exist_ok=True)

# === Fonctions utilitaires ===
def log_message(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def run_tool(command, output_file, ip=None, url=None, tool_name=None):
    full_path = os.path.join(RESULTS_DIR, output_file)
    result = os.system(f"{command} > {full_path} 2>&1")

    if result == 0:
        msg = f"✅ Commande OK : {command} -> {output_file}"
        log_message(msg)
        print(msg)

        if ip and url and tool_name:
            save_to_postgres(ip, url, tool_name, msg)
        upload_to_minio(full_path)
        return msg
    else:
        msg = f"❌ Échec : {command} -> {output_file}"
        log_message(msg)
        print(msg)
        return msg

def save_to_postgres(ip, url, tool, log):
    try:
        conn = psycopg2.connect(
            database="toolbox_db",
            user="postgres",
            password="motdepasse",  # Remplace ici
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO scans (ip_target, url_target, tool_used, log) VALUES (%s, %s, %s, %s)",
            (ip, url, tool, log)
        )
        conn.commit()
        cur.close()
        conn.close()
        print("📥 Enregistré dans PostgreSQL")
    except Exception as e:
        print("❌ Erreur PostgreSQL :", e)

def upload_to_minio(file_path):
    try:
        client = Minio(
            "localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            secure=False
        )
        bucket = "toolbox"
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
        client.fput_object(bucket, os.path.basename(file_path), file_path)
        print(f"📤 Upload MinIO : {file_path}")
    except Exception as e:
        print("❌ Erreur MinIO :", e)

def generate_report():
    with open(REPORT_FILE, "w") as report_file:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as log_file:
                report_file.write("====== Rapport Final CyberSecurity Toolbox ======\n\n")
                report_file.write(log_file.read())
                report_file.write("\n====== Fin du Rapport ======\n")
    upload_to_minio(REPORT_FILE)
    return REPORT_FILE

# === Interface graphique (GUI) PyQt5 ===
class ToolboxApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberSecurity Toolbox - PyQt5")
        self.setGeometry(100, 100, 700, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Adresse IP cible (ex: 127.0.0.1)")
        layout.addWidget(self.ip_input)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("URL cible (ex: http://testphp.vulnweb.com)")
        layout.addWidget(self.url_input)

        self.tool_selector = QComboBox()
        self.tool_selector.addItems(["Nmap", "SQLMap", "WPScan", "Gobuster", "Nikto"])
        layout.addWidget(self.tool_selector)

        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        layout.addWidget(self.output_display)

        run_btn = QPushButton("▶️ Lancer le scan")
        run_btn.clicked.connect(self.run_selected_tool)
        layout.addWidget(run_btn)

        report_btn = QPushButton("🧾 Générer le rapport")
        report_btn.clicked.connect(self.show_report)
        layout.addWidget(report_btn)

        open_results_btn = QPushButton("📂 Ouvrir le dossier des résultats")
        open_results_btn.clicked.connect(self.open_results_folder)
        layout.addWidget(open_results_btn)

        self.setLayout(layout)

    def run_selected_tool(self):
        ip = self.ip_input.text()
        url = self.url_input.text()
        tool = self.tool_selector.currentText()

        if not ip or not url:
            QMessageBox.warning(self, "Champs manquants", "Merci de saisir une IP et une URL.")
            return

        commands = {
            "Nmap": (f"nmap -sP {ip}", "nmap.txt"),
            "SQLMap": (f"sqlmap -u {url} --batch", "sqlmap.txt"),
            "WPScan": (f"wpscan --url {url}", "wpscan.txt"),
            "Gobuster": (f"gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt", "gobuster.txt"),
            "Nikto": (f"nikto -h {url}", "nikto.txt"),
        }

        cmd, outfile = commands[tool]
        result = run_tool(cmd, outfile, ip, url, tool)
        self.output_display.append(result)

    def show_report(self):
        path = generate_report()
        QMessageBox.information(self, "✅ Rapport généré", f"Rapport enregistré : {path}")

    def open_results_folder(self):
        subprocess.run(["xdg-open", os.path.abspath(RESULTS_DIR)])
        QMessageBox.information(self, "✅ Dossier ouvert", "Le dossier des résultats a été ouvert.")

# === Interface CLI (optionnelle)
def cli_mode():
    print("=== Mode CLI ===")
    ip = input("IP cible : ")
    url = input("URL cible : ")

    tools = [
        ("Nmap", f"nmap -sP {ip}", "nmap.txt"),
        ("SQLMap", f"sqlmap -u {url} --batch", "sqlmap.txt"),
        ("WPScan", f"wpscan --url {url}", "wpscan.txt"),
        ("Gobuster", f"gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt", "gobuster.txt"),
        ("Nikto", f"nikto -h {url}", "nikto.txt")
    ]

    for i, (name, _, _) in enumerate(tools, 1):
        print(f"{i}. {name}")
    print("a. Tous | r. Rapport | q. Quitter")

    choice = input("Ton choix : ").strip()
    if choice == 'a':
        for name, cmd, out in tools:
            run_tool(cmd, out, ip, url, name)
    elif choice == 'r':
        generate_report()
    elif choice == 'q':
        sys.exit()
    else:
        try:
            index = int(choice) - 1
            name, cmd, out = tools[index]
            run_tool(cmd, out, ip, url, name)
        except:
            print("Choix invalide.")

# === Lancement principal
if __name__ == "__main__":
    print("1. Lancer l'interface graphique (GUI)")
    print("2. Utiliser en ligne de commande (CLI)")
    mode = input("Choix [1/2] : ")

    if mode == "2":
        cli_mode()
    else:
        app = QApplication(sys.argv)
        window = ToolboxApp()
        window.show()
        sys.exit(app.exec_())
