#!/bin/bash

# Exit on error
set -e

echo "Starting setup..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Homebrew if not installed
if ! command_exists brew; then
    echo "Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    eval "$(/opt/homebrew/bin/brew shellenv)"  # Ensure `brew` is available immediately
else
    echo "Homebrew is already installed."
fi

# Install Python if not installed
if ! command_exists python3; then
    echo "Python3 not found. Installing..."
    brew install python3
else
    echo "Python3 is already installed."
fi

# Install Ollama if not installed
if ! command_exists ollama; then
    echo "Ollama not found. Installing..."
    brew install ollama
else
    echo "Ollama is already installed."
fi

# Get total RAM in GB
RAM=$(sysctl -n hw.memsize)
RAM_GB=$((RAM / 1024 / 1024 / 1024))

# Get available disk space in GB
AVAILABLE_SPACE_KB=$(df -k / | awk 'NR==2 {print $4}')
AVAILABLE_SPACE_GB=$((AVAILABLE_SPACE_KB / 1024 / 1024))

# Choose DeepSeek model based on RAM & required storage
if [ "$RAM_GB" -ge 64 ]; then
    MODEL="deepseek-r1:67b"
    REQUIRED_SPACE=50
elif [ "$RAM_GB" -ge 32 ]; then
    MODEL="deepseek-r1:32b"
    REQUIRED_SPACE=30
elif [ "$RAM_GB" -ge 16 ]; then
    MODEL="deepseek-r1:8b"
    REQUIRED_SPACE=10
elif [ "$RAM_GB" -ge 8 ]; then
    MODEL="deepseek-r1:1.5b"
    REQUIRED_SPACE=4
else
    echo "Error: Not enough RAM to run DeepSeek. Minimum 8GB required."
    exit 1
fi

# Check if there's enough free space
echo "Available Disk Space: ${AVAILABLE_SPACE_GB}GB"
if [ "$AVAILABLE_SPACE_GB" -lt "$REQUIRED_SPACE" ]; then
    echo "Error: Not enough free space to download $MODEL."
    echo "Required: ${REQUIRED_SPACE}GB, Available: ${AVAILABLE_SPACE_GB}GB."
    exit 1
fi

# Warn user about model size
echo "System RAM: ${RAM_GB}GB"
echo "The selected model ($MODEL) requires approximately ${REQUIRED_SPACE}GB of storage."
read -p "Do you want to continue with the installation? (y/n): " choice

if [[ "$choice" != "y" ]]; then
    echo "Aborting installation. Cleaning up..."


    # Uninstall Ollama (only if installed by this script)
    if command_exists ollama; then
        echo "Removing Ollama..."
        brew uninstall ollama || rm -rf ~/.ollama
    fi

    # Uninstall Python (only if installed by this script)
    if command_exists python3; then
        echo "Removing Python..."
        brew uninstall python3
    fi

    echo "Cleanup complete. Exiting."
    exit 1
fi

# Pull DeepSeek model
echo "Downloading DeepSeek model ($MODEL)..."
ollama pull "$MODEL"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the app
echo "Running the pocket-deepseek app locally..."
streamlit run app.py