# 🎬 Demo Guide - Smart File Organizer

**3-minute demo for CalHacks 12 judges**

---

## 🎯 Demo Objectives

Show judges:
1. ✅ **Downloadable software** - Real app users can install
2. ✅ **First-launch experience** - Permission, analysis, user choice
3. ✅ **Real-time organization** - Download CS170 file, watch it organize
4. ✅ **Native macOS integration** - Notifications, file system

**Total time**: 3 minutes

---

## 🔧 Setup (Before Demo)

### 1. Reset First Launch
```bash
rm -rf ~/.smart_file_organizer/config.json
```

### 2. Prepare Test File
Have ready: https://cs170.org/assets/pdf/hw07.pdf

### 3. Open Terminal
```bash
cd /Users/tructran/Desktop/calundergrad/hackathons/calhack12/fima
```

---

## 🎬 Demo Script (3 Minutes)

### **Part 1: Introduction** (20 seconds)

**Say**: 
> "Hi! I'm showing Smart File Organizer - a downloadable macOS app that uses AI to automatically organize your files. Users can download it from GitHub and install on their Mac."

**Show**: GitHub repository

---

### **Part 2: First Launch** (60 seconds)

**Do**:
```bash
./launch_app.sh
```

**What happens**:
1. **Permission Dialog** → "Grant Full Disk Access"
2. **Analysis** → "🔍 Analyzing 1,247 files..."
3. **Choice Dialog** → Click "Keep Current Structure"
4. **Notification** → "We support your choice! 💚" (top-right)
5. **Browser opens** → http://127.0.0.1:8000

**Say**: 
> "On first launch, it asks for permission, analyzes your files, and lets you choose to keep your organization or optimize it. When I choose 'Keep', it shows this supportive notification."

---

### **Part 3: Real-Time Organization** (60 seconds)

**Do**:
1. Click "Start Monitoring"
2. Download CS170 file
3. **Watch notification**: "📁 CS170_HW7.pdf → homework"
4. Open Finder → Show organized file

**Say**: 
> "Now watch it work in real-time. I'm downloading a CS170 homework file... The AI recognized it's CS170 homework and automatically moved it to the right folder. Less than 1 second!"

---

### **Part 4: Technical Highlights** (30 seconds)

**Say**: 
> "Technically: Claude AI analyzes file content, macOS FSEvents monitors in real-time, native notifications, and it's privacy-first - files stay on your computer."

**Show** (optional):
- Web UI with recent operations
- Terminal logs

---

### **Closing** (10 seconds)

**Say**: 
> "Smart File Organizer - downloadable from GitHub, never manually organize files again. Thank you!"

---

## 🎤 Key Talking Points

### What Makes This Special:
- ✅ **Real downloadable app** - Not just a demo
- ✅ **Thoughtful UX** - Respects user's organization
- ✅ **AI intelligence** - Understands context (CS170 = course)
- ✅ **Native integration** - macOS notifications, permissions
- ✅ **Privacy-first** - Files stay local, open source

---

## 🐛 Backup Plans

### If notification doesn't appear:
- Show Recent Operations in web UI

### If download is slow:
- Have pre-downloaded file ready to drag

### If permission dialog doesn't show:
- Say: "I've already granted permission"

---

## 💡 Questions Judges Might Ask

**Q: How do you handle different file types?**
**A**: Claude AI analyzes file content, name, and context. Recognizes PDFs, images, documents, code files. For PDFs, we extract text for better classification.

**Q: What if the AI makes a mistake?**
**A**: Users can toggle off anytime. All operations logged and reversible. AI learns from your existing organization.

**Q: How is this different from existing tools?**
**A**: Most tools require manual rules or are cloud-based. We use AI to understand context and work locally for privacy.

**Q: Can it work on Windows/Linux?**
**A**: Backend is cross-platform Python. Starting with macOS for native experience, Windows/Linux support planned.

**Q: How much does it cost?**
**A**: ~$0.001 per file with Claude API. For 50 files/day, that's ~$1.50/month.

**Q: Is it open source?**
**A**: Yes! Apache 2.0 license on GitHub.

---

## 📊 Demo Checklist

**Before demo**:
- [ ] Reset first launch
- [ ] Test file ready (CS170 PDF)
- [ ] Terminal open
- [ ] Browser closed
- [ ] Notifications enabled

**During demo**:
- [ ] Show GitHub
- [ ] Launch app
- [ ] Grant permissions
- [ ] Choose "Keep"
- [ ] Point to notification
- [ ] Start monitoring
- [ ] Download file
- [ ] Show organized file
- [ ] Explain technical details

---

## 🎯 Success Metrics

Judges should see:
- ✅ Real downloadable software
- ✅ Thoughtful first-launch UX
- ✅ Native macOS integration
- ✅ AI working in <1 second
- ✅ Professional execution

---

## 🚀 Final Tips

1. **Practice** 2-3 times before demo
2. **Time yourself** - aim for 2:30
3. **Speak clearly**
4. **Point to screen**
5. **Show confidence**
6. **Have fun!**

---

**Good luck at CalHacks 12!** 🏆
