
import os
import shutil
from datetime import datetime

BASE_DIR = os.getcwd()
RESULTS_DIR = os.path.join(BASE_DIR, "results")
LOG_FILE = os.path.join(BASE_DIR, "toolbox_log.txt")
REPORT_FILE = os.path.join(BASE_DIR, "final_report.txt")
os.makedirs(RESULTS_DIR, exist_ok=True)

def get_current_time():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def create_timestamped_dir():
    timestamp = get_current_time()
    dir_path = os.path.join(RESULTS_DIR, f"Run_{timestamp}")
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

def cleanup_logs():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    if os.path.exists(REPORT_FILE):
        os.remove(REPORT_FILE)
    for folder in os.listdir(RESULTS_DIR):
        folder_path = os.path.join(RESULTS_DIR, folder)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
    print("🧹 Tous les anciens logs et fichiers de résultats ont été supprimés.")

def run_tool(command, output_file, show_output=True):
    result_dir = create_timestamped_dir()
    full_output_path = os.path.join(result_dir, output_file)
    
    if show_output:
        result = os.system(f"{command} | tee {full_output_path}")
    else:
        result = os.system(f"{command} > {full_output_path} 2>&1")

    if result == 0:
        success_message = f"✅ Commande réussie : {command}. Résultat enregistré dans {full_output_path}"
        print(success_message)
        log_message(success_message)
        return True
    else:
        error_message = f"❌ Erreur lors de l'exécution : {command}. Voir {full_output_path} pour plus de détails."
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

def search_logs(keyword):
    if not os.path.exists(LOG_FILE):
        print("Aucun log disponible pour la recherche.")
        return

    print(f"🔍 Recherche du mot-clé '{keyword}' dans les logs :
")
    with open(LOG_FILE, "r") as log_file:
        lines = log_file.readlines()
        results = [line for line in lines if keyword.lower() in line.lower()]
        
    if results:
        for result in results:
            print(result.strip())
    else:
        print("Aucun résultat trouvé pour ce mot-clé.")

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
        ("Gobuster", f"gobuster dir -u {target_url} -w /usr/share/wordlists/dirb/common.txt", "gobuster.txt", "Scanner de répertoires et fichiers cachés.")
    ]
    return tools

# --- Defensive Tools ---
def defensive_tools():
    tools = [
        ("Snort", "snort -c /etc/snort/snort.conf", "snort.txt", "Système de détection d'intrusion en réseau (IDS)."),
        ("Suricata", "suricata -c /etc/suricata/suricata.yaml", "suricata.txt", "Moteur IDS/IPS open-source de détection d'intrusion."),
        ("OpenVAS", "gvm-start", "openvas.txt", "Scanner de vulnérabilités complet et avancé."),
        ("Rkhunter", "rkhunter --checkall", "rkhunter.txt", "Détection de rootkits sur un système Linux."),
        ("Chkrootkit", "chkrootkit", "chkrootkit.txt", "Scanner de rootkits pour Linux."),
        ("Log Analysis", "tail -n 50 /var/log/syslog", "log_analysis.txt", "Analyse des logs système.")
    ]
    return tools

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
        print("4. Rechercher dans les logs")
        print("5. Quitter")

        choice = input("Votre choix : ")
        if choice == "1":
            tools = offensive_tools(target_ip, target_url)
            for name, command, output, description in tools:
                options = get_tool_options(name)
                run_tool(f"{command} {options}", output)
        elif choice == "2":
            tools = defensive_tools()
            for name, command, output, description in tools:
                options = get_tool_options(name)
                run_tool(f"{command} {options}", output)
        elif choice == "3":
            generate_report()
        elif choice == "4":
            keyword = input("Entrez le mot-clé à rechercher dans les logs : ")
            search_logs(keyword)
        elif choice == "5":
            print("Fermeture de la CyberSecurity Toolbox. À bientôt !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")
