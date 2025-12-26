#!/bin/bash

set -e

echo "Setting up Formbricks Challenge environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --break-system-packages -q -r requirements.txt 2>/dev/null || pip install -q -r requirements.txt
echo "✓ Python dependencies installed"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "✗ Docker not found. Please install Docker first."
    exit 1
fi
echo "✓ Docker installed"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "✗ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi
echo "✓ Docker Compose installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created. Update with your OpenAI API key if needed."
else
    echo "✓ .env file already exists"
fi

echo ""
echo "Setup complete! You can now run:"
echo "  python3 main.py formbricks up       - Start Formbricks"
echo "  python3 main.py formbricks generate - Generate data"
echo "  python3 main.py formbricks seed     - Seed the platform"
echo "  python3 main.py formbricks down     - Stop Formbricks"
