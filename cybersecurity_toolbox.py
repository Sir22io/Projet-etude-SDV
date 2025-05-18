import os
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QMessageBox, QComboBox)
import sys

RESULTS_DIR = "results"
LOG_FILE = "toolbox_log.txt"
REPORT_FILE = "final_report.txt"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Fonctions de base
def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

def run_tool(command, output_file):
    full_path = os.path.join(RESULTS_DIR, output_file)
    result = os.system(f"{command} > {full_path} 2>&1")
    if result == 0:
        msg = f"✅ Commande OK : {command}. Résultat dans {output_file}"
        log_message(msg)
        return msg
    else:
        msg = f"❌ Échec commande : {command}. Voir {output_file}"
        log_message(msg)
        return msg

def generate_report():
    with open(REPORT_FILE, "w") as report_file:
        report_file.write("====== Rapport Final de la CyberSecurity Toolbox ======\n\n")

        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as log_file:
                log_lines = log_file.readlines()

            for line in log_lines:
                report_file.write(f"🔹 {line.strip()}\n")
                if "Résultat dans" in line:
                    parts = line.strip().split("Résultat dans")
                    if len(parts) > 1:
                        filename = parts[1].strip()
                        filepath = os.path.join(RESULTS_DIR, filename)
                        if os.path.exists(filepath):
                            report_file.write(f"\n📄 Contenu de {filename} :\n")
                            with open(filepath, "r", errors='ignore') as result_file:
                                report_file.write(result_file.read())
                                report_file.write("\n\n")
                        else:
                            report_file.write(f"(⚠️ Fichier {filename} introuvable)\n\n")

        report_file.write("====== Fin du Rapport ======\n")

    print(f"📄 Rapport généré avec les résultats complets dans {REPORT_FILE}")
    return REPORT_FILE

# Interface PyQt5
class ToolboxApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberSecurity Toolbox - PyQt5")
        self.setGeometry(100, 100, 600, 400)
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
        self.tool_selector.addItem("Nmap")
        self.tool_selector.addItem("SQLMap")
        self.tool_selector.addItem("WPScan")
        self.tool_selector.addItem("Gobuster")
        self.tool_selector.addItem("Nikto")
        layout.addWidget(self.tool_selector)

        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        layout.addWidget(self.output_display)

        run_btn = QPushButton("Exécuter l'outil sélectionné")
        run_btn.clicked.connect(self.run_selected_tool)
        layout.addWidget(run_btn)

        report_btn = QPushButton("Générer le rapport final")
        report_btn.clicked.connect(self.show_report)
        layout.addWidget(report_btn)

        self.setLayout(layout)

    def run_selected_tool(self):
        ip = self.ip_input.text()
        url = self.url_input.text()
        tool = self.tool_selector.currentText()

        if not ip or not url:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer l'IP et l'URL cibles.")
            return

        commands = {
            "Nmap": (f"nmap -sP {ip}", "nmap.txt"),
            "SQLMap": (f"sqlmap -u {url} --batch", "sqlmap.txt"),
            "WPScan": (f"wpscan --url {url}", "wpscan.txt"),
            "Gobuster": (f"gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt", "gobuster.txt"),
            "Nikto": (f"nikto -h {url}", "nikto.txt"),
        }

        cmd, outfile = commands[tool]
        result = run_tool(cmd, outfile)
        self.output_display.append(result)

    def show_report(self):
        path = generate_report()
        QMessageBox.information(self, "Rapport généré", f"Rapport enregistré dans {path}")

def display_cli():
    print("===== Bienvenue dans la CyberSecurity Toolbox (CLI) =====")
    ip = input("Entrez l'adresse IP cible : ")
    url = input("Entrez l'URL cible : ")

    tools = {
        "1": ("Nmap", f"nmap -sP {ip}", "nmap.txt"),
        "2": ("SQLMap", f"sqlmap -u {url} --batch", "sqlmap.txt"),
        "3": ("WPScan", f"wpscan --url {url}", "wpscan.txt"),
        "4": ("Gobuster", f"gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt", "gobuster.txt"),
        "5": ("Nikto", f"nikto -h {url}", "nikto.txt"),
    }

    while True:
        print("\n--- Menu CLI ---")
        print("1. Nmap")
        print("2. SQLMap")
        print("3. WPScan")
        print("4. Gobuster")
        print("5. Nikto")
        print("6. Générer le rapport")
        print("7. Quitter")
        choice = input("Votre choix : ")

        if choice in tools:
            name, cmd, outfile = tools[choice]
            print(f"\n➡️  Lancement de {name}...")
            print(run_tool(cmd, outfile))
        elif choice == "6":
            path = generate_report()
            print(f"📄 Rapport généré : {path}")
        elif choice == "7":
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide. Veuillez réessayer.")

if __name__ == '__main__':
    print("===== CyberSecurity Toolbox =====")
    print("1. Interface Graphique (GUI)")
    print("2. Interface en Ligne de Commande (CLI)")
    mode = input("Choisissez le mode (1 ou 2) : ")

    if mode == "1":
        app = QApplication(sys.argv)
        window = ToolboxApp()
        window.show()
        sys.exit(app.exec_())
    elif mode == "2":
        display_cli()
    else:
        print("❌ Choix invalide. Relancez le programme.")
