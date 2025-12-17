@echo off
REM Startup script for the RAG Chatbot API on Windows

echo Starting RAG Chatbot API...

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/update dependencies
pip install -r requirements.txt

REM Run the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload