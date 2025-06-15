from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
import ssl # Décommenté pour activer HTTPS
import os
import subprocess
import markdown
import csv
from io import StringIO, BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import json
from cryptography.fernet import Fernet
import base64

# Génération de la clé Fernet (À FAIRE EN PRODUCTION : Stocker cette clé de manière sécurisée, ex: variable d'environnement)
# Pour le développement, vous pouvez la générer une fois et la copier.
# key = Fernet.generate_key()
# print(f"Clé Fernet générée (à stocker dans une variable d'environnement par exemple): {key.decode()}")

# Utiliser une clé d'environnement ou une clé par défaut pour le développement
FERNET_KEY = os.getenv('FERNET_KEY', 'mXaxMycy8caNylQ_hA_IbLW51L24op6w_aVMQyNvSIE=').encode() # Remplacez par une vraie clé en prod
# Assurez-vous que la clé est de la bonne longueur (32 URL-safe base64-encoded bytes)
if len(FERNET_KEY) != 44 or not FERNET_KEY.endswith(b'='):
    raise ValueError("FERNET_KEY doit être une clé Fernet valide de 32 URL-safe base64-encoded bytes.")

cipher_suite = Fernet(FERNET_KEY)

app = Flask(__name__)
app.secret_key = os.urandom(24) # Set a secret key for sessions

SCAN_HISTORY_FILE = os.path.join(app.root_path, 'data', 'scan_history.json')

# Dummy user for demonstration
USERS = {
    "admin": "admin"
}

def login_required(f):
    """
    Decorator to check if user is logged in.
    """
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Veuillez vous connecter pour accéder à cette page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def load_scan_history():
    if os.path.exists(SCAN_HISTORY_FILE):
        try:
            with open(SCAN_HISTORY_FILE, 'rb') as f:
                encrypted_data = f.read()
                if encrypted_data:
                    decrypted_data = cipher_suite.decrypt(encrypted_data)
                    return json.loads(decrypted_data.decode('utf-8'))
        except Exception as e:
            print(f"Erreur lors du déchiffrement ou du chargement de l'historique des scans: {e}")
            # En cas d'erreur (ex: clé incorrecte, données corrompues), on retourne un historique vide
    return []

