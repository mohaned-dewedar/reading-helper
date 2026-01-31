# Setup Guide 🛠️

This guide walks you through setting up your development environment from scratch.

## Prerequisites

Before starting, make sure you have:

- **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- A **text editor** (VS Code, Sublime, or any editor you like)
- A **web browser** (Chrome, Firefox, etc.)
- **Git** (already initialized in your project)

## Step 1: Verify Directory Structure

Your project should have these directories:

```bash
ls
# Should show: backend/ frontend/ docs/ sample-texts/ README.md
```

### 📝 Why This Structure?

- **backend/** - Keeps all Python code separate from HTML/CSS/JS
- **frontend/** - All user-facing code in one place
- **docs/** - Documentation to guide your learning
- **sample-texts/** - Test data to verify your app works

## Step 2: Set Up Python Virtual Environment

A virtual environment keeps your project's dependencies isolated from your system Python.

```bash
cd backend
python -m venv venv
```

**What just happened?**
- Created a `venv` folder containing a clean Python installation
- Your project's packages won't interfere with system Python
- Each project can have different package versions

### Activate the Virtual Environment

**On Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**On Mac/Linux:**
```bash
source venv/bin/activate
```

**How to tell it worked?**
You should see `(venv)` at the start of your command prompt.

## Step 3: Install Python Dependencies

The `requirements.txt` file has already been created with these packages:

```txt
fastapi==0.104.1        # Web framework
uvicorn[standard]==0.24.0   # Server to run FastAPI
python-multipart==0.0.6     # Handles file uploads
```

Install them all at once:

```bash
pip install -r requirements.txt
```

### 📦 What Each Package Does

- **fastapi** - The web framework for building your API. It's modern, fast, and has automatic documentation.
- **uvicorn** - An ASGI server that runs FastAPI applications. ASGI is the interface between web servers and Python web applications.
- **python-multipart** - Allows FastAPI to handle file uploads (multipart/form-data requests).

## Step 4: Verify Installation

Check that everything installed correctly:

```bash
python --version
# Should show Python 3.8 or higher

pip list
# Should show fastapi, uvicorn, python-multipart and their dependencies
```

## Step 5: Understanding .gitignore

The `.gitignore` file tells Git which files NOT to track. Let's understand why each entry matters:

```gitignore
# Python
backend/venv/          # Virtual environment (can be recreated)
backend/__pycache__/   # Compiled Python files (auto-generated)
*.pyc, *.pyo, *.pyd    # More compiled files

# Environment
.env                   # Secret keys (NEVER commit secrets!)

# IDE
.vscode/, .idea/       # Editor settings (personal preference)

# OS
.DS_Store, Thumbs.db   # System files (Mac/Windows)
```

### 🔒 Why .gitignore Matters

- **venv/** is huge (thousands of files) and can be recreated with `pip install -r requirements.txt`
- **\_\_pycache\_\_/** contains compiled Python that's auto-generated
- **.env** files contain secrets (API keys, passwords) - committing these is a security risk
- **IDE files** are personal preferences and differ between team members

## Step 6: Project File Overview

Let's understand what each file will do once created:

### Backend Files (Python)

```
backend/
├── venv/                    # Virtual environment (DO NOT EDIT)
├── __pycache__/            # Compiled Python (auto-generated)
├── main.py                 # FastAPI app & API routes
├── word_analyzer.py        # Text processing logic
├── dictionary_service.py   # Definition lookup
└── requirements.txt        # Package dependencies
```

### Frontend Files (HTML/CSS/JS)

```
frontend/
├── index.html    # User interface structure
├── styles.css    # Visual styling
└── app.js        # Logic & API communication
```

### Documentation Files

```
docs/
├── SETUP.md          # This file!
├── ARCHITECTURE.md   # How the system works
└── PHASE_GUIDE.md    # Step-by-step code tutorial
```

## Troubleshooting Common Issues

### "python: command not found"
**Problem**: Python isn't installed or not in PATH  
**Solution**: 
- Install Python from python.org
- Or try `python3` instead of `python`

### "pip: command not found"
**Problem**: pip isn't in PATH  
**Solution**: Use `python -m pip` instead of `pip`

### Virtual environment won't activate (Windows PowerShell)
**Problem**: Execution policy prevents running scripts  
**Solution**: Run this command:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Virtual environment won't activate (Mac/Linux)
**Problem**: Wrong activate command  
**Solution**: Make sure you're using `source venv/bin/activate` (not just `venv/bin/activate`)

### "Port 8000 already in use" error
**Problem**: Another process is using port 8000  
**Solution**: 
- Use a different port: `uvicorn main:app --port 8001`
- Or find and stop the process using port 8000

### Package installation fails
**Problem**: Network issues or outdated pip  
**Solution**: 
```bash
python -m pip install --upgrade pip  # Update pip
pip install -r requirements.txt       # Try again
```

## Next Steps

✅ **Environment is ready!**

You now have:
- ✅ Project directories created
- ✅ Virtual environment set up
- ✅ Dependencies installed
- ✅ Git configured to ignore unnecessary files

**What's Next?**

1. Read **[ARCHITECTURE.md](ARCHITECTURE.md)** to understand how the system is designed
2. Then follow **[PHASE_GUIDE.md](PHASE_GUIDE.md)** to start building!

## Quick Reference Commands

```bash
# Activate virtual environment
cd backend
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the server (after creating main.py)
uvicorn main:app --reload

# Deactivate virtual environment
deactivate
```

## Learning Resources

To learn more about the tools we're using:

- **FastAPI**: https://fastapi.tiangolo.com/
- **Python Virtual Environments**: https://docs.python.org/3/tutorial/venv.html
- **pip Documentation**: https://pip.pypa.io/
- **Git .gitignore**: https://git-scm.com/docs/gitignore
