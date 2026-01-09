# 🎯 Common Commands - Quick Reference

**Print this out or keep it handy!**

---

## 📦 Installation Commands

### **Install Dependencies (First Time)**
```cmd
python -m pip install -r requirements.txt
```

**Alternative if above doesn't work:**
```cmd
py -m pip install -r requirements.txt
```

---

## 🔍 Check Your Setup

### **Check Python Version**
```cmd
python --version
```

**Alternative:**
```cmd
py --version
```

### **Check pip Version**
```cmd
python -m pip --version
```

### **List Installed Packages**
```cmd
python -m pip list
```

---

## 🛠️ Running the Tool

### **Run Risk Assessment**
```cmd
python tools\risk_assessment.py --facility YOUR_FACILITY --title "Your Job Title"
```

**Example:**
```cmd
python tools\risk_assessment.py --facility SEA93 --title "Program Manager III"
```

### **Get Help**
```cmd
python tools\risk_assessment.py --help
```

### **Run with Verbose Output**
```cmd
python tools\risk_assessment.py --facility SEA93 --title "Program Manager III" --verbose
```

---

## 🗺️ Map Commands

### **Launch the Map (Easiest)**
```cmd
scripts\run_map.bat
```

### **Launch the Map (PowerShell)**
```cmd
powershell -ExecutionPolicy Bypass -File scripts\run_map.ps1
```

### **Build Map Data Only**
```cmd
scripts\build_map_data.bat
```

### **Start Server Manually**
```cmd
cd app\public
python -m http.server 8000
```

Then open browser to: `http://localhost:8000`

**Stop the server:** Press `Ctrl+C`

---

## 🧪 Testing Commands

### **Run All Tests**
```cmd
pytest
```

### **Run Tests with Verbose Output**
```cmd
pytest -v
```

### **Run Tests with Coverage**
```cmd
pytest --cov=tools --cov-report=html
```

### **Run Specific Test File**
```cmd
pytest tests\test_risk_assessment.py
```

---

## 📁 Navigation Commands

### **Go to Project Folder**
```cmd
cd C:\Users\ezrashiv\Desktop\27z-6_role_evaluator
```

### **Check Current Location**
```cmd
cd
```

### **List Files**
```cmd
dir
```

### **List Files in Subfolder**
```cmd
dir scripts
dir tools
dir data\exports
```

---

## 🔧 Troubleshooting Commands

### **Check if File Exists**
```cmd
dir scripts\run_map.bat
dir data\exports\impacts_by_facility.csv
```

### **Find Python Location**
```cmd
where python
```

### **Find pip Location**
```cmd
where pip
```

### **Check What's Using Port 8000**
```cmd
netstat -ano | findstr :8000
```

### **Reinstall Dependencies**
```cmd
python -m pip install --upgrade -r requirements.txt
```

---

## 📊 Git Commands

### **Check Status**
```cmd
git status
```

### **Add Files**
```cmd
git add .
```

### **Commit Changes**
```cmd
git commit -m "Your message here"
```

### **Push to GitHub**
```cmd
git push origin main
```

### **Pull Latest Changes**
```cmd
git pull origin main
```

---

## 💡 Pro Tips

### **Use Tab Completion**
Type `scri` and press **Tab** to autocomplete to `scripts\`

### **Use Up Arrow**
Press **Up Arrow** to see previous commands

### **Copy from Command Prompt**
Right-click to copy selected text

### **Paste into Command Prompt**
Right-click to paste

### **Clear Screen**
```cmd
cls
```

### **Exit Command Prompt**
```cmd
exit
```

---

## 🎯 Most Common Commands

**90% of the time, you'll use these:**

```cmd
# 1. Navigate to project
cd C:\Users\ezrashiv\Desktop\27z-6_role_evaluator

# 2. Install dependencies (first time only)
python -m pip install -r requirements.txt

# 3. Run the tool
python tools\risk_assessment.py --facility SEA93 --title "Program Manager III"

# 4. Launch the map
scripts\run_map.bat
```

---

## 🆘 When Things Go Wrong

### **"pip is not recognized"**
→ Use: `python -m pip` instead of `pip`

### **"python is not recognized"**
→ Try: `py` instead of `python`
→ Or install Python from python.org

### **"No such file or directory"**
→ Check you're in the right folder: `cd`
→ Navigate to project: `cd C:\Users\ezrashiv\Desktop\27z-6_role_evaluator`

### **"Permission denied"**
→ Close programs that might be using the files
→ Try running Command Prompt as Administrator

### **"Port already in use"**
→ Use a different port: `python -m http.server 8080`
→ Or find and kill the process using port 8000

---

## 📞 Need More Help?

- **Full troubleshooting:** See `TROUBLESHOOTING.md`
- **Complete guide:** See `HOW_TO_USE_THIS_TOOL.md`
- **Quick start:** See `QUICK_START.md`

---

**Keep this handy for quick reference!** 📋
