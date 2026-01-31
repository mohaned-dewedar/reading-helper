# Architecture Guide 🏗️

This guide explains **how** your Reading Helper works. Understanding the architecture helps you make better decisions as you build.

## The Big Picture

Your app has three main components that work together:

```
┌──────────────┐      HTTP        ┌──────────────┐      Python       ┌──────────────┐
│   Browser    │ ◄────────────► │   FastAPI    │ ◄─────────────► │    Word      │
│  (Frontend)  │   POST /file    │  (Backend)   │  analyze_text() │  Analyzer    │
└──────────────┘                 └──────────────┘                 └──────────────┘
                                        │                                  │
                                        │                                  │
                                        ▼                                  ▼
                                   Returns JSON              Calls Dictionary Service
```

## Component Breakdown

### 1. Frontend (Browser)

**Location**: `frontend/` directory

**Files**: `index.html`, `app.js`, `styles.css`

**Responsibilities**:
- Display the user interface (file upload button, text display area)
- Capture user actions (file selection, button clicks)
- Send file to backend via HTTP POST request
- Receive processed data (JSON) from backend
- Render text with interactive tooltips

**Technologies**:
- **HTML** - Structure of the webpage (headings, buttons, divs)
- **CSS** - Styling (colors, layout, tooltip appearance)
- **JavaScript** - Logic (file upload, API calls, DOM manipulation)

**Why separate these?** Following "separation of concerns":
- HTML defines **what** content exists
- CSS defines **how** it looks
- JavaScript defines **how** it behaves

### 2. Backend (FastAPI Server)

**Location**: `backend/main.py`

**Responsibilities**:
- Listen for HTTP requests on port 8000
- Receive uploaded files via POST /process-text endpoint
- Coordinate text processing (delegate to word analyzer)
- Return structured JSON responses
- Handle errors gracefully (invalid files, etc.)

**Technologies**:
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server that runs the FastAPI app

**Why FastAPI?**
- Automatic API documentation (available at /docs)
- Built-in async support (handles multiple requests efficiently)
- Automatic data validation
- Modern Python type hints

### 3. Word Analyzer

**Location**: `backend/word_analyzer.py`

**Responsibilities**:
- **Tokenize**: Split text into individual words
- **Analyze**: Determine which words are "hard"
- **Lookup**: Get definitions for hard words
- **Format**: Return structured data to main.py

**Technologies**:
- **Regular Expressions (regex)**: Text pattern matching
- **Python type hints**: Clear function signatures

**Why separate from main.py?**
- **Single Responsibility Principle**: main.py handles HTTP, analyzer handles text
- **Testability**: Can test text processing without running a server
- **Reusability**: Could use analyzer in other projects

## Data Flow: Complete Journey

When a user uploads a file, here is the complete journey:

### Step 1: User Action
User clicks file input, selects "story.txt", clicks "Process Text"

**Technology**: HTML `<input type="file">` element

### Step 2: JavaScript Creates FormData
JavaScript prepares file data for HTTP transmission

### Step 3: HTTP POST Request
Browser sends file to backend via HTTP using multipart/form-data format

### Step 4: FastAPI Receives Request
Server receives file and converts bytes to UTF-8 text string

### Step 5: Text Processing
Word analyzer tokenizes text, identifies hard words, looks up definitions

### Step 6: JSON Response
Server sends structured data back to browser

### Step 7: JavaScript Renders
JavaScript rebuilds text with hard words wrapped in spans

### Step 8: CSS Tooltip on Hover
Pure CSS displays definition when user hovers over hard words

## Key Concepts

### Client-Server Architecture

**Client** (Browser) - Requests data, displays results, handles user interaction  
**Server** (Python FastAPI) - Processes requests, performs computation, returns data

**Why split responsibilities?** Better separation of concerns and scalability.

### RESTful API Design

Your `/process-text` endpoint follows REST principles:
- Resource-oriented URL
- HTTP POST method for sending data
- Stateless (each request is independent)
- JSON response format

### Asynchronous Programming

FastAPI uses async/await to handle multiple requests efficiently without blocking.

### Word Detection Algorithm

**Phase 1 (Current)**: Simple length rule (words > 7 characters)  
**Phase 2 (Future)**: Frequency-based (check against common words list)  
**Phase 3 (Advanced)**: External API for real-time difficulty scoring

## File Responsibilities

| File | Purpose | Key Functions | Depends On |
|------|---------|---------------|------------|
| `main.py` | HTTP API | `process_text()` | word_analyzer.py |
| `word_analyzer.py` | Text processing | `tokenize()`, `analyze_text()` | dictionary_service.py |
| `dictionary_service.py` | Definitions | `get_definition()` | None |
| `app.js` | Frontend logic | `uploadFile()`, `renderText()` | main.py API |

## Design Decisions

### Mock Dictionary vs Real API
**Current**: Mock dictionary (fast, no API key needed, limited words)  
**Future**: Real API (comprehensive, requires network calls)

### Server-Side vs Client-Side Processing
**Current**: Server-side (powerful, centralized, can use Python libraries)  
**Alternative**: Client-side (faster for small files, no server needed)

### FastAPI vs Flask
**Current**: FastAPI (modern, async, auto-docs, type hints)  
**Alternative**: Flask (simpler, more tutorials)

## Security Considerations

For production, you would need:
- File size validation (prevent huge uploads)
- File type validation (only allow .txt)
- CORS configuration (specify allowed origins)
- Input sanitization (prevent XSS attacks)

## Performance Considerations

Current bottlenecks:
- File upload and text processing
- No caching (processes same file multiple times)

Future optimizations:
- Caching with `@lru_cache`
- Batch definition lookups
- Streaming responses for large files

## Next Steps

Now that you understand the architecture, proceed to **[PHASE_GUIDE.md](PHASE_GUIDE.md)** for step-by-step implementation!
