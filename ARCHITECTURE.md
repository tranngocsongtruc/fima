# System Architecture - Smart File Organizer

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  ┌──────────────────┐              ┌──────────────────┐       │
│  │  Web Browser     │              │  macOS Finder    │       │
│  │  (Frontend UI)   │              │  (File System)   │       │
│  └────────┬─────────┘              └────────┬─────────┘       │
└───────────┼──────────────────────────────────┼─────────────────┘
            │                                  │
            │ HTTP/REST                        │ File Events
            ▼                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND SERVER (FastAPI)                   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                         │  │
│  │  /analyze  /reorganize  /monitor  /reminder  /report    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │   Config    │  │  Database   │  │  Notification Mgr   │   │
│  │  Manager    │  │  (SQLite)   │  │  (macOS Native)     │   │
│  └─────────────┘  └─────────────┘  └─────────────────────┘   │
└───────────┬───────────────┬───────────────┬───────────────────┘
            │               │               │
            ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CORE SERVICES                              │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  File Monitor    │  │  AI Classifier   │  │   Folder     │ │
│  │  (Watchdog)      │  │  (Groq)          │  │   Analyzer   │ │
│  │                  │  │                  │  │   (Claude)   │ │
│  │  - FSEvents      │  │  - Fast classify │  │  - Deep      │ │
│  │  - Real-time     │  │  - <50ms         │  │    analysis  │ │
│  │  - Downloads     │  │  - High accuracy │  │  - Patterns  │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  Reorganizer     │  │  Email Reporter  │  │   Reminder   │ │
│  │                  │  │                  │  │   Service    │ │
│  │  - Move files    │  │  - HTML reports  │  │  - Async     │ │
│  │  - Create dirs   │  │  - SMTP send     │  │  - Scheduled │ │
│  │  - Archive       │  │  - Beautiful UI  │  │  - Alerts    │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
            │                       │                   │
            ▼                       ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │    Groq      │  │   Claude     │  │   Lava (Optional)    │ │
│  │    API       │  │    API       │  │   API Gateway        │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow - File Download Scenario

```
1. USER DOWNLOADS FILE
   │
   ├─> File appears in ~/Downloads/CS170_HW7.pdf
   │
   ▼
2. FILE MONITOR DETECTS
   │
   ├─> Watchdog FSEvents triggers
   ├─> file_monitor.py: on_created() called
   │
   ▼
3. AI CLASSIFICATION (Groq)
   │
   ├─> Extract metadata (name, type, size)
   ├─> Extract PDF text preview (first 500 chars)
   ├─> Send to Groq API
   ├─> Receive classification (<50ms)
   │   {
   │     "category": "homework",
   │     "suggested_path": "uc_berkeley/fall_2025/cs170/homework",
   │     "confidence": 0.95
   │   }
   │
   ▼
4. FILE REORGANIZATION
   │
   ├─> Build destination path
   │   ~/Documents/SmartFileOrganizer/uc_berkeley/fall_2025/cs170/homework/
   ├─> Create directories if needed
   ├─> Move file from Downloads to destination
   ├─> Handle duplicates (append _1, _2, etc.)
   │
   ▼
5. LOGGING & NOTIFICATION
   │
   ├─> Log to SQLite database
   │   - filename, original_path, new_path
   │   - classification, confidence, timestamp
   ├─> Show macOS notification
   │   "File Organized: CS170_HW7.pdf → uc_berkeley/fall_2025/cs170/homework/"
   │
   ▼
6. USER SEES RESULT
   │
   └─> File in organized location
   └─> Notification on screen
   └─> Can view in Recent Operations
```

---

