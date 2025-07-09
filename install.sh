#!/bin/bash

echo "[SETUP] Starting installation of Daily Dose of News application..."

if ! command -v python3 &> /dev/null then
    echo "Python3 could not be found. Please install Python3 first..."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists..."
fi

echo "Activating virtual environment..."
source ./venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

if [ ! -f requirements.txt ]; then
    echo "requirements.txt not found - get it from https://www.github.com/RexGloriae/DailyDoseOfNews ..."
    deactivate
    exit 1
fi

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Installation completed successfully..."
echo "[SETUP] Exiting..."

deactivate

exit 0