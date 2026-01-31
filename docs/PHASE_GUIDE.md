# Phase-by-Phase Implementation Guide 🚀

This guide walks you through building the Reading Helper **in order**. Complete each phase before moving to the next.

---

## Phase 1: Backend Foundation

**Goal**: Get a basic FastAPI server running that responds to requests.

### Step 1.1: Create Basic FastAPI App

Create `backend/main.py` with this content:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Reading Helper API is running!"}
```

**What each line does**:
- `from fastapi import FastAPI` - Import the FastAPI class
- `app = FastAPI()` - Create an instance of the FastAPI application
- `@app.get("/")` - Decorator that creates a GET endpoint at the root URL
- `def read_root()` - Function that handles requests to "/"
- `return {...}` - FastAPI automatically converts dict to JSON

**Test it**:
```bash
cd backend
uvicorn main:app --reload
```

Visit http://127.0.0.1:8000 in your browser - you should see the JSON message!

**Understanding the command**:
- `uvicorn` - The ASGI server
- `main:app` - "main" is the file name, "app" is the FastAPI instance
- `--reload` - Auto-restart when code changes (for development)

**What you learned**:
- Creating a FastAPI application
- Defining API routes with decorators
- Starting a development server
- How FastAPI automatically handles JSON

### Step 1.2: Explore Auto-Generated Documentation

One of FastAPI's best features is automatic interactive documentation!

Visit: http://127.0.0.1:8000/docs

You'll see:
- All your API endpoints listed
- Ability to test them directly in the browser
- Request/response schemas
- Try clicking "Try it out" and "Execute"

**What you learned**:
- FastAPI creates docs automatically from your code
- You can test APIs without writing separate test files

### Step 1.3: Add File Upload Endpoint

Update `backend/main.py`:

```python
from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Reading Helper API is running!"}

@app.post("/process-text")
async def process_text(file: UploadFile):
    # Read the file content
    content = await file.read()
    text = content.decode("utf-8")

    # For now, just return basic info
    return {
        "filename": file.filename,
        "content": text,
        "length": len(text)
    }
```

**New concepts explained**:
- `UploadFile` - Special FastAPI type for file uploads
- `async def` - Asynchronous function (can handle other requests while waiting)
- `await file.read()` - Wait for file to be fully read
- `decode("utf-8")` - Convert bytes to string

**Test it**:
1. Restart your server (or it auto-reloads with --reload)
2. Go to http://127.0.0.1:8000/docs
3. Click on `/process-text` endpoint
4. Click "Try it out"
5. Click "Choose File" and upload any .txt file
6. Click "Execute"

You should see your file content in the response!

**What you learned**:
- Handling file uploads with FastAPI
- Using async/await for I/O operations
- Testing file uploads with /docs interface

---

## Phase 2: Word Analysis Logic

**Goal**: Create the "brain" that detects hard words.

### Step 2.1: Create Dictionary Service

Create `backend/dictionary_service.py`:

```python
from typing import Optional

# Mock dictionary with sample definitions
# In a real app, this would call an external API
MOCK_DEFINITIONS = {
    "extraordinary": "Very unusual or remarkable.",
    "loquacious": "Tending to talk a great deal; talkative.",
    "comprehensive": "Complete and including everything necessary.",
    "contemporary": "Living or occurring at the same time.",
    "documentation": "Material that provides official information.",
    "illuminating": "Helping to clarify or explain something.",
    "comfortable": "Providing physical ease and relaxation.",
    "exceptionally": "To an unusual degree; very.",
    "particularly": "To a higher degree than is usual or average.",
    "professor": "A university teacher of the highest rank."
}

def get_definition(word: str) -> Optional[str]:
    """
    Get definition for a word.

    Args:
        word: The word to look up (can include punctuation)

    Returns:
        Definition string if found, else a default message
    """
    # Clean the word: lowercase and remove punctuation
    clean_word = word.lower().strip('.,!?;:\'"')

    # Look up in our mock dictionary
    return MOCK_DEFINITIONS.get(
        clean_word,
        "A complex word worth looking up!"
    )
```

**Concepts explained**:
- `Optional[str]` - Type hint meaning "string or None"
- `.get(key, default)` - Dictionary method that returns default if key not found
- `.strip('.,!?')` - Remove specified characters from start/end of string

**Test it** (create `backend/test_dict.py`):
```python
from dictionary_service import get_definition

