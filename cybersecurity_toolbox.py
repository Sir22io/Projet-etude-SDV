import os
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QMessageBox, QComboBox, QFileDialog)
from jinja2 import Environment, FileSystemLoader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
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

def generate_txt_report():
    with open(REPORT_FILE, "w") as report_file:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as log_file:
                report_file.write("====== Rapport Final de la CyberSecurity Toolbox ======\n\n")
                report_file.write(log_file.read())
                report_file.write("\n====== Fin du Rapport ======\n")
    return REPORT_FILE

def generate_html_report(data, output_path="results/report_final.html"):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")
    html_content = template.render(data)
    with open(output_path, "w") as f:
        f.write(html_content)
    return output_path

def generate_pdf_report(data, output_path="results/report_final.pdf"):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.darkblue)
    c.drawString(50, height - 50, "🛡️ Rapport de Pentest - CyberSecurity Toolbox")

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.black)
    c.drawString(50, height - 100, f"📅 Date : {data.get('date')}")
    c.drawString(50, height - 120, f"🌐 IP cible : {data.get('ip')}")
    c.drawString(50, height - 140, f"🔗 URL cible : {data.get('url')}")

    c.drawString(50, height - 180, "🛠️ Outils exécutés :")
    y = height - 200
    for tool in data.get('tools', []):
        c.drawString(70, y, f"- {tool}")
        y -= 15

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "📄 Résultats & Logs :")
    c.setFont("Helvetica", 10)
    y -= 20

    lines = data.get('logs', "").splitlines()
    for line in lines:
        if y < 100:
            c.showPage()
            y = height - 50
        c.drawString(60, y, line[:100])
        y -= 12

    c.save()
    return output_path

# Interface PyQt5
class ToolboxApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CyberSecurity Toolbox - PyQt5")
        self.setGeometry(100, 100, 600, 400)
        self.selected_tools = []
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
        tools = ["Nmap", "SQLMap", "WPScan", "Gobuster", "Nikto"]
        self.tool_selector.addItems(tools)
        layout.addWidget(self.tool_selector)

        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        layout.addWidget(self.output_display)

        run_btn = QPushButton("Exécuter l'outil sélectionné")
        run_btn.clicked.connect(self.run_selected_tool)
        layout.addWidget(run_btn)

        export_btn_layout = QHBoxLayout()
        export_pdf = QPushButton("Exporter en PDF")
        export_pdf.clicked.connect(self.export_pdf)
        export_html = QPushButton("Exporter en HTML")
        export_html.clicked.connect(self.export_html)
        export_txt = QPushButton("Exporter en TXT")
        export_txt.clicked.connect(self.export_txt)

        export_btn_layout.addWidget(export_pdf)
        export_btn_layout.addWidget(export_html)
        export_btn_layout.addWidget(export_txt)

        layout.addLayout(export_btn_layout)
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
        if tool not in self.selected_tools:
            self.selected_tools.append(tool)

    def export_pdf(self):
        data = self.get_report_data()
        path = generate_pdf_report(data)
        QMessageBox.information(self, "Export PDF", f"Rapport PDF généré : {path}")

    def export_html(self):
        data = self.get_report_data()
        path = generate_html_report(data)
        QMessageBox.information(self, "Export HTML", f"Rapport HTML généré : {path}")

    def export_txt(self):
        path = generate_txt_report()
        QMessageBox.information(self, "Export TXT", f"Rapport texte généré : {path}")

    def get_report_data(self):
        return {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": self.ip_input.text(),
            "url": self.url_input.text(),
            "tools": self.selected_tools,
            "logs": open(LOG_FILE).read() if os.path.exists(LOG_FILE) else ""
        }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToolboxApp()
    window.show()
    sys.exit(app.exec_())
