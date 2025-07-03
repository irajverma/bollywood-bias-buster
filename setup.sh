#!/bin/bash

# Setup script for Bollywood Bias Buster analysis

echo "Setting up Bollywood Bias Buster Analysis Environment..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv bollywood_analysis_env

# Activate virtual environment
echo "Activating virtual environment..."
source bollywood_analysis_env/bin/activate

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

# Download spaCy model
echo "Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Create necessary directories
echo "Creating directories..."
mkdir -p processed_data
mkdir -p analysis_results
mkdir -p logs

echo "Setup completed!"
echo ""
echo "To run the complete analysis:"
echo "1. Activate the environment: source bollywood_analysis_env/bin/activate"
echo "2. Run the pipeline: python scripts/run_complete_analysis.py /path/to/Bollywood-Data"
echo ""
echo "Example:"
echo "python scripts/run_complete_analysis.py ~/Downloads/Bollywood-Data"