print(get_definition("extraordinary"))  # Should print definition
print(get_definition("cat"))  # Should print default message
print(get_definition("loquacious,"))  # Should handle punctuation
```

Run: `python backend/test_dict.py`

**What you learned**:
- Creating reusable modules
- Type hints for better code documentation
- Dictionary lookups with defaults

### Step 2.2: Create Word Analyzer

Create `backend/word_analyzer.py`:

```python
import re
from typing import List, Dict
from dictionary_service import get_definition

def tokenize(text: str) -> List[str]:
    """
    Split text into words and punctuation.

    Example:
        "Hello, world!" → ["Hello", ",", "world", "!"]

    Why? We want to preserve punctuation in output but analyze it separately.
    """
    # Regex pattern:
    # \w+ matches one or more word characters (letters, numbers, underscore)
    # | means "or"
    # [.,!?;] matches individual punctuation marks
    tokens = re.findall(r"[\w']+|[.,!?;]", text)
    return tokens

def is_hard_word(word: str) -> bool:
    """
    Determine if a word is "hard" based on length.

    Simple rule: words longer than 7 characters are considered hard.

    Note: This is a simple heuristic. More advanced versions could:
    - Check word frequency (rare words are harder)
    - Use reading level algorithms (Flesch-Kincaid, etc.)
    - Call an external API for difficulty scoring
    """
    # Remove any punctuation that might still be attached
    clean_word = re.sub(r'[^\w]', '', word)

    # Check if word is long enough to be considered "hard"
    return len(clean_word) > 7

def analyze_text(text: str) -> List[Dict]:
    """
    Analyze text and return metadata for each word.

    Args:
        text: Raw text string to analyze

    Returns:
        List of dictionaries with structure:
        {
            "word": "loquacious",
            "is_hard": True,
            "definition": "Tending to talk a great deal"
        }
    """
    # Step 1: Tokenize
    tokens = tokenize(text)

    # Step 2: Analyze each token
    results = []
    for token in tokens:
        # Check if this word is hard
        is_hard = is_hard_word(token)

        # Get definition only for hard words
        definition = None
        if is_hard:
            definition = get_definition(token)

        # Build result object
        results.append({
            "word": token,
            "is_hard": is_hard,
            "definition": definition
        })

    return results
```

**Concepts explained**:
- `re.findall()` - Find all matches of a regex pattern
- `r"pattern"` - Raw string (backslashes don't need escaping)
- `List[Dict]` - Type hint for list of dictionaries
- Docstrings - Multi-line strings that document functions

**Test it** (create `backend/test_analyzer.py`):
```python
from word_analyzer import analyze_text

text = "The cat is loquacious and extraordinary."
result = analyze_text(text)

for item in result:
    hard_marker = "⭐" if item['is_hard'] else "  "
    print(f"{hard_marker} {item['word']:15} → {item['definition']}")
```

Run: `python backend/test_analyzer.py`

Expected output:
```
   The             → None
   cat             → None
   is              → None
⭐ loquacious     → Tending to talk a great deal; talkative.
   and             → None
⭐ extraordinary  → Very unusual or remarkable.
   .               → None
```

**What you learned**:
- Regular expressions for text parsing
- List comprehensions and iteration
- Building structured data (list of dicts)
- Docstring documentation

### Step 2.3: Integrate Analyzer with API

Update `backend/main.py`:

```python
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from word_analyzer import analyze_text

app = FastAPI()

# Add CORS middleware to allow requests from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development. In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Reading Helper API is running!"}

@app.post("/process-text")
async def process_text(file: UploadFile):
    """
    Process uploaded text file and identify hard words.

    Returns:
        JSON with filename and processed word data
    """
    # Read file content
    content = await file.read()
    text = content.decode("utf-8")

    # Analyze the text
    processed_words = analyze_text(text)

    # Return structured response
    return {
        "filename": file.filename,
        "processed_words": processed_words
    }
```

**New concepts**:
- CORS middleware - Allows browser to make requests to your API
- `allow_origins=["*"]` - Allow all origins (for development only!)
- Importing your custom module

**Test the complete backend**:
1. Restart server
2. Go to http://127.0.0.1:8000/docs
3. Upload a sample .txt file
4. Check response - you should see each word with `is_hard` and `definition` fields!

**What you learned**:
- Integrating modules into your API
- CORS and why it's needed
- Building complete backend functionality

---

## Phase 3: Frontend Interface

**Goal**: Create a web page to interact with your API.

### Step 3.1: Create HTML Structure

Create `frontend/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reading Helper</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 Reading Helper</h1>
            <p>Upload a text file to identify difficult words and see definitions</p>
        </header>

        <div class="upload-section">
            <input type="file" id="fileInput" accept=".txt">
            <button id="uploadBtn">Process Text</button>
        </div>

        <div id="status"></div>

        <div id="textDisplay" class="text-display"></div>
    </div>

    <script src="app.js"></script>
