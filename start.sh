#!/bin/bash
# Startup script for the RAG Chatbot API

echo "Starting RAG Chatbot API..."

# Install dependencies if requirements.txt is newer than the virtual environment
if [ ! -f venv/Scripts/activate ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/Scripts/activate

# Install/update dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload