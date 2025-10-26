# 🎬 Demo Guide - Smart File Organizer

**Complete walkthrough for your CalHacks 12 demo**

---

## 🎯 Demo Objectives

Show judges:
1. ✅ **Downloadable software** - Real app users can install
2. ✅ **First-launch experience** - Permission request, analysis, user choice
3. ✅ **Real-time organization** - Download CS170 file, watch it organize
4. ✅ **Native macOS integration** - Notifications, file system

**Total demo time**: 3 minutes

---

## 🔧 Setup (Before Demo)

### 1. Reset First Launch (to show it fresh)
```bash
rm -rf ~/.smart_file_organizer/config.json
```

### 2. Prepare Test File
Have this link ready: https://cs170.org/assets/pdf/hw07.pdf
(Or any CS170-related PDF)

### 3. Clean Downloads Folder
```bash
# Optional: Clean Downloads to show organization clearly
```

### 4. Have Terminal Ready
```bash
cd /Users/tructran/Desktop/calundergrad/hackathons/calhack12/fima
```

---

## 🎬 Demo Script (3 Minutes)

### Part 1: Introduction (20 seconds)

**Say**: 
> "Hi! I'm going to show you Smart File Organizer - a downloadable macOS app that uses AI to automatically organize your files. This isn't just a web tool - it's a real application that users can download from GitHub and install on their Mac."

**Show**: 
- GitHub repository page
- Point to "Download" section

---

### Part 2: First Launch Experience (60 seconds)

**Say**: 
> "Let me show you what happens when someone downloads and launches the app for the first time."

**Do**:
```bash
./launch_app.sh
```

**What happens**:
1. **Permission Dialog appears** (macOS system dialog)
   - **Say**: "First, the app requests permission to access files - this is required to organize them."
   - Click "Open Settings" or "OK"

2. **Analysis runs** (in terminal)
   - **Say**: "The AI analyzes your existing files to understand your organization style."
   - Shows: "🔍 Analyzing your files..."
   - Shows: "📊 Found X files, Y folders, organization score: Z/100"

3. **Choice Dialog appears** (macOS dialog)
   - **Say**: "Now it asks: do you want to keep your current organization, or let AI optimize it?"
   - Shows two buttons: "Keep Current Structure" | "Optimize with AI"
   - **Click**: "Keep Current Structure"

4. **Supportive Notification** (top-right corner)
   - **Say**: "And here's the supportive notification - 'We support your choice! 💚'"
   - **Point to notification** in top-right corner

5. **Browser opens** automatically to http://127.0.0.1:8000
   - **Say**: "The web dashboard opens automatically"

---

### Part 3: Real-Time Organization (60 seconds)

**Say**: 
> "Now the app is monitoring my Downloads folder. Watch what happens when I download a CS170 homework file."

**Do**:
1. **Click "Start Monitoring"** in web UI
   - Status changes to 🟢 Monitoring

2. **Open new browser tab**
   - Go to: https://cs170.org/assets/pdf/hw07.pdf
   - Or: Have file ready to drag into Downloads

3. **Download the file**
   - **Say**: "I'm downloading CS170 homework 7..."

4. **Watch the magic** (happens in <1 second):
   - **Notification appears** (top-right):
     ```
     📁 Smart File Organizer
     CS170_HW7.pdf → homework
     Moved to: uc_berkeley/fall_2025/cs170/homework/
     ```
   - **Point to notification**
   - **Say**: "The AI recognized this is CS170 homework and automatically moved it to the right folder!"

5. **Show the organized file**:
   - Open Finder
   - Navigate to: `~/Documents/SmartFileOrganizer/uc_berkeley/fall_2025/cs170/homework/`
   - **Say**: "And here it is - perfectly organized!"

---

### Part 4: Technical Highlights (30 seconds)

**Say**: 
> "Technically, here's what's happening:"

**Points to emphasize**:
- ✅ **Claude AI** analyzes file content and context
- ✅ **Real-time monitoring** using macOS FSEvents
- ✅ **Native notifications** using macOS APIs
- ✅ **<1 second** from download to organized
- ✅ **Privacy-first** - files stay on your computer

**Show** (optional):
- Web UI showing recent operations
- Terminal logs showing AI classification

---

### Part 5: Downloadable Software (20 seconds)

**Say**: 
> "And the best part - this is real software that anyone can download."

**Show**:
- GitHub releases page
- **Say**: "Users can download the .dmg file, drag it to Applications, and start using it immediately."
- **Say**: "No app store approval needed - it's open source on GitHub."

---

### Closing (10 seconds)

**Say**: 
> "Smart File Organizer - never manually organize files again. Thank you!"

**Show**: 
- Web UI with statistics
- Or: Organized folder structure

---

## 🎤 Key Talking Points

### What Makes This Special:

1. **Real Downloadable App**
   - Not just a demo - users can actually download and use it
   - Available on GitHub releases
   - No app store needed

2. **Thoughtful UX**
   - Asks for permission properly
   - Respects user's existing organization
   - Supportive, not pushy

3. **AI Intelligence**
   - Understands context (CS170 = course, homework = assignment type)
   - Creates logical folder structures
   - Learns from your style

4. **Native Integration**
   - macOS notifications
   - File system monitoring
   - Feels like a real Mac app

5. **Privacy-First**
   - Files stay local
   - Only metadata sent to AI
   - Open source - audit the code

---

## 🐛 Backup Plans

### If notification doesn't appear:
- **Say**: "The notification should appear here, but you can see it worked in the web UI"
- Show Recent Operations in web UI

### If download is slow:
- Have a pre-downloaded file ready
- Drag it into Downloads folder manually

### If permission dialog doesn't show:
- **Say**: "On first launch, macOS asks for permission - I've already granted it"
- Continue with analysis

### If browser doesn't open:
- Open manually: http://127.0.0.1:8000
- **Say**: "The web dashboard provides a visual interface"

---

## 💡 Questions Judges Might Ask

**Q: How do you handle different file types?**
**A**: Claude AI analyzes file content, name, and context. It recognizes PDFs, images, documents, code files, and more. For PDFs, we extract text for better classification.

**Q: What if the AI makes a mistake?**
**A**: Users can toggle monitoring off anytime. All operations are logged and reversible. Plus, the AI learns from your existing organization style.

**Q: How is this different from existing tools?**
**A**: Most tools require manual rules or are cloud-based. We use AI to understand context (like recognizing "CS170" as a course) and work entirely locally for privacy.

**Q: Can it work on Windows/Linux?**
**A**: The backend is cross-platform Python. We're starting with macOS for the native experience, but Windows/Linux support is planned.

**Q: How much does it cost to run?**
**A**: About $0.001 per file with Claude API. For typical usage (50 files/day), that's ~$1.50/month. We're exploring local models to reduce costs.

**Q: Is it open source?**
**A**: Yes! Apache 2.0 license. Code is on GitHub for anyone to audit, modify, or contribute to.

---

## 📊 Demo Checklist

Before demo:
- [ ] Reset first launch: `rm -rf ~/.smart_file_organizer/config.json`
- [ ] Test file ready (CS170 PDF link)
- [ ] Terminal open to project directory
- [ ] Browser closed (so it opens fresh)
- [ ] Downloads folder visible in Finder
- [ ] Notifications enabled in System Settings

During demo:
- [ ] Show GitHub repository
- [ ] Launch app: `./launch_app.sh`
- [ ] Grant permissions
- [ ] Choose "Keep Current Structure"
- [ ] Point to supportive notification
- [ ] Click "Start Monitoring"
- [ ] Download CS170 file
- [ ] Point to notification
- [ ] Show organized file in Finder
- [ ] Explain technical details
- [ ] Show GitHub releases page

---

## 🎯 Success Metrics

Judges should see:
- ✅ Real downloadable software (not just a demo)
- ✅ Thoughtful first-launch experience
- ✅ Native macOS integration
- ✅ AI working in real-time (<1 second)
- ✅ Professional UI and notifications
- ✅ Privacy-first approach

---

## 🚀 Final Tips

1. **Practice the flow** 2-3 times before demo
2. **Time yourself** - aim for 2:30 to leave buffer
3. **Speak clearly** - judges are listening
4. **Point to screen** - help judges follow along
5. **Show confidence** - you built something real!
6. **Have fun** - this is cool tech!

---

## 🎉 You're Ready!

You have:
- ✅ Real downloadable app
- ✅ First-launch experience
- ✅ Real-time file organization
- ✅ Native macOS integration
- ✅ Professional demo flow

**Go win CalHacks 12!** 🏆