</body>
</html>
```

**HTML elements explained**:
- `<input type="file">` - File selector
- `accept=".txt"` - Only show .txt files in file picker
- `<div id="status">` - Status messages (loading, success, error)
- `<div id="textDisplay">` - Where processed text will appear
- `<script src="app.js">` - Link to JavaScript file

**Test it**: Open `frontend/index.html` in your browser. You should see the basic structure (unstyled for now).

### Step 3.2: Add CSS Styling

Create `frontend/styles.css`:

```css
/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    border-radius: 10px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

/* Header */
header {
    text-align: center;
    margin-bottom: 30px;
}

h1 {
    color: #333;
    margin-bottom: 10px;
}

header p {
    color: #666;
}

/* Upload section */
.upload-section {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

#fileInput {
    flex: 1;
    padding: 10px;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-size: 14px;
}

button {
    padding: 10px 30px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    transition: background 0.3s;
}

button:hover {
    background: #5568d3;
}

button:active {
    transform: scale(0.98);
}

/* Status messages */
#status {
    margin-bottom: 20px;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    font-weight: 500;
}

.status-loading {
    background: #cfe2ff;
    color: #084298;
}

.status-success {
    background: #d1e7dd;
    color: #0f5132;
}

.status-error {
    background: #f8d7da;
    color: #842029;
}

/* Text display */
.text-display {
    line-height: 1.8;
    font-size: 18px;
    padding: 20px;
    background: #f9f9f9;
    border-radius: 5px;
    min-height: 200px;
}

/* Hard word styling */
.hard-word {
    background: #fff3cd;
    padding: 2px 4px;
    border-radius: 3px;
    cursor: help;
    position: relative;
    border-bottom: 2px dotted #667eea;
    transition: background 0.2s;
}

.hard-word:hover {
    background: #ffe69c;
}

/* Tooltip */
.hard-word::after {
    content: attr(data-definition);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: #333;
    color: white;
    padding: 8px 12px;
    border-radius: 5px;
    font-size: 14px;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s;
    margin-bottom: 5px;
    z-index: 10;
}

.hard-word:hover::after {
    opacity: 1;
}

/* Tooltip arrow */
.hard-word::before {
    content: '';
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 5px solid transparent;
    border-top-color: #333;
    opacity: 0;
    transition: opacity 0.3s;
}

.hard-word:hover::before {
    opacity: 1;
}
```

**CSS concepts explained**:
- `::before` and `::after` - Pseudo-elements for tooltip
- `position: relative/absolute` - Positioning tooltips
- `attr(data-definition)` - Get value from HTML data attribute
- `opacity` and `transition` - Smooth fade-in effect
- `z-index` - Ensure tooltip appears on top

**Test it**: Refresh your browser - the page should look beautiful now!

### Step 3.3: Add JavaScript Logic

Create `frontend/app.js`:

```javascript
// Get references to DOM elements
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const statusDiv = document.getElementById('status');
const textDisplay = document.getElementById('textDisplay');

// API endpoint - update if your backend runs on a different port
const API_URL = 'http://127.0.0.1:8000/process-text';

// Handle upload button click
uploadBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];

    // Validation
    if (!file) {
        showStatus('Please select a file first!', 'error');
        return;
    }

    showStatus('Processing...', 'loading');

    try {
        // Create FormData and add file
        const formData = new FormData();
        formData.append('file', file);

        // Send POST request to backend
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        // Check if request was successful
        if (!response.ok) {
            throw new Error('Failed to process text');
        }

        // Parse JSON response
        const data = await response.json();

        // Render the processed text
        renderText(data.processed_words);

        showStatus('Text processed successfully!', 'success');

    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
        console.error('Full error:', error);
    }
});

function showStatus(message, type) {
    """
    Display status message to user.

    Args:
        message: Text to display
        type: 'loading', 'success', or 'error'
    """
    statusDiv.textContent = message;
    statusDiv.className = `status-${type}`;
}

