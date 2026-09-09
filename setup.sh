#!/bin/bash

echo "Discode Setup"

if [ ! -d "$PREFIX" ]; then
    echo "Error: Run in Termux"
    exit 1
fi

if ! command -v python &> /dev/null; then
    pkg install python -y
fi

if ! command -v pip &> /dev/null; then
    python -m ensurepip --upgrade
fi

pip install discord.py

mkdir -p ~/.discode/bots ~/.discode/commands

cp discode.py $PREFIX/bin/discode
chmod +x $PREFIX/bin/discode

echo "alias discode='python $PREFIX/bin/discode'" >> ~/.bashrc
source ~/.bashrc

echo "Setup done!"
echo "Use: discode --help"
