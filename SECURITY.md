# 🔒 Security & Privacy Guide

**Complete security and privacy documentation**

---

## 🎯 Quick Answer

**Your files are secure because**:
- ✅ Files NEVER leave your computer
- ✅ Only metadata sent to AI (filename, size, type)
- ✅ Optional: Small PDF preview (200-500 chars)
- ✅ API keys protected (gitignored)
- ✅ 3 privacy modes available

---

## 📊 What Data is Sent to AI?

### Standard Mode (Default)
```
✅ Filename: "CS170_HW7.pdf"
✅ Extension: ".pdf"
✅ Size: "2.5 MB"
✅ MIME type: "application/pdf"
✅ PDF Preview: First 500 characters

❌ Full file content: NEVER
❌ Your file system: NEVER
❌ Personal files: NEVER
```

### Strict Mode (Most Private)
```
✅ Filename: "CS170_HW7.pdf"
✅ Extension: ".pdf"
✅ Size: "2.5 MB"
✅ MIME type: "application/pdf"

❌ PDF Preview: DISABLED
❌ Full file content: NEVER
```

### Balanced Mode (Recommended)
```
✅ Filename: "CS170_HW7.pdf"
✅ Extension: ".pdf"
✅ Size: "2.5 MB"
✅ MIME type: "application/pdf"
✅ PDF Preview: First 200 characters

❌ Full file content: NEVER
```

---

## 🔧 Configure Privacy Mode

Edit your `.env` file:

### Maximum Privacy (Strict):
```env
PRIVACY_MODE=strict
EXTRACT_PDF_TEXT=false
```

### Balanced Privacy (Recommended):
```env
PRIVACY_MODE=balanced
EXTRACT_PDF_TEXT=true
MAX_PDF_CHARS=200
```

### Best Accuracy (Standard):
```env
PRIVACY_MODE=standard
EXTRACT_PDF_TEXT=true
MAX_PDF_CHARS=500
```

---

## 📝 Enable Audit Logging

See exactly what's sent to AI:

```env
LOG_AI_REQUESTS=true
```

**Logs saved to**: `~/.smart_file_organizer/audit_logs/`

**Example log**:
```
[2025-10-26T07:30:00] AI Request:
  Filename: CS170_HW7.pdf
  Extension: .pdf
  Size: 2.5 MB
  Content Preview: 500 chars sent
  Privacy Mode: standard
```

---

## 🛡️ Security Measures

### 1. API Keys Protection
- ✅ Stored in `.env` (gitignored)
- ✅ Never committed to GitHub
- ✅ Local only
- ✅ Encrypted by macOS FileVault (if enabled)

### 2. File Content Protection
- ✅ Files NEVER uploaded
- ✅ Full content NEVER sent
- ✅ Stay on your computer
- ✅ Only you have access

### 3. Network Security
- ✅ HTTPS/TLS 1.3 encryption
- ✅ Certificate validation
- ✅ No man-in-the-middle attacks

### 4. Database Security
- ✅ SQLite (local only)
- ✅ Stores: operation logs, timestamps
- ✅ Does NOT store: file content
- ✅ Location: `~/.smart_file_organizer/`

---

## 📊 Data Retention

### On Your Computer
- **Files**: Forever (you control them)
- **Database**: Forever (or until you delete)
- **Logs**: 30 days (auto-cleanup)

### Claude API (Anthropic)
- **Request data**: 30 days, then deleted
- **Policy**: https://www.anthropic.com/legal/privacy
- **No training**: Your data NOT used to train models

### Lava API (Optional)
- **Request metadata**: As per Lava policy
- **Can disable**: Remove `LAVA_API_KEY` from `.env`

---

## ⚖️ Privacy Comparison

| Mode | Filename | Metadata | PDF Preview | Accuracy | Privacy |
|------|----------|----------|-------------|----------|---------|
| **Standard** | ✅ | ✅ | 500 chars | Highest | Good |
| **Balanced** | ✅ | ✅ | 200 chars | High | Better |
| **Strict** | ✅ | ✅ | None | Good | Best |

