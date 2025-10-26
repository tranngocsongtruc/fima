# 🚀 How to Run - Smart File Organizer

## 📋 Prerequisites

Before running, make sure you have:
- ✅ macOS 12.0+ (M1/M2/M3/M4)
- ✅ Python 3.10+
- ✅ Claude API key from Anthropic

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Clone & Setup
```bash
# Navigate to project
cd /Users/tructran/Desktop/calundergrad/hackathons/calhack12/fima

# Install dependencies
pip install -r requirements-core.txt
```

### Step 2: Configure API Keys
```bash
# Copy example env file
cp .env.example .env

# Edit .env file
nano .env
# or
open -a TextEdit .env
```

Add your Claude API key:
```env
ANTHROPIC_API_KEY=your_claude_api_key_here
```

### Step 3: Launch!
```bash
./launch_app.sh
```

The app will:
- ✅ Start the backend server
- ✅ Open web UI in your browser (http://127.0.0.1:8000)
- ✅ Show first-launch experience (if first time)

---

## 🎯 Main Feature 1: Real-Time File Organization

**What it does**: Automatically organizes files as you download them

### How to Run:

#### Step 1: Start Monitoring
```bash
# 1. Launch the app
./launch_app.sh

# 2. In the web UI (http://127.0.0.1:8000)
#    Click "▶️ Start Monitoring" button
#    Status should change to 🟢 Active
```

#### Step 2: Download a File
```bash
# Open your browser (Chrome, Safari, etc.)
# Go to any file download link, for example:
https://cs170.org/assets/pdf/hw07.pdf

# Click download
```

#### Step 3: Watch the Magic! ✨
```
What happens (in <1 second):
├── File downloads to ~/Downloads/hw07.pdf
├── AI detects and analyzes file
├── Recognizes: "CS170 homework, Fall 2025, UC Berkeley"
├── Creates folders: ~/Documents/SmartFileOrganizer/uc_berkeley/fall_2025/cs170/homework/
├── Moves file automatically
├── Shows macOS notification (top-right corner)
└── Updates web UI
```

#### Step 4: Verify
```bash
# Check the organized file
open ~/Documents/SmartFileOrganizer/

# You should see:
# SmartFileOrganizer/
#   └── uc_berkeley/
#       └── fall_2025/
#           └── cs170/
#               └── homework/
#                   └── hw07.pdf
```

### Expected Results:
- ✅ macOS notification appears (top-right)
- ✅ Web UI shows new operation in "Recent Operations"
- ✅ File moved to organized folder
- ✅ Folder structure created automatically
- ✅ Total time: <1 second

### Demo Files to Try:
```bash
# CS170 Homework
https://cs170.org/assets/pdf/hw07.pdf
→ Organizes to: uc_berkeley/fall_2025/cs170/homework/

# Any PDF from your courses
→ AI will recognize course name and organize accordingly

# Work documents
→ Organizes to: work/[company]/[project]/

# Receipts
→ Organizes to: receipts/2025/october/
```

---

## 🎯 Main Feature 2: File Reminders

**What it does**: Set reminders to review specific files later

### How to Run:

#### Step 1: Organize Some Files First
```bash
# 1. Start monitoring (see Feature 1 above)
# 2. Download a few files
# 3. Let them get organized
```

#### Step 2: Set a Reminder

**Option A: From Recent Files**
```
1. Go to "File Reminders" section in web UI
2. Step 1: Select file from dropdown
3. Step 2: Click time (30 min, 1 hour, 3 hours)
4. Click "✅ Create Reminder"
```

**Option B: Browse Any File**
```
1. Go to "File Reminders" section
2. Step 1: Click "📂 Browse Files"
3. Select any file from Finder
4. Step 2: Click time or use Custom (hours + minutes)
5. Click "✅ Create Reminder"
```

**Option C: Custom Time**
```
1. Go to "File Reminders" section
2. Step 1: Select or browse file
3. Step 2: Click "⚙️ Custom"
4. Enter hours and minutes (e.g., 2 hours 30 minutes)
5. Click "✅ Create Reminder"
```

#### Step 3: See Active Reminders
```
Scroll to "Active Reminders" section
You'll see:
├── File name
├── Reminder time
└── 🗑️ Delete button
```

#### Step 4: Get Notified
```
When time expires:
├── macOS notification appears
└── Reminder to review the file
```

### Expected Results:
- ✅ Reminder created successfully
- ✅ Shows in Active Reminders list
- ✅ Can delete anytime
- ✅ Notification at specified time

---

## 🎬 Complete Demo Flow (3 Minutes)

### Setup (30 seconds)
```bash
cd /Users/tructran/Desktop/calundergrad/hackathons/calhack12/fima
./launch_app.sh
# Click "Start Monitoring"
```

### Feature 1: Real-Time Organization (1 minute)
```
1. Open Chrome
2. Download: https://cs170.org/assets/pdf/hw07.pdf
3. Watch notification appear
4. Show organized folder in Finder
5. Show web UI update
```

### Feature 2: File Reminders (1 minute)
```
1. Scroll to File Reminders
2. Click "📂 Browse Files"
3. Select the file you just organized
4. Click "⏱️ 30 min"
5. Click "✅ Create Reminder"
6. Show in Active Reminders list
```

### Wrap Up (30 seconds)
```
1. Show Recent Operations
2. Show Lava cost tracking
3. Explain privacy features
```

---

## 🔧 Troubleshooting

### Issue: "API key not found"
```bash
# Check .env file exists
ls -la .env

# Check API key is set
cat .env | grep ANTHROPIC_API_KEY

# If missing, add it:
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

### Issue: "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements-core.txt
```

### Issue: "Port 8000 already in use"
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9

# Or use different port
python backend/main.py --port 8001
```

### Issue: "File not organizing"
```bash
# Check monitoring is active
# Web UI should show 🟢 Active

# Check terminal logs
# Should see: "🔔 New file detected: ..."

# Check API key is valid
# Try making a test API call
```

### Issue: "Permission denied"
```bash
# Grant Full Disk Access
# System Settings → Privacy & Security → Full Disk Access
# Add Terminal or your IDE
```

---

## 📊 What You Should See

### Terminal Output:
```
╔══════════════════════════════════════════════════════════════╗
║        Smart File Organizer - CalHacks 12                    ║
╚══════════════════════════════════════════════════════════════╝

🚀 Starting Smart File Organizer...
✅ API keys validated
✅ Database initialized
✅ Notification manager ready
🌐 Opening web interface...

INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### When File Downloads:
```
🔔 New file detected: hw07.pdf
🤖 Classifying file with AI...
📋 Classification: homework
📊 Confidence: 95%
📁 Suggested path: uc_berkeley/fall_2025/cs170/homework
✅ File moved to: ~/Documents/SmartFileOrganizer/uc_berkeley/fall_2025/cs170/homework/hw07.pdf
```

### Web UI:
```
📊 System Dashboard
├── Files Organized: 1
├── Total Operations: 1
├── Monitor Status: 🟢 Active
└── Avg Confidence: 95%

📋 Recent Operations
└── hw07.pdf
    ~/Downloads → ~/Documents/.../homework/
    Category: homework | Confidence: 95%
```

---

## 🎯 Key Commands

### Start App:
```bash
./launch_app.sh
```

### Stop App:
```bash
# Press Ctrl+C in terminal
```

### View Logs:
```bash
# Terminal shows real-time logs
# Or check: ~/.smart_file_organizer/logs/
```

### Reset First Launch:
```bash
rm -rf ~/.smart_file_organizer/config.json
```

### Check Database:
```bash
sqlite3 ~/.smart_file_organizer/data.db
.tables
.quit
```

---

## 📁 Important Paths

### Project Files:
```
/Users/tructran/Desktop/calundergrad/hackathons/calhack12/fima/
├── backend/          # Python backend
├── frontend/         # Web UI
├── .env             # API keys (create this!)
└── launch_app.sh    # Start script
```

### User Data:
```
~/.smart_file_organizer/
├── config.json      # User preferences
├── data.db          # SQLite database
└── audit_logs/      # Privacy audit logs
```

### Organized Files:
```
~/Documents/SmartFileOrganizer/
├── uc_berkeley/
├── work/
├── receipts/
└── misc/
```

---

## ✅ Success Checklist

Before demo:
- [ ] API key configured in .env
- [ ] Dependencies installed
- [ ] App starts without errors
- [ ] Web UI opens in browser
- [ ] Can click "Start Monitoring"
- [ ] Status shows 🟢 Active

During demo:
- [ ] Download file → organizes automatically
- [ ] Notification appears
- [ ] Web UI updates
- [ ] Can set reminder
- [ ] Reminder appears in list

---

## 🎉 You're Ready!

**Two main features**:
1. ✅ Real-time file organization
2. ✅ File reminders

**Total setup time**: 5 minutes
**Demo time**: 3 minutes
**Impact**: Maximum! 🏆

---

**Happy demoing!** 🚀
