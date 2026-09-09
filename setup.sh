#!/bin/bash

# Discode - Termux Discord Bot Manager Setup Script

clear

echo ""
echo -e "\e[1;36m"
echo "  ██████╗ ██╗██████╗ ██████╗ ███████╗    ██████╗ ██████╗ ██████╗ ███████╗"
echo "  ██╔══██╗██║██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██╔══██╗██╔════╝"
echo "  ██████╔╝██║██████╔╝██████╔╝█████╗      ██║  ██║██████╔╝██████╔╝█████╗  "
echo "  ██╔═══╝ ██║██╔══██╗██╔══██╗██╔══╝      ██║  ██║██╔══██╗██╔══██╗██╔══╝  "
echo "  ██║     ██║██║  ██║██║  ██║███████╗    ██████╔╝██║  ██║██║  ██║███████╗"
echo "  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝"
echo -e "\e[0m"
echo -e "\e[1;33m  Termux Discord Bot Manager - Setup\e[0m"
echo ""

# Check if running in Termux
echo -e "\e[1;34m[*] Checking environment...\e[0m"
if [ ! -d "$PREFIX" ]; then
    echo -e "\e[1;31m[!] Error: This script is designed for Termux!\e[0m"
    exit 1
fi
echo -e "\e[1;32m[✓] Termux environment detected\e[0m"

# Check for Python
echo -e "\e[1;34m[*] Checking Python...\e[0m"
if command -v python &> /dev/null; then
    echo -e "\e[1;32m[✓] Python is installed\e[0m"
else
    echo -e "\e[1;33m[!] Python not found. Installing...\e[0m"
    pkg install python -y
    if [ $? -ne 0 ]; then
        echo -e "\e[1;31m[!] Failed to install Python\e[0m"
        exit 1
    fi
    echo -e "\e[1;32m[✓] Python installed\e[0m"
fi

# Check for pip
echo -e "\e[1;34m[*] Checking pip...\e[0m"
if command -v pip &> /dev/null; then
    echo -e "\e[1;32m[✓] pip is installed\e[0m"
else
    echo -e "\e[1;33m[!] pip not found. Installing...\e[0m"
    python -m ensurepip --upgrade
    if [ $? -ne 0 ]; then
        echo -e "\e[1;31m[!] Failed to install pip\e[0m"
        exit 1
    fi
    echo -e "\e[1;32m[✓] pip installed\e[0m"
fi

# Install discord.py
echo -e "\e[1;34m[*] Installing discord.py...\e[0m"
pip install discord.py
if [ $? -ne 0 ]; then
    echo -e "\e[1;31m[!] Failed to install discord.py\e[0m"
    exit 1
fi
echo -e "\e[1;32m[✓] discord.py installed\e[0m"

# Create config directory
echo -e "\e[1;34m[*] Creating configuration directory...\e[0m"
mkdir -p ~/.discode/bots ~/.discode/commands
echo -e "\e[1;32m[✓] Configuration directory created\e[0m"

# Copy discode.py to a accessible location
echo -e "\e[1;34m[*] Installing Discode CLI...\e[0m"
cp discode.py $PREFIX/bin/discode
chmod +x $PREFIX/bin/discode
if [ $? -ne 0 ]; then
    echo -e "\e[1;31m[!] Failed to install Discode CLI\e[0m"
    exit 1
fi
echo -e "\e[1;32m[✓] Discode CLI installed\e[0m"

# Create a simple alias for easier access
echo -e "\e[1;34m[*] Creating command alias...\e[0m"
echo "alias discode='python $PREFIX/bin/discode'" >> ~/.bashrc
source ~/.bashrc
echo -e "\e[1;32m[✓] Alias created\e[0m"

echo ""
echo -e "\e[1;32m==========================================\e[0m"
echo -e "\e[1;32m  ✓ Discode Setup Complete!\e[0m"
echo -e "\e[1;32m==========================================\e[0m"
echo ""
echo -e "\e[1;36mTo use Discode:\e[0m"
echo "  1. Type 'discode' to see all available commands"
echo "  2. Create a bot: 'discode create <name> --token <your-token>'"
echo "  3. Start a bot: 'discode start <name>'"
echo "  4. Add commands: 'discode add-cmd <bot> <cmd-name> <response>'"
echo ""
echo -e "\e[1;33mTo get a Discord bot token:\e[0m"
echo "  Run: 'discode token-guide'"
echo ""
echo -e "\e[1;34mPlugin directory:\e[0m"
echo "  ~/.discode/commands/"
echo ""
echo -e "\e[1;34mBot configurations:\e[0m"
echo "  ~/.discode/config.json"
echo ""