def save_scan_history(history):
    try:
        json_data = json.dumps(history, indent=4).encode('utf-8')
        encrypted_data = cipher_suite.encrypt(json_data)
        with open(SCAN_HISTORY_FILE, 'wb') as f:
            f.write(encrypted_data)
    except Exception as e:
        print(f"Erreur lors du chiffrement ou de la sauvegarde de l'historique des scans: {e}")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            flash('Connexion réussie!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Identifiant ou mot de passe incorrect.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('login'))

@app.route('/execute_tool', methods=['POST'])
@login_required
def execute_tool():
    tool_name = request.form['tool_name']
    result_text = ""
    success = False
    message = ""

    try:
        if tool_name == 'nmap':
            target = request.form['target']
            command = ['nmap', target]
            process = subprocess.run(command, capture_output=True, text=True, check=True)
            result_text = process.stdout
            success = True
            message = f'Nmap a été exécuté avec succès sur {target}.'
        elif tool_name == 'metasploit':
            command_str = request.form['command']
            result_text = f"""Simulation de l'exécution Metasploit avec la commande: {command_str}

Le Framework Metasploit est un outil puissant pour les tests d'intrusion. Voici un exemple de sortie simulée:
[*] Using MSF_LOCAL_IP as 127.0.0.1
[*] Starting the payload handler...
[*] Started reverse TCP handler on 127.0.0.1:4444
[*] Sending stage (206403 bytes) to 127.0.0.1
[*] Meterpreter session 1 opened (127.0.0.1:4444 -> 127.0.0.1:1234) at 2025-06-12 10:00:00 UTC

meterpreter > sysinfo
Computer        : TARGET-PC
OS              : Windows 7 (Build 7601, Service Pack 1).
Architecture    : x64
System Language : en_US
Meterpreter     : x64/windows
"""
            success = True
            message = 'Simulation Metasploit exécutée avec des détails améliorés.'
        elif tool_name == 'wireshark':
            interface = request.form['interface']
            duration = request.form['duration']
            result_text = f"""Simulation de capture Wireshark sur {interface} pendant {duration} secondes.

Voici un exemple de trafic réseau simulé capturé par Wireshark:
1   0.000000 192.168.1.100 -> 192.168.1.1  HTTP 100 GET /index.html
2   0.000120 192.168.1.1   -> 192.168.1.100 HTTP 200 OK (text/html)
3   0.000500 192.168.1.100 -> 8.8.8.8      DNS 70 Standard query A www.google.com
4   0.000700 8.8.8.8       -> 192.168.1.100 DNS 86 Standard query response A 142.250.187.164
5   0.001200 192.168.1.100 -> 142.250.187.164 TCP 60 49152 > 80 [SYN] Seq=0 Win=64240 Len=0 MSS=1460 SACK_PERM=1 TSval=12345 TSecr=0 WS=256
... (plus de paquets simulés)
"""
            success = True
            message = 'Simulation Wireshark exécutée avec des détails améliorés.'
        elif tool_name == 'owasp_zap':
            target = request.form['target']
            result_text = f"""Simulation de scan OWASP ZAP sur: {target}

Rapport de scan ZAP simulé:
Vulnérabilités trouvées:
- Alerte: Cross-Site Scripting (XSS) (High)
  Description: XSS détecté dans le paramètre 'search' sur la page /search.html
  Solution: Valider et encoder toutes les entrées utilisateur avant de les afficher.
- Alerte: SQL Injection (Medium)
  Description: Potentielle injection SQL sur le paramètre 'id' sur /products.php
  Solution: Utiliser des requêtes préparées ou des ORM pour toutes les interactions avec la base de données.
- Alerte: Missing Security Headers (Low)
  Description: Les en-têtes de sécurité HSTS, X-Frame-Options, X-Content-Type-Options sont manquants.
  Solution: Configurer le serveur web pour inclure les en-têtes de sécurité recommandés.
"""
            success = True
            message = 'Simulation OWASP ZAP exécutée avec des détails améliorés.'
        elif tool_name == 'burp_suite':
            target = request.form['target']
            result_text = f"""Simulation de scan Burp Suite sur: {target}

Rapport de scan Burp Suite simulé:
Scan terminé. Résumé des vulnérabilités:
- High: 1 (Ex: Injection SQL)
- Medium: 2 (Ex: XSS réfléchi, Session fixation)
- Low: 3 (Ex: Content spoofing, Cookie sans HttpOnly)

Détails:
1. Injection SQL:
   URL: {target}/api/products?id=1'
   Payload: ' OR 1=1--
   Gravité: High
   Recommandation: Utiliser des requêtes préparées.

2. Cross-Site Scripting (Reflected):
   URL: {target}/search?query=<script>alert(1)</script>
   Gravité: Medium
   Recommandation: Encoder les sorties.
"""
            success = True
            message = 'Simulation Burp Suite exécutée avec des détails améliorés.'
        elif tool_name == 'postman':
            collection = request.form['collection']
            result_text = f"""Simulation d'exécution Postman Collection: {collection}

Résultat de l'exécution de la collection Postman via Newman (simulate):
  ✔ Mon API Test Collection
    ✔ Authentification
      ✔ Statut 200 pour le login
      ✔ Récupération du jeton JWT
    ✔ Utilisateurs
      ✔ Obtenir tous les utilisateurs (Statut 200)
      ✔ Créer un nouvel utilisateur (Statut 201)
      ✖ Mettre à jour l'utilisateur existant (Échec: Validation des données)
        - Échec de l'assertion: "Status code is 200"
"""
            success = True
            message = 'Simulation Postman exécutée avec des détails améliorés.'
        elif tool_name == 'sqlmap':
            target = request.form['target']
            result_text = f"""Simulation d'exécution SQLmap sur: {target}

Résultat simulé de SQLmap:
[*] checking if the target is stable
[*] checking for GET parameter '#1' in GET
    (custom) parameter 'id' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 1 HTTP(s) request(s):
---
Parameter: id (GET)
    Type: error-based
    Title: MySQL >= 5.0 AND error-based - Parameter replace (DUAL table)
    Payload: id=1' AND (SELECT 9999 FROM(SELECT COUNT(*),CONCAT(0x717a787171,(SELECT (ELT(9999=9999,1))),0x7176707171,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a) AND 'XfXk'='XfXk'
---
[SUCCESS] the GET parameter 'id' is vulnerable!
"""
            success = True
            message = 'Simulation SQLmap exécutée avec des détails améliorés.'
        elif tool_name == 'dependency_check':
            path = request.form['path']
            result_text = f"""Simulation d'analyse Dependency-Check sur: {path}

Rapport simulé d'OWASP Dependency-Check:
[INFO] CVE-2019-17571: Apache Log4j Deserialization of Untrusted Data
   Description: Apache Log4j 1.x is vulnerable to deserialization of untrusted data when the attacker has write access to the Log4j configuration.
   CPE: cpe:/a:apache:log4j:1.2.17
   Severity: High
   Solution: Upgrade to Log4j 2.x or later.

[INFO] CVE-2014-0050: Jackson Databind Deserialization Vulnerability
   Description: The FasterXML jackson-databind library before 2.2.3, 2.3.x before 2.3.2, and 2.4.x before 2.4.0 does not disable the enableDefaultTyping feature, which allows remote attackers to execute arbitrary code via a crafted JSON string that is deserialized.
   CPE: cpe:/a:fasterxml:jackson-databind:2.2.2
   Severity: High
   Solution: Upgrade to a patched version or disable default typing.

[INFO] Aucune autre vulnérabilité critique détectée pour les dépendances analysées.
"""
            success = True
            message = 'Simulation Dependency-Check exécutée avec des détails améliorés.'
        elif tool_name == 'nessus':
            target = request.form['target']
            result_text = f"""Simulation de scan Nessus sur: {target}

Rapport de scan Nessus simulé:
Hôte: {target}
Vulnérabilités critiques:
- Plugin ID: 10863
  Nom: Web Server Common Files Disclosure
  Gravité: Critical
  Description: Des fichiers de configuration ou de logs sensibles sont accessibles via le serveur web.
  Solution: Restreindre l'accès aux fichiers et répertoires sensibles.
"""
            success = True
            message = 'Simulation Nessus exécutée avec des détails améliorés.'
        elif tool_name == 'acunetix':
            target = request.form['target']
            result_text = f"""Simulation de scan Acunetix sur: {target}

Rapport de scan Acunetix simulé:
Scan Status: Completed
High Vulnerabilities:
- Vulnerability: SQL Injection
  Target: {target}/products?id=1
  Description: SQL Injection vulnerability detected in 'id' parameter.
  Solution: Use parameterized queries.

Medium Vulnerabilities:
- Vulnerability: Cross-Site Scripting (XSS)
  Target: {target}/search?q=test
  Description: Reflected XSS detected.
  Solution: Sanitize user input.

Low Vulnerabilities:
- Vulnerability: Missing HTTP Security Headers
  Target: {target}
  Description: Several security headers are missing (e.g., Strict-Transport-Security, X-Frame-Options).
  Solution: Configure your web server to include recommended security headers.
"""
            success = True
            message = 'Simulation Acunetix exécutée avec des détails améliorés.'
        elif tool_name == 'aircrack_ng':
            interface = request.form['interface']
            result_text = f"""Simulation Aircrack-ng sur interface: {interface}

Résultat simulé d'Aircrack-ng (capture et analyse WPA/WPA2):
CH  BW  N° ESSID               BSSID              PWR  BEACONS  #DATA, #/s  CH  MB   ENC  CIPHER AUTH  ESSID
1   20  2  MyWirelessNetwork    00:11:22:33:44:55  -45  12345    123456, 1234  1   54e  WPA2 CCMP  PSK   MyWirelessNetwork

Captured handshake: 00:11:22:33:44:55 (MyWirelessNetwork)

Crackage du handshake WPA (utilisant une liste de mots):
[0:00:00] 100/1000 mots par seconde
[0:00:05] Mot de passe trouvé: "SuperSecretPass"
"""
            success = True
            message = 'Simulation Aircrack-ng exécutée avec des détails améliorés.'
        elif tool_name == 'nikto':
            target = request.form['target']
            result_text = f"""Simulation de scan Nikto sur: {target}

Résultat simulé de Nikto:
- Configuration d'Apache/2.4.6 (CentOS) par défaut trouvée.
- Le chemin '/.git/' a été découvert. Ceci est potentiellement une fuite d'informations.
- La version de PHP '5.3.3' est obsolète et contient des vulnérabilités connues.
- Une page d'administration par défaut '/admin/' a été trouvée.
+ URL: {target}/phpinfo.php - La page phpinfo() a été trouvée.
+ HTTP Server: Apache/2.4.6 (CentOS)
+ OSVDB-ID: 3092: /manual/: Répertoire de documentation Apache trouvé.
+ OSVDB-ID: 3233: /icons/: Répertoire d'icônes Apache trouvé.
"""
            success = True
            message = 'Simulation Nikto exécutée avec des détails améliorés.'
        elif tool_name == 'sslyze':
            target = request.form['target']
            result_text = f"""Simulation d'analyse SSLyze sur: {target}

Résultat simulé de SSLyze:
SCAN RESULTS FOR {target}
  * Certificate Information
    - Issuer: Let's Encrypt
    - Not Before: 2025-01-01
    - Not After: 2025-03-31
    - Common Name: {target}
    - SANs: {target}, www.{target}
  * TLS 1.3: Supported
  * TLS 1.2: Supported
    - Weak Cipher Suites: None
    - Strong Cipher Suites: TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (0xc030)
  * TLS 1.1: Not Supported (Good)
  * TLS 1.0: Not Supported (Good)
  * SSL 3.0: Not Supported (Good)
  * SSL 2.0: Not Supported (Good)

  * Heartbleed: NOT VULNERABLE
  * CCS Injection: NOT VULNERABLE
  * ROBOT: NOT VULNERABLE
"""
            success = True
            message = 'Simulation SSLyze exécutée avec des détails améliorés.'
        elif tool_name == 'ettercap':
            interface = request.form['interface']
            result_text = f"""Simulation Ettercap sur interface: {interface}

Résultat simulé d'Ettercap (exemple d'attaque MITM DNS spoofing):
ettercap NG-0.7.3-alpha  -- unified package
Listening on {interface}
Privileges acquired: root
7 plugins loaded.
DNS spoofing enabled.
ARP poisoning targets:
  - 192.168.1.1 (Gateway)
  - 192.168.1.100 (Victim)
Spoofing ARP replies...
Caught DNS request for 'www.google.com' from 192.168.1.100.
Spoofing DNS reply for 'www.google.com' to 192.168.1.100 with IP 1.2.3.4 (simulated attacker's server).
"""
            success = True
            message = 'Simulation Ettercap exécutée avec des détails améliorés.'
        elif tool_name == 'maltego':
            target = request.form['target']
            result_text = f"""Simulation Maltego sur entité: {target}

Résultat simulé de Maltego:
Entité centrale: {target} (Domaine)
Relations découvertes:
- Domaine {target} est lié à Adresse IP: 203.0.113.45
- Adresse IP 203.0.113.45 est liée à Hôte: webserver.example.com
- Hôte webserver.example.com est lié à MX Record: mail.example.com
- Domaine {target} est lié à Personne: John Doe (email: john.doe@{target})
- Personne John Doe est liée à Numéro de téléphone: +1-555-123-4567
"""
            success = True
            message = 'Simulation Maltego exécutée avec des détails améliorés.'
        elif tool_name == 'john_the_ripper':
            file_path = request.form['file']
            result_text = f"""Simulation John the Ripper sur fichier: {file_path}

Résultat simulé de John the Ripper (craquage de mots de passe):
Using default input encoding: UTF-8
Loaded 10 password hashes with no different salts to test (./{file_path})
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Warning: detected hash type "sha512crypt", but the string is also recognized as "crypt".
Optimal kernel parameters for your GPU were not found.
0g 0:00:00:00 DONE (2025-06-12 10:30) 2.000g/s 64000p/s 64000c/s 64000C/s user1:password123 user2:testpass
Session completed.
"""
            success = True
            message = 'Simulation John the Ripper exécutée avec des détails améliorés.'
        elif tool_name == 'hydra':
            target = request.form['target']
            protocol = request.form['protocol']
            wordlist = request.form['wordlist']
            result_text = f"""Simulation d'exécution Hydra sur {target} avec protocole {protocol} et liste de mots {wordlist}

Résultat simulé de Hydra:
Hydra v9.0 (c) 2024 by van Hauser / THC & David Maciejak -  http://www.thc.org/thc-hydra/
[DATA] max 16 tasks per server, 4 parallel targets, 16 tries per password, 32 parallel attacks (job 0)
[DATA] attacking service {protocol}://{target}
[STATUS] 1.00% (8/800) done, 0:00:01 remaining, 8 tries a second
[STATUS] 2.00% (16/800) done, 0:00:01 remaining, 8 tries a second
...
[800] [SUCCESS] host: {target}  login: admin  password: {password_found_simulated}
1 of 1 target successfully completed, 1 of 1 host completed.
Hydra finished at 2025-06-12 11:00:00
"""
            success = True
            message = 'Simulation Hydra exécutée avec des détails améliorés.'
        elif tool_name == 'nmap_nse':
            target = request.form['target']
            script = request.form['script']
            result_text = f"""Simulation Nmap NSE sur {target} avec script {script}

Résultat simulé de Nmap Scripting Engine:
Starting Nmap 7.80 ( https://nmap.org ) at 2025-06-12 10:45 UTC
Nmap scan report for {target}
Host is up (0.0001s latency).

PORT   STATE SERVICE
80/tcp open  http
| http-enum: 
|   /admin/: Administration interface.
|   /phpinfo.php: PHP information disclosure.
|   /robots.txt: Disallows /private.
|_  /sitemap.xml: Found sitemap.

Nmap done: 1 IP address (1 host up) scanned in 0.50 seconds
"""
            success = True
            message = 'Simulation Nmap NSE exécutée avec des détails améliorés.'
        else:
            message = "Outil non reconnu."

        if success:
            # Record scan history
            scan_history = load_scan_history()
            scan_entry = {
                'tool_name': tool_name,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'target': request.form.get('target', 'N/A'),
                'message': message
            }
            scan_history.append(scan_entry)
            try:
                save_scan_history(scan_history)
            except PermissionError:
                flash("L'historique des scans n'a pas pu être enregistré en raison de problèmes de permissions sur '/app/data/scan_history.json'. Veuillez vérifier les permissions du répertoire.", 'warning')
            except Exception as e:
                flash(f"Une erreur inattendue est survenue lors de la tentative d'enregistrement de l'historique des scans: {e}", 'warning')
            
            # The success message for the tool itself is handled by the final flash statement

        else:
            flash(message, 'danger')

    except subprocess.CalledProcessError as e:
        result_text = e.stderr or e.stdout
        message = f'Erreur lors de l\'exécution de {tool_name}: {result_text}'
        success = False
    except FileNotFoundError:
        message = f'L\'outil {tool_name} n\'est pas trouvé dans le conteneur. Veuillez vérifier votre Dockerfile ou l\'installation de l\'outil.'
        success = False
    except Exception as e:
        message = f'Une erreur inattendue est survenue lors de l\'exécution de {tool_name}: {e}'
        success = False
    
    # Flash the message if there is one
    if message:
        flash(message, 'success' if success else 'danger')

    return jsonify({
        'success': success,
        'result': result_text,
        'message': message
    })

@app.route('/scan_history')
@login_required
def scan_history():
    history = load_scan_history()
    return render_template('scan_history.html', scan_history=history)

@app.route('/download_report/<tool_name>/<format>')
@login_required
def download_report(tool_name, format):
    report_filename_base = f'{tool_name}_report'
    report_path_txt = os.path.join('/app/reports', f'{report_filename_base}.txt')

    if not os.path.exists(report_path_txt):
        flash(f'Aucun rapport trouvé pour {tool_name}. Exécutez d\'abord l\'outil.', 'warning')
        return redirect(url_for('index'))

    with open(report_path_txt, 'r', encoding='utf-8') as f:
        raw_report_content = f.read()

    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if format == 'txt':
        return send_file(report_path_txt, as_attachment=True, download_name=f'{report_filename_base}.txt', mimetype='text/plain')
    elif format == 'html':
        html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Rapport {tool_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; white-space: pre-wrap; word-wrap: break-word; }}
        h1 {{ color: #0056b3; }}
        .report-meta {{ font-size: 0.9em; color: #666; margin-bottom: 10px; }}
        pre {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; border: 1px solid #dee2e6; }}
    </style>
</head>
<body>
    <h1>Rapport {tool_name}</h1>
    <div class="report-meta">Date et Heure d'exécution: {current_datetime}</div>
    <pre>{raw_report_content}</pre>
</body>
</html>
"""
        return send_file(BytesIO(html_content.encode('utf-8')), as_attachment=True, download_name=f'{report_filename_base}.html', mimetype='text/html')
    elif format == 'csv':
        csv_output_buffer = BytesIO()
        csv_in_memory = StringIO(newline='') # Create a StringIO object
        writer = csv.writer(csv_in_memory) # Pass it to csv.writer
        
        for line in raw_report_content.splitlines():
            writer.writerow(line.split())
        
        csv_in_memory.seek(0) # Rewind the StringIO buffer
        csv_data_bytes = csv_in_memory.getvalue().encode('utf-8') # Get string, then encode to bytes

        return send_file(BytesIO(csv_data_bytes), as_attachment=True, download_name=f'{report_filename_base}.csv', mimetype='text/csv')
    elif format == 'pdf':
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        c.drawString(100, 750, f"Rapport {tool_name}")
        c.drawString(100, 735, f"Date et Heure d'exécution: {current_datetime}")
        
        textobject = c.beginText()
        textobject.setTextOrigin(100, 700)
        textobject.setFont("Helvetica", 10)
        
        # Split raw_report_content into lines and add them to the PDF
        lines = raw_report_content.splitlines()
        y_position = 700
        for line in lines:
            if y_position < 50: # Check if close to bottom of page
                c.showPage()
                y_position = 750 # Reset y position for new page
                textobject = c.beginText() # New text object for new page
                textobject.setTextOrigin(100, y_position)
                textobject.setFont("Helvetica", 10)
            textobject.textLine(line)
            y_position -= 12 # Adjust for next line
        c.drawText(textobject)
        
        c.showPage()
        c.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f'{report_filename_base}.pdf', mimetype='application/pdf')
    else:
        flash('Format de rapport non pris en charge.', 'danger')
        return redirect(url_for('index'))

@app.route('/')
@login_required # Protect this route
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Démarrer l'application en mode HTTPS
    app.run(host='0.0.0.0', port=5000, ssl_context=('/usr/local/etc/ssl/cert.pem', '/usr/local/etc/ssl/key.pem'))