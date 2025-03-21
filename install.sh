
#!/bin/bash
echo "Starting installation of required tools..."

# Update and install packages
sudo apt-get update
sudo apt-get install -y python3 python3-pip masscan nikto gobuster nmap commix

# Install SQLMap
if ! command -v sqlmap &> /dev/null
then
    echo "Installing SQLMap..."
    sudo apt-get install -y sqlmap
fi

# Install WPScan (via Ruby)
if ! command -v wpscan &> /dev/null
then
    echo "Installing WPScan..."
    sudo apt-get install ruby-full
    sudo gem install wpscan
fi

# Install other Python dependencies
pip3 install -r requirements.txt

echo "Installation completed successfully!"
