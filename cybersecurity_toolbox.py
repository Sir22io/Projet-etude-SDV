import os
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QMessageBox, QComboBox)
import sys
from cryptography.fernet import Fernet

RESULTS_DIR = "results"
LOG_FILE = "toolbox_log.txt"
REPORT_FILE = "final_report.txt"
KEY_FILE = "toolbox.key"

os.makedirs(RESULTS_DIR, exist_ok=True)

# =========================== CHIFFREMENT ===========================
def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)

def load_key():
    return open(KEY_FILE, "rb").read()

def encrypt_file(filepath):
    key = load_key()
    fernet = Fernet(key)
    with open(filepath, "rb") as file:
        data = file.read()
    encrypted = fernet.encrypt(data)
    with open(filepath, "wb") as file:
        file.write(encrypted)

def decrypt_file(filepath):
    key = load_key()
    fernet = Fernet(key)
    with open(filepath, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data.decode('utf-8')

# =========================== LOGGING & RAPPORT ===========================
def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")
    encrypt_file(LOG_FILE)

def run_tool(command, output_file):
    full_path = os.path.join(RESULTS_DIR, output_file)
    result = os.system(f"{command} > {full_path} 2>&1")
    if result == 0:
        msg = f"✅ Commande OK : {command}. Résultat dans {output_file}"
        log_message(msg)
        encrypt_file(full_path)
        return msg
    else:
        msg = f"❌ Échec commande : {command}. Voir {output_file}"
        log_message(msg)
        encrypt_file(full_path)
        return msg

def generate_report():
    if os.path.exists(LOG_FILE):
        log_content = decrypt_file(LOG_FILE)
        with open(REPORT_FILE, "w") as report_file:
            report_file.write("====== Rapport Final de la CyberSecurity Toolbox ======\n\n")
            report_file.write(log_content)
            report_file.write("\n====== Fin du Rapport ======\n")
        encrypt_file(REPORT_FILE)
    return REPORT_FILE

# =========================== INTERFACE ===========================
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

if __name__ == '__main__':
    generate_key()
    app = QApplication(sys.argv)
    window = ToolboxApp()
    window.show()
    sys.exit(app.exec_())