## 🧠 AI Classification Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    FILE METADATA EXTRACTION                     │
│                                                                 │
│  Input: /Users/user/Downloads/CS170_HW7.pdf                    │
│                                                                 │
│  Extract:                                                       │
│  ├─ Filename: "CS170_HW7.pdf"                                  │
│  ├─ Extension: ".pdf"                                          │
│  ├─ Size: 2.3 MB                                               │
│  ├─ MIME Type: "application/pdf"                               │
│  └─ Content Preview: "CS 170 Homework 7\nDue: Oct 30..."       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GROQ AI CLASSIFICATION                       │
│                                                                 │
│  Prompt:                                                        │
│  "Classify this file and suggest optimal folder structure:     │
│   Filename: CS170_HW7.pdf                                      │
│   Extension: .pdf                                              │
│   Content: CS 170 Homework 7..."                               │
│                                                                 │
│  Model: llama-3.1-70b-versatile                                │
│  Temperature: 0.3                                              │
│  Response Format: JSON                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLASSIFICATION RESULT                        │
│                                                                 │
│  {                                                              │
│    "category": "homework",                                      │
│    "subcategory": "assignment",                                 │
│    "suggested_path": "uc_berkeley/fall_2025/cs170/homework",   │
│    "confidence": 0.95,                                          │
│    "reasoning": "Detected CS170 course homework assignment",    │
│    "metadata": {                                                │
│      "school": "UC Berkeley",                                   │
│      "course": "CS170",                                         │
│      "semester": "Fall 2025"                                    │
│    }                                                            │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CONFIDENCE CHECK                             │
│                                                                 │
│  IF confidence > 0.5:                                           │
│    ├─> Auto-move file                                          │
│    └─> Show success notification                               │
│                                                                 │
│  ELSE:                                                          │
│    ├─> Keep in Downloads                                       │
│    └─> Show "needs review" notification                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Folder Analysis Pipeline (Claude)

```
┌─────────────────────────────────────────────────────────────────┐
│                    DIRECTORY STRUCTURE SCAN                     │
│                                                                 │
│  Scan: ~/Documents                                             │
│  Max Depth: 4 levels                                           │
│                                                                 │
│  Result:                                                        │
│  Documents/                                                     │
│  ├─ School/ (45 files, 120 MB)                                │
│  │  ├─ CS170/ (15 files)                                      │
│  │  └─ Math/ (30 files)                                       │
│  ├─ Work/ (120 files, 450 MB)                                 │
│  └─ Personal/ (200 files, 1.2 GB)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE PATTERN ANALYSIS                      │
│                                                                 │
│  Prompt:                                                        │
│  "Analyze this folder structure:                               │
│   [structure summary]                                          │
│   What patterns do you observe?                                │
│   What are strengths/weaknesses?"                              │
│                                                                 │
│  Model: claude-3-5-sonnet-20241022                             │
│  Max Tokens: 2000                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYSIS RESULT                              │
│                                                                 │
│  {                                                              │
│    "patterns_observed": [                                       │
│      "Mixed organization by project and date",                  │
│      "Inconsistent naming conventions",                         │
│      "Some folders very deep, others flat"                      │
│    ],                                                           │
│    "strengths": [                                               │
│      "Clear separation of School/Work/Personal"                 │
│    ],                                                           │
│    "weaknesses": [                                              │
│      "No consistent date-based organization",                   │
│      "Duplicate files across folders"                           │
│    ],                                                           │
│    "consistency_score": 0.6                                     │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OPTIMIZATION SUGGESTIONS                     │
│                                                                 │
│  Prompt:                                                        │
│  "Based on this analysis, suggest improvements..."             │
│                                                                 │
│  Result:                                                        │
│  {                                                              │
│    "suggested_structure": {                                     │
│      "root_folders": [                                          │
│        "uc_berkeley/",                                          │
│        "work/",                                                 │
│        "personal/"                                              │
│      ],                                                         │
│      "naming_conventions": [                                    │
│        "Use lowercase with underscores",                        │
│        "Include semester/year for school files"                 │
│      ]                                                          │
│    },                                                           │
│    "migration_plan": [                                          │
│      {                                                          │
│        "action": "move",                                        │
│        "source": "School/CS170/hw1.pdf",                       │
│        "destination": "uc_berkeley/fall_2025/cs170/homework/", │
│        "reason": "Standardize school organization"              │
│      }                                                          │
│    ]                                                            │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔔 Notification System

```
┌─────────────────────────────────────────────────────────────────┐
│                    NOTIFICATION TRIGGERS                        │
│                                                                 │
│  1. File Organized                                             │
│     ├─> Title: "File Organized"                               │
│     ├─> Message: "filename → folder/"                         │
│     └─> Sound: Glass                                          │
│                                                                 │
│  2. Progress Update (50%, 90%, 100%)                           │
│     ├─> Title: "Reorganization Progress"                      │
│     ├─> Message: "X/Y operations completed"                   │
│     └─> Sound: Only at 100%                                   │
│                                                                 │
│  3. File Reminder                                              │
│     ├─> Title: "File Reminder"                                │
│     ├─> Message: "Check: filename"                            │
│     └─> Sound: Glass                                          │
│                                                                 │
│  4. User Choice Confirmation                                   │
│     ├─> Title: "Choice Confirmed"                             │
│     ├─> Message: "I support your decision..."                 │
│     └─> Sound: None                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    macOS NOTIFICATION API                       │
│                                                                 │
│  Method: osascript (AppleScript)                               │
│                                                                 │
│  Command:                                                       │
│  osascript -e '                                                │
│    display notification "message"                              │
│    with title "Smart File Organizer"                           │
│    subtitle "title"                                            │
│    sound name "Glass"                                          │
│  '                                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    USER SEES NOTIFICATION                       │
│                                                                 │
│  ┌────────────────────────────────────────────────┐            │
│  │  Smart File Organizer                          │            │
│  │  File Organized                                │            │
│  │  CS170_HW7.pdf → uc_berkeley/.../homework/     │            │
│  └────────────────────────────────────────────────┘            │
│                                                                 │
│  Location: Top-right of screen                                 │
│  Duration: ~5 seconds                                          │
│  Sound: Glass.aiff (if enabled)                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💾 Database Schema

```sql
-- File Operations History
CREATE TABLE file_operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    original_path TEXT NOT NULL,
    new_path TEXT,
    operation_type TEXT NOT NULL,  -- 'detected', 'moved', 'archived'
    file_type TEXT,                -- 'homework', 'receipt', 'media'
    classification TEXT,           -- subcategory
    confidence REAL,               -- 0.0 - 1.0
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending'  -- 'pending', 'completed', 'failed'
);

-- Folder Analysis Results
CREATE TABLE folder_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_files INTEGER,
    folder_structure TEXT,         -- JSON
    optimization_suggestions TEXT, -- JSON
    user_choice TEXT               -- 'keep' or 'optimize'
);

-- File Reminders
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL,
    reminder_time DATETIME NOT NULL,
    message TEXT,
    status TEXT DEFAULT 'active',  -- 'active', 'completed'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- User Preferences
CREATE TABLE preferences (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Email Reports
CREATE TABLE email_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_email TEXT NOT NULL,
    report_data TEXT,              -- JSON
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'sent'     -- 'sent', 'failed'
);
```

---

## 🔐 Security & Privacy

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA PRIVACY LAYERS                          │
│                                                                 │
│  Layer 1: Local Processing                                     │
│  ├─ All file operations happen locally                         │
│  ├─ No file content uploaded to cloud                          │
│  └─ Database stored locally (SQLite)                           │
│                                                                 │
│  Layer 2: Minimal API Data                                     │
│  ├─ Only metadata sent to AI APIs:                             │
│  │  - Filename                                                 │
│  │  - File type/extension                                      │
│  │  - File size                                                │
│  │  - PDF text preview (first 500 chars only)                  │
│  ├─ Never send:                                                │
│  │  - Full file content                                        │
│  │  - Personal information                                     │
│  │  - File paths (only relative paths)                         │
│                                                                 │
│  Layer 3: API Key Security                                     │
│  ├─ Stored in .env file (gitignored)                           │
│  ├─ Never committed to version control                         │
│  ├─ Loaded via environment variables                           │
│  └─ Not exposed in API responses                               │
│                                                                 │
│  Layer 4: User Control                                         │
│  ├─ Toggle on/off anytime                                      │
│  ├─ Archive before delete                                      │
│  ├─ All operations logged                                      │
│  └─ Can review before confirming                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Performance Optimization

```
┌─────────────────────────────────────────────────────────────────┐
│                    OPTIMIZATION STRATEGIES                      │
│                                                                 │
│  1. Model Quantization (Annapurna Labs Track)                  │
│     ├─ INT8 quantization for inference                         │
│     ├─ Reduced model size: 70B → optimized                     │
│     └─ Result: 500ms → <50ms latency                           │
│                                                                 │
│  2. Async Operations                                           │
│     ├─ Non-blocking file operations                            │
│     ├─ Background reminder service                             │
│     └─ Async API endpoints                                     │
│                                                                 │
│  3. Caching                                                    │
│     ├─ Cache file metadata                                     │
│     ├─ Cache classification results                            │
│     └─ Reuse for duplicate files                               │
│                                                                 │
│  4. Batch Processing                                           │
│     ├─ Batch classify multiple files                           │
│     ├─ Single API call for multiple items                      │
│     └─ Reduced API overhead                                    │
│                                                                 │
│  5. Memory Management                                          │
│     ├─ Stream large files                                      │
│     ├─ Limit PDF text extraction                               │
│     └─ Clean up temp data                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    ERROR SCENARIOS                              │
│                                                                 │
│  1. API Key Missing/Invalid                                    │
│     ├─> Validate on startup                                    │
│     ├─> Show clear error message                               │
│     ├─> Provide setup instructions                             │
│     └─> Fallback to rule-based classification                  │
│                                                                 │
│  2. File Permission Error                                      │
│     ├─> Catch PermissionError                                  │
│     ├─> Log error to database                                  │
│     ├─> Show notification to user                              │
│     └─> Skip file, continue processing                         │
│                                                                 │
│  3. API Rate Limit                                             │
│     ├─> Catch rate limit exception                             │
│     ├─> Implement exponential backoff                          │
│     ├─> Queue requests                                         │
│     └─> Fallback to rule-based                                 │
│                                                                 │
│  4. Network Error                                              │
│     ├─> Retry with timeout                                     │
│     ├─> Fallback to offline mode                               │
│     ├─> Queue for later processing                             │
│     └─> Notify user                                            │
│                                                                 │
│  5. File Already Exists                                        │
│     ├─> Detect duplicate                                       │
│     ├─> Append number (_1, _2, etc.)                           │
│     ├─> Log operation                                          │
│     └─> Continue                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

**Architecture designed for CalHacks 12 - October 2025** 🚀
