# Reading Helper 📚

A learning project that helps readers by automatically detecting difficult words and showing definitions on hover.

## What You'll Learn

This project teaches full-stack web development fundamentals:

- **Backend**: Building REST APIs with Python FastAPI
- **Frontend**: Creating interactive web pages with HTML/CSS/JavaScript
- **Integration**: Connecting frontend and backend systems
- **Text Processing**: Analyzing and manipulating text data

## Quick Start

```bash
# 1. Set up the backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# 2. Open the frontend
# Simply open frontend/index.html in your browser
```

## How It Works

1. **Upload** a .txt file through the web interface
2. **Process** - Backend analyzes text and identifies hard words
3. **Display** - Text appears with hard words highlighted
4. **Learn** - Hover over words to see definitions

## Project Structure

```
reading-helper/
├── backend/          # Python FastAPI server
├── frontend/         # HTML/CSS/JS interface
├── docs/            # Learning guides
└── sample-texts/    # Test files
```

## Learning Path

Follow the guides in order:

1. **[Setup Guide](docs/SETUP.md)** - Get everything running
2. **[Architecture Guide](docs/ARCHITECTURE.md)** - Understand how it works
3. **[Phase Guide](docs/PHASE_GUIDE.md)** - Build it step-by-step

## Current Status

✅ **Project structure created** - All directories and basic files in place!

## Next Steps

Start with `docs/SETUP.md` to set up your Python environment and install dependencies.
