# Check for Administrator privileges
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Ce script doit être exécuté en tant qu'administrateur. Veuillez faire un clic droit sur le fichier .ps1 et choisir 'Exécuter en tant qu'administrateur'." -ForegroundColor Red
    Start-Sleep -Seconds 5
    Exit 1
}

# Define the TOOLS_DIR relative to the script location (assuming script is placed in Projet-etude-SDV-main)
$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$TOOLS_DIR = Join-Path -Path $scriptDir -ChildPath "tools"

# Create TOOLS_DIR if it doesn't exist
if (-not (Test-Path $TOOLS_DIR)) {
    New-Item -ItemType Directory -Path $TOOLS_DIR -Force
}

Set-Location $TOOLS_DIR

Write-Host "Début de l'installation des prérequis et outils..." -ForegroundColor Green

# --- 7-Zip (pour Gobuster) ---
Write-Host "Installation de 7-Zip..." -ForegroundColor Cyan
$sevenZipUrl = "https://www.7-zip.org/a/7z2301-x64.exe"
$sevenZipInstaller = Join-Path -Path $TOOLS_DIR -ChildPath "7zip-setup.exe"
try {
    Invoke-WebRequest -Uri $sevenZipUrl -OutFile $sevenZipInstaller -UseBasicParsing
    Start-Process -FilePath $sevenZipInstaller -ArgumentList "/S" -Wait -NoNewWindow
    # Add 7-Zip to PATH (if not automatically added by installer)
    $sevenZipPath = "C:\Program Files\7-Zip\"
    if (-not ($env:Path -like "*$sevenZipPath*")) {
        $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$sevenZipPath", "Machine")
        Write-Host "Ajouté 7-Zip au PATH système." -ForegroundColor Green
    }
    Write-Host "7-Zip installé avec succès." -ForegroundColor Green
} catch {
    Write-Host "Erreur lors de l'installation de 7-Zip: $($_.Exception.Message)" -ForegroundColor Red
}

# --- Ruby (pour WPScan) ---
Write-Host "Installation de Ruby (avec MSYS2)..." -ForegroundColor Cyan
$rubyUrl = "https://github.com/oneclick/rubyinstaller2/releases/download/RubyInstaller-3.0.3-1/rubyinstaller-3.0.3-1-x64.exe"
$rubyInstaller = Join-Path -Path $TOOLS_DIR -ChildPath "ruby-setup.exe"
try {
    Invoke-WebRequest -Uri $rubyUrl -OutFile $rubyInstaller -UseBasicParsing
    Start-Process -FilePath $rubyInstaller -ArgumentList "/VERYSILENT /NORESTART /TASKS=""/RUBYANDMSYS2INSTALL"" /DIR=""C:\Ruby30""" -Wait -NoNewWindow
    Write-Host "Ruby installé avec succès. L'installation des dépendances MSYS2 a été tentée. Si WPScan ne fonctionne pas, vous devrez peut-être lancer 'ridk install' manuellement dans une invite de commande Ruby." -ForegroundColor Yellow
    # Add Ruby bin to current session's PATH for immediate use
    $env:Path = $env:Path + ";C:\Ruby30\bin"
} catch {
    Write-Host "Erreur lors de l'installation de Ruby: $($_.Exception.Message)" -ForegroundColor Red
}

# --- Perl (pour Nikto) ---
Write-Host "Installation de Perl (Strawberry Perl)..." -ForegroundColor Cyan
$perlUrl = "https://strawberryperl.com/download/5.32.1.1/strawberry-perl-5.32.1.1-64bit.msi"
$perlInstaller = Join-Path -Path $TOOLS_DIR -ChildPath "perl-setup.msi"
try {
    Invoke-WebRequest -Uri $perlUrl -OutFile $perlInstaller -UseBasicParsing
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i `"$perlInstaller`" /quiet /qn /norestart" -Wait -NoNewWindow
    Write-Host "Perl installé avec succès." -ForegroundColor Green
} catch {
    Write-Host "Erreur lors de l'installation de Perl: $($_.Exception.Message)" -ForegroundColor Red
}

# --- Java (pour DirBuster et Burp Suite) ---
Write-Host "Installation de Java (OpenJDK)..." -ForegroundColor Cyan
$javaUrl = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.10%2B7/OpenJDK17U-jdk_x64_windows_hotspot_17.0.10_7.msi"
$javaInstaller = Join-Path -Path $TOOLS_DIR -ChildPath "java-setup.msi"
try {
    Invoke-WebRequest -Uri $javaUrl -OutFile $javaInstaller -UseBasicParsing
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i `"$javaInstaller`" /quiet /qn /norestart" -Wait -NoNewWindow
    Write-Host "Java installé avec succès." -ForegroundColor Green
} catch {
    Write-Host "Erreur lors de l'installation de Java: $($_.Exception.Message)" -ForegroundColor Red
}

# --- Metasploit ---
Write-Host "Installation de Metasploit Framework (tentative d'installation silencieuse)..." -ForegroundColor Cyan
$metasploitUrl = "https://windows.metasploit.com/metasploitframework-latest.msi"
$metasploitInstaller = Join-Path -Path $TOOLS_DIR -ChildPath "metasploit-setup.msi"
try {
    Invoke-WebRequest -Uri $metasploitUrl -OutFile $metasploitInstaller -UseBasicParsing
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i `"$metasploitInstaller`" /quiet /qn /norestart" -Wait -NoNewWindow
    Write-Host "Installation de Metasploit terminée (vérifiez si elle a réussi. Une erreur 1603 signifie une défaillance de l'installation silencieuse)." -ForegroundColor Yellow
} catch {
    Write-Host "Erreur lors de l'installation de Metasploit: $($_.Exception.Message). Il se peut que vous deviez l'installer manuellement." -ForegroundColor Red
}

Write-Host "Nettoyage des fichiers d'installation..." -ForegroundColor Green
Get-ChildItem -Path $TOOLS_DIR -Include "*-setup.exe", "*-setup.msi", "*.zip", "*.7z" | Remove-Item -ErrorAction SilentlyContinue

Write-Host "Installation des prérequis terminée. Veuillez redémarrer l'application Flask et tester les outils." -ForegroundColor Green
Write-Host "Note importante: Pour Shodan, vous devrez toujours configurer votre clé API (shodan init YOUR_API_KEY) manuellement." -ForegroundColor Yellow
Write-Host "Note importante: Pour PostgreSQL, une installation manuelle est généralement requise en raison de sa complexité." -ForegroundColor Yellow
Write-Host "Note importante: Pour Gobuster, vous devrez fournir un 'common.txt' dans votre dossier 'tools' ou un chemin valide." -ForegroundColor Yellow 