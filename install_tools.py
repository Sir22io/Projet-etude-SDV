import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
import platform

# Création du dossier tools s'il n'existe pas
TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')
os.makedirs(TOOLS_DIR, exist_ok=True)

def is_windows():
    return platform.system().lower() == 'windows'

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Erreur lors de l'exécution de la commande: {command}")
        return False

def download_file(url, filename):
    try:
        print(f"Téléchargement de {filename}...")
        urllib.request.urlretrieve(url, filename)
        return True
    except Exception as e:
        print(f"Erreur lors du téléchargement de {filename}: {e}")
        return False

def install_nmap():
    if is_windows():
        nmap_url = "https://nmap.org/dist/nmap-7.94-setup.exe"
        nmap_installer = os.path.join(TOOLS_DIR, "nmap-setup.exe")
        if download_file(nmap_url, nmap_installer):
            print("Installation de Nmap...")
            run_command(nmap_installer)
    else:
        run_command("apt-get install -y nmap")

def install_sqlmap():
    print("Installation de SQLMap...")
    run_command("pip install sqlmap")

def install_wpscan():
    if is_windows():
        print("Installation de Ruby (nécessaire pour WPScan)...")
        ruby_url = "https://github.com/oneclick/rubyinstaller2/releases/download/RubyInstaller-3.0.3-1/rubyinstaller-3.0.3-1-x64.exe"
        ruby_installer = os.path.join(TOOLS_DIR, "ruby-setup.exe")
        if download_file(ruby_url, ruby_installer):
            run_command(ruby_installer)
            run_command("gem install wpscan")
    else:
        run_command("gem install wpscan")

def install_gobuster():
    if is_windows():
        gobuster_url = "https://github.com/OJ/gobuster/releases/latest/download/gobuster-windows-amd64.7z"
        gobuster_zip = os.path.join(TOOLS_DIR, "gobuster.7z")
        if download_file(gobuster_url, gobuster_zip):
            run_command(f"7z x {gobuster_zip} -o{TOOLS_DIR}")
    else:
        run_command("go get github.com/OJ/gobuster")

def install_nikto():
    if is_windows():
        nikto_url = "https://github.com/sullo/nikto/archive/master.zip"
        nikto_zip = os.path.join(TOOLS_DIR, "nikto.zip")
        if download_file(nikto_url, nikto_zip):
            with zipfile.ZipFile(nikto_zip, 'r') as zip_ref:
                zip_ref.extractall(TOOLS_DIR)
    else:
        run_command("apt-get install -y nikto")

def install_hydra():
    if is_windows():
        hydra_url = "https://github.com/vanhauser-thc/thc-hydra/archive/master.zip"
        hydra_zip = os.path.join(TOOLS_DIR, "hydra.zip")
        if download_file(hydra_url, hydra_zip):
            with zipfile.ZipFile(hydra_zip, 'r') as zip_ref:
                zip_ref.extractall(TOOLS_DIR)
    else:
        run_command("apt-get install -y hydra")

def install_dirbuster():
    dirbuster_url = "https://sourceforge.net/projects/dirbuster/files/latest/download"
    dirbuster_jar = os.path.join(TOOLS_DIR, "dirbuster.jar")
    download_file(dirbuster_url, dirbuster_jar)

def install_metasploit():
    if is_windows():
        metasploit_url = "https://windows.metasploit.com/metasploitframework-latest.msi"
        metasploit_installer = os.path.join(TOOLS_DIR, "metasploit-setup.msi")
        if download_file(metasploit_url, metasploit_installer):
            run_command(f"msiexec /i {metasploit_installer} /quiet")
    else:
        run_command("curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall")
        run_command("chmod +x msfinstall")
        run_command("./msfinstall")

def install_shodan():
    print("Installation de Shodan...")
    run_command("pip install shodan")

def install_burpsuite():
    burp_url = "https://portswigger.net/burp/releases/download?product=community&version=latest&type=jar"
    burp_jar = os.path.join(TOOLS_DIR, "burpsuite_community.jar")
    download_file(burp_url, burp_jar)

def install_john():
    if is_windows():
        john_url = "https://www.openwall.com/john/k/john-1.9.0-jumbo-1-win64.zip"
        john_zip = os.path.join(TOOLS_DIR, "john.zip")
        if download_file(john_url, john_zip):
            with zipfile.ZipFile(john_zip, 'r') as zip_ref:
                zip_ref.extractall(TOOLS_DIR)
    else:
        run_command("apt-get install -y john")

def install_aircrack():
    if is_windows():
        aircrack_url = "https://download.aircrack-ng.org/aircrack-ng-1.7-win.zip"
        aircrack_zip = os.path.join(TOOLS_DIR, "aircrack.zip")
        if download_file(aircrack_zip, aircrack_zip):
            with zipfile.ZipFile(aircrack_zip, 'r') as zip_ref:
                zip_ref.extractall(TOOLS_DIR)
    else:
        run_command("apt-get install -y aircrack-ng")

def create_requirements():
    with open('requirements.txt', 'w') as f:
        f.write("""flask==2.0.1
flask-bootstrap==3.3.7.1
flask-sqlalchemy==2.5.1
flask-admin==1.5.8
cryptography==3.4.7
pdfkit==1.0.0
sqlmap==1.5.2
shodan==1.25.0
""")

def main():
    print("Installation des outils de sécurité...")
    
    # Création du fichier requirements.txt
    create_requirements()
    
    # Installation des dépendances Python
    print("Installation des dépendances Python...")
    run_command("pip install -r requirements.txt")
    
    # Installation de chaque outil
    tools = [
        ("Nmap", install_nmap),
        ("SQLMap", install_sqlmap),
        ("WPScan", install_wpscan),
        ("Gobuster", install_gobuster),
        ("Nikto", install_nikto),
        ("Hydra", install_hydra),
        ("DirBuster", install_dirbuster),
        ("Metasploit", install_metasploit),
        ("Shodan", install_shodan),
        ("Burp Suite", install_burpsuite),
        ("John The Ripper", install_john),
        ("Aircrack-ng", install_aircrack)
    ]
    
    for tool_name, install_func in tools:
        print(f"\nInstallation de {tool_name}...")
        try:
            install_func()
            print(f"✅ {tool_name} installé avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de l'installation de {tool_name}: {e}")
    
    print("\nInstallation terminée!")
    print("Vous pouvez maintenant lancer l'application avec 'python app.py'")

if __name__ == "__main__":
    main() 