---

## 🔍 What Can Be Traced Back?

### ❌ Cannot Be Traced
- ❌ Your file content (never sent)
- ❌ Your file system structure (never sent)
- ❌ Your personal files (stay local)
- ❌ Your identity (API calls are anonymous)

### ⚠️ Potentially Traceable
- ⚠️ Filename (if contains personal info)
- ⚠️ PDF preview text (first 200-500 chars)
- ⚠️ API key (links requests to your account)

### ✅ How to Minimize
1. Use strict privacy mode
2. Disable PDF text extraction
3. Use generic filenames (if concerned)
4. Review audit logs regularly

---

## 🎯 Recommendations

### For General Use:
✅ **Standard mode** is fine
- Good privacy
- Best accuracy
- Anthropic is trustworthy

### For Sensitive Files:
✅ **Balanced or Strict mode**
- Less content sent
- Still good accuracy
- Maximum privacy

### For Maximum Privacy:
✅ **Strict mode + audit logging**
```env
PRIVACY_MODE=strict
EXTRACT_PDF_TEXT=false
LOG_AI_REQUESTS=true
```

---

## 🆚 Comparison with Alternatives

| Feature | Smart File Organizer | Google Drive | Dropbox | iCloud |
|---------|---------------------|--------------|---------|--------|
| **Files stay local** | ✅ | ❌ | ❌ | ❌ |
| **No cloud upload** | ✅ | ❌ | ❌ | ❌ |
| **Open source** | ✅ | ❌ | ❌ | ❌ |
| **Privacy modes** | ✅ | ❌ | ❌ | ❌ |
| **Audit logs** | ✅ | ❌ | ❌ | ❌ |

---

## ✅ Compliance

### GDPR Compliant
- ✅ Data minimization
- ✅ User control
- ✅ Right to deletion
- ✅ Transparency

### Best Practices
- ✅ Encryption in transit (TLS 1.3)
- ✅ Local-first architecture
- ✅ No unnecessary data collection
- ✅ Open source (auditable)

---

## 💡 FAQ

### Q: Can Anthropic see my files?
**A**: No. Only filename and metadata (and optional 200-500 char PDF preview) are sent. Full files never leave your computer.

### Q: Is my API key safe?
**A**: Yes. Stored in `.env` which is gitignored and never committed to GitHub.

### Q: Can I use this offline?
**A**: Not yet. AI classification requires API calls. Local AI mode is planned.

### Q: Can someone trace my files back to me?
**A**: Only if your filename contains personal info. Use generic names if concerned.

### Q: Is this HIPAA/FERPA compliant?
**A**: For sensitive data (medical, educational), use strict mode or consult your compliance officer.

---

## 🔮 Future Enhancements

Planned features:
- 🔄 **Local AI mode** - No API calls, 100% local
- 🔄 **End-to-end encryption** - Encrypt API requests
- 🔄 **Anonymization** - Hash filenames before sending
- 🔄 **Offline mode** - Work without internet

---

## 📞 Security Issues

**Report security issues**:
- GitHub: Open a private security advisory
- Response time: 48 hours

**Privacy questions**:
- Anthropic: https://www.anthropic.com/legal/privacy
- Lava: https://www.lavapayments.com/privacy

---

## 🎯 Summary

**What's Safe**:
- ✅ Files never leave your computer
- ✅ Only metadata sent to AI
- ✅ API keys protected
- ✅ Open source (auditable)
- ✅ 3 privacy modes

**What to Know**:
- ⚠️ Filenames sent to AI
- ⚠️ PDF preview (200-500 chars) sent by default
- ⚠️ Can be disabled with strict mode

**Bottom Line**:
- 🔒 More private than cloud storage
- 🔒 More transparent than closed-source
- 🔒 Configurable to your comfort level

---

**Made with 🔒 Privacy in Mind**
