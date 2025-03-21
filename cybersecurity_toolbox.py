
import os
import shutil
from datetime import datetime

RESULTS_DIR = "results"
LOG_FILE = "toolbox_log.txt"
REPORT_FILE = "final_report.txt"
os.makedirs(RESULTS_DIR, exist_ok=True)

def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

def cleanup_logs():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    if os.path.exists(REPORT_FILE):
        os.remove(REPORT_FILE)
    for file in os.listdir(RESULTS_DIR):
        file_path = os.path.join(RESULTS_DIR, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("🧹 Tous les anciens logs et fichiers de résultats ont été supprimés.")

def run_tool(command, output_file):
    result = os.system(f"{command} > {RESULTS_DIR}/{output_file} 2>&1")
    if result == 0:
        success_message = f"✅ Commande réussie : {command}. Résultat enregistré dans {RESULTS_DIR}/{output_file}"
        print(success_message)
        log_message(success_message)
        return True
    else:
        error_message = f"❌ Erreur lors de l'exécution : {command}. Voir {RESULTS_DIR}/{output_file} pour plus de détails."
        print(error_message)
        log_message(error_message)
        return False

def generate_report():
    with open(REPORT_FILE, "w") as report_file:
        with open(LOG_FILE, "r") as log_file:
            logs = log_file.read()
            report_file.write("====== Rapport Final de la CyberSecurity Toolbox ======

")
            report_file.write(logs)
            report_file.write("
====== Fin du Rapport ======
")
    print(f"
📄 Rapport final généré dans {REPORT_FILE}")

def show_logs():
    if os.path.exists(LOG_FILE):
        print("📖 Affichage des logs en direct :
")
        with open(LOG_FILE, "r") as log_file:
            print(log_file.read())
    else:
        print("Aucun log disponible.")

def get_tool_options(tool_name):
    options = input(f"Voulez-vous ajouter des options spécifiques pour {tool_name}? (Laissez vide pour continuer) : ")
    return options.strip()

# --- Offensive Tools ---
def offensive_tools(target_ip, target_url):
    tools = [
        ("Commix", f"commix -u {target_url}", "commix.txt", "Outil d'injection de commandes basé sur une URL."),
        ("SQLMap", f"sqlmap -u {target_url} --batch", "sqlmap.txt", "Outil automatisé de détection et exploitation d'injections SQL."),
        ("WPScan", f"wpscan --url {target_url}", "wpscan.txt", "Scanner WordPress pour trouver des vulnérabilités."),
        ("Masscan", f"masscan -p1-65535 {target_ip} --rate=1000", "masscan.txt", "Scanner réseau très rapide pour identifier des ports ouverts."),
        ("Nikto", f"nikto -h {target_url}", "nikto.txt", "Scanner de vulnérabilités d'applications Web."),
        ("Gobuster", f"gobuster dir -u {target_url} -w /usr/share/wordlists/dirb/common.txt", "gobuster.txt", "Scanner de répertoires et fichiers cachés."),
        ("Arachni", f"arachni {target_url}", "arachni.txt", "Scanner de vulnérabilités d'applications web."),
        ("Fimap", f"fimap -u {target_url}", "fimap.txt", "Scanner d'inclusions de fichiers locaux (LFI)."),
        ("Clusterd", f"clusterd -i {target_ip}", "clusterd.txt", "Outil d'attaque automatisé contre les serveurs d'applications.")
    ]
    return tools

# --- Defensive Tools ---
def defensive_tools():
    tools = [
        ("Snort", "snort -c /etc/snort/snort.conf", "snort.txt", "Système de détection d'intrusion en réseau (IDS)."),
        ("Suricata", "suricata -c /etc/suricata/suricata.yaml", "suricata.txt", "Moteur IDS/IPS open-source de détection d'intrusion."),
        ("OpenVAS", "gvm-start", "openvas.txt", "Scanner de vulnérabilités complet et avancé."),
        ("Binwalk", "binwalk -e firmware.bin", "binwalk.txt", "Outil d'analyse de firmware pour extraire des fichiers cachés."),
        ("Rkhunter", "rkhunter --checkall", "rkhunter.txt", "Détection de rootkits sur un système Linux."),
        ("Chkrootkit", "chkrootkit", "chkrootkit.txt", "Scanner de rootkits pour Linux."),
        ("Iptables", "sudo iptables -L", "firewall.txt", "Pare-feu intégré à Linux pour gérer les paquets réseau."),
        ("Log Analysis", "tail -n 50 /var/log/syslog", "log_analysis.txt", "Analyse des logs système.")
    ]
    return tools

def run_tools(tools):
    for index, (name, command, output, description) in enumerate(tools, start=1):
        print(f"{index}. {name} - {description}")
    choice = input("
Sélectionnez un outil à exécuter (ou 'a' pour tous, 'l' pour logs, 'q' pour quitter) : ")
    
    if choice.lower() == 'a':
        for name, command, output, _ in tools:
            options = get_tool_options(name)
            run_tool(f"{command} {options}", output)
    elif choice.lower() == 'l':
        show_logs()
    elif choice.lower() == 'q':
        return
    else:
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(tools):
                name, command, output, _ = tools[choice_index]
                options = get_tool_options(name)
                run_tool(f"{command} {options}", output)
            else:
                print("Choix invalide. Veuillez réessayer.")
        except ValueError:
            print("Choix invalide. Veuillez entrer un numéro.")

if __name__ == "__main__":
    cleanup_logs()
    print("===== DÉMARRAGE DE LA CYBERSECURITY TOOLBOX =====")
    target_ip = input("Entrez l'adresse IP cible (ex: 127.0.0.1) : ")
    target_url = input("Entrez l'URL cible (ex: http://testphp.vulnweb.com) : ")

    while True:
        print("\nMenu principal :")
        print("1. Lancer les outils offensifs")
        print("2. Lancer les outils défensifs")
        print("3. Générer un rapport final")
        print("4. Afficher les logs")
        print("5. Quitter")

        choice = input("Votre choix : ")
        if choice == "1":
            tools = offensive_tools(target_ip, target_url)
            run_tools(tools)
        elif choice == "2":
            tools = defensive_tools()
            run_tools(tools)
        elif choice == "3":
            generate_report()
        elif choice == "4":
            show_logs()
        elif choice == "5":
            print("Fermeture de la CyberSecurity Toolbox. À bientôt !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")