function renderText(words) {
    """
    Render processed words with hard words highlighted.

    Args:
        words: Array of word objects from backend
    """
    // Clear previous content
    textDisplay.innerHTML = '';

    // Process each word
    words.forEach(wordObj => {
        if (wordObj.is_hard) {
            // Create span for hard words
            const span = document.createElement('span');
            span.className = 'hard-word';
            span.textContent = wordObj.word;
            span.setAttribute('data-definition', wordObj.definition);
            textDisplay.appendChild(span);
        } else {
            // Regular text node
            textDisplay.appendChild(document.createTextNode(wordObj.word));
        }

        // Add space after each word (but not after punctuation)
        if (!/[.,!?;]/.test(wordObj.word)) {
            textDisplay.appendChild(document.createTextNode(' '));
        }
    });
}
```

**JavaScript concepts explained**:
- `document.getElementById()` - Get reference to HTML element
- `addEventListener()` - Listen for user actions
- `async/await` - Handle asynchronous operations
- `FormData` - Format data for file upload
- `fetch()` - Make HTTP requests
- `createElement()` - Create new HTML elements
- `setAttribute()` - Set HTML attributes
- `appendChild()` - Add element to DOM

**Test the complete app**:
1. Make sure backend is running (`uvicorn main:app --reload`)
2. Open `frontend/index.html` in browser
3. Select a text file
4. Click "Process Text"
5. Hover over highlighted words to see definitions!

**What you learned**:
- DOM manipulation
- Async JavaScript (fetch, promises)
- Form data handling
- Error handling
- Creating interactive UIs

---

## Phase 4: Testing with Sample Data

**Goal**: Create test files to verify everything works.

### Step 4.1: Create Sample Text Files

Create `sample-texts/simple.txt`:

```
The cat sat on the mat. It was extraordinary how comfortable the feline appeared.
```

Create `sample-texts/medium.txt`:

```
The loquacious professor delivered an exceptionally comprehensive lecture about
contemporary literature. Students found the documentation particularly illuminating.
```

### Step 4.2: Test End-to-End

1. Start backend: `uvicorn backend.main:app --reload`
2. Open `frontend/index.html`
3. Upload `sample-texts/simple.txt`
4. Verify "extraordinary" and "comfortable" are highlighted
5. Hover to see definitions
6. Upload `sample-texts/medium.txt`
7. Verify multiple words are highlighted

---

## Testing Checklist

- [ ] Backend server starts without errors
- [ ] Can access http://127.0.0.1:8000 and see welcome message
- [ ] Can access http://127.0.0.1:8000/docs and see API documentation
- [ ] File upload works in /docs interface
- [ ] JSON response contains word metadata
- [ ] Frontend page opens without errors
- [ ] Can select and upload file
- [ ] Text appears after upload
- [ ] Hard words are highlighted
- [ ] Tooltips show on hover
- [ ] Definitions are correct

---

## Common Issues & Solutions

### "CORS error" in browser console
**Problem**: Browser blocks requests to different origin
**Solution**: Make sure CORS middleware is added to main.py (see Phase 2.3)

### "Cannot read property of undefined"
**Problem**: API response structure doesn't match expectations
**Solution**: Check console.log(data) to see actual structure

### Tooltips don't appear
**Problem**: CSS positioning or z-index issues
**Solution**: Verify .hard-word has `position: relative`

### File not uploading
**Problem**: FormData not set up correctly
**Solution**: Ensure parameter name matches: `formData.append('file', file)`

### "Module not found" error
**Problem**: Python can't find your modules
**Solution**: Run `uvicorn main:app` from backend directory

---

## Next Steps

Congratulations! You've built a complete full-stack application!

### Enhancements to Try

1. **Better Word Detection**
   - Use word frequency lists
   - Different difficulty thresholds

2. **Real Dictionary API**
   - Integrate Free Dictionary API
   - Add caching

3. **UI Improvements**
   - Different highlight colors for difficulty levels
   - Reading statistics (grade level, average word length)
   - Dark mode toggle

4. **Features**
   - Save processed texts
   - Export to HTML
   - Support for PDF/DOCX files
   - User preferences (customize threshold)

### What You've Learned

**Backend**:
- ✅ Building REST APIs with FastAPI
- ✅ File upload handling
- ✅ Async programming
- ✅ Modular code organization
- ✅ Regular expressions
- ✅ Type hints

**Frontend**:
- ✅ HTML structure
- ✅ CSS styling and positioning
- ✅ JavaScript DOM manipulation
- ✅ Fetch API for HTTP requests
- ✅ Event handling
- ✅ Creating interactive tooltips

**Integration**:
- ✅ Client-server architecture
- ✅ CORS handling
- ✅ JSON data exchange
- ✅ Error handling

Keep experimenting and building!
