# 📥 Download Smart File Organizer

**AI-powered file organization for macOS** - Never manually organize files again!

---

## 🚀 Quick Download

### Option 1: Download Pre-built App (Recommended)
1. Go to [Releases](https://github.com/tranngocsongtruc/fima/releases)
2. Download `SmartFileOrganizer.dmg`
3. Open the DMG file
4. Drag `SmartFileOrganizer.app` to your Applications folder
5. Double-click to launch!

### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/tranngocsongtruc/fima.git
cd fima

# Install dependencies
pip install -r requirements-core.txt

# Configure API keys (see below)
cp .env.example .env
# Edit .env with your API keys

# Run the app
python backend/main.py
```

---

## 🔑 API Keys Setup

You'll need a **Claude API key** (required):

1. Go to https://console.anthropic.com
2. Create an account and get your API key
3. Create a `.env` file in the app's Resources folder:
   ```env
   ANTHROPIC_API_KEY=your_claude_api_key_here
   ```

**Optional**: Get a Lava API key for cost tracking at https://www.lavapayments.com

---

## 🎬 First Launch Experience

When you first launch Smart File Organizer:

### 1. **Permission Request** 📋
The app will ask for permission to access your files. This is required to organize them.

**Grant Full Disk Access**:
- System Settings → Privacy & Security → Full Disk Access
- Add Smart File Organizer

### 2. **File Analysis** 🔍
The AI will analyze your existing files:
- Counts all files and folders
- Calculates organization score
- Identifies file types

### 3. **Your Choice** 💭
You'll see a dialog with two options:

#### Option A: **Keep Current Structure** ✅
- Keeps your existing folder organization
- AI will organize NEW files to match your style
- Shows supportive notification: "We support your choice! 💚"

#### Option B: **Optimize with AI** 🚀
- AI creates an optimized folder structure
- Reorganizes existing files intelligently
- Shows progress notification

---

## 📁 How It Works

### After Setup:

1. **Download any file** (e.g., CS170 homework PDF)
2. **AI analyzes** the file content instantly
3. **File moves automatically** to the right folder
4. **Notification appears** in top-right corner

### Example:
```
Download: CS170_HW7.pdf
    ↓
AI recognizes: "CS170 homework, Fall 2025"
    ↓
Moves to: ~/Documents/uc_berkeley/fall_2025/cs170/homework/
    ↓
Notification: "📁 CS170_HW7.pdf → homework"
```

---

## ✨ Features

- ✅ **AI-powered classification** - Understands context (courses, companies, projects)
- ✅ **Real-time monitoring** - Organizes files as you download them
- ✅ **Native macOS notifications** - See what's happening
- ✅ **Respects your style** - Learns from your existing organization
- ✅ **Web dashboard** - View all operations at http://localhost:8000
- ✅ **Privacy-first** - All processing happens locally

---

## 🖥️ System Requirements

- **macOS 12.0+** (Monterey or later)
- **Python 3.10+** (usually pre-installed)
- **Internet connection** (for AI API calls)
- **~500MB disk space**

---

## 🎯 Demo Flow (For Presentation)

### Setup (Before Demo):
1. Launch app for the first time
2. Grant permissions
3. Choose "Keep Current Structure"
4. See supportive notification

### Live Demo:
1. Open browser to http://localhost:8000
2. Click "Start Monitoring"
3. Download CS170 file
4. Watch notification appear
5. Show file in organized folder

**Total demo time**: ~2 minutes

---

## 🐛 Troubleshooting

### "Permission Denied" Error
**Solution**: Grant Full Disk Access in System Settings

### "API Key Not Found" Error
**Solution**: Create `.env` file with your Claude API key

### Notifications Not Showing
**Solution**: Enable notifications for Terminal/SmartFileOrganizer in System Settings

### Port 8000 Already in Use
**Solution**: Change port in `.env`: `PORT=8001`

---

## 📊 What Gets Organized

The AI recognizes and organizes:

- **📚 Academic files** - Homework, lectures, notes by course/semester
- **💼 Work documents** - By company, project, department
- **📄 Receipts** - By date and vendor
- **🖼️ Images** - By event, date, or content
- **📦 Downloads** - By type and purpose
- **📝 Documents** - By category and importance

---

## 🔒 Privacy & Security

- ✅ **Local processing** - Files stay on your computer
- ✅ **No file upload** - Only metadata sent to AI
- ✅ **API keys encrypted** - Stored securely in .env
- ✅ **Open source** - Audit the code yourself
- ✅ **No tracking** - No analytics or telemetry

---

## 🏆 Built For CalHacks 12

**Sponsors**:
- **Claude (Anthropic)** - AI file classification
- **Lava** - Cost tracking (optional)

**Tech Stack**:
- FastAPI (Python backend)
- Claude 3.5 Sonnet (AI)
- macOS FSEvents (file monitoring)
- Vanilla JavaScript (web UI)

---

## 📞 Support

**Issues?** Open an issue on GitHub: https://github.com/tranngocsongtruc/fima/issues

**Questions?** Check the [full documentation](CONSOLIDATED_GUIDE.md)

---

## 🎉 You're Ready!

Download the app and never manually organize files again!

**[Download Now →](https://github.com/tranngocsongtruc/fima/releases)**

---

## 📝 License

Apache 2.0 - Free to use, modify, and distribute

---

**Made with 💚 at CalHacks 12**
