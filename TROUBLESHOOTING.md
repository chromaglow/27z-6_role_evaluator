# 🆘 Troubleshooting Guide

Common problems and how to fix them.

---

## 🗺️ Map Issues

### **Problem: "scripts\run_map.bat is not recognized"**

**Cause:** You're not in the right directory, or the file doesn't exist.

**Solution:**

1. Make sure you're in the project folder:
   ```cmd
   cd C:\Users\ezrashiv\Desktop\27z-6_role_evaluator
   ```

2. Check if the file exists:
   ```cmd
   dir scripts\run_map.bat
   ```

3. If it doesn't exist, try the PowerShell version:
   ```cmd
   powershell -ExecutionPolicy Bypass -File scripts\run_map.ps1
   ```

---

### **Problem: Map won't open in browser**

**Solution 1:** Open manually
- Start the server: `python -m http.server 8000` (from `app\public` folder)
- Open browser and go to: `http://localhost:8000`

**Solution 2:** Check if port 8000 is in use
```cmd
netstat -ano | findstr :8000
```
If something is using it, kill that process or use a different port:
```cmd
python -m http.server 8080
```
Then go to: `http://localhost:8080`

---

### **Problem: "facilities.geojson not found"**

**Cause:** Map data hasn't been generated yet.

**Solution:**
```cmd
scripts\build_map_data.bat
```

---

## 🐍 Python Issues

### **Problem: "python is not recognized"**

**Cause:** Python is not installed or not in PATH.

**Solution 1:** Check if Python is installed
```cmd
py --version
```

If that works, use `py` instead of `python`:
```cmd
py tools\risk_assessment.py --help
```

**Solution 2:** Install Python
- Download from: https://www.python.org/downloads/
- Check "Add Python to PATH" during installation
- Restart computer

---

### **Problem: "pip is not recognized"**

**Solution:** Use Python module syntax
```cmd
python -m pip install -r requirements.txt
```

Or:
```cmd
py -m pip install -r requirements.txt
```

---

### **Problem: "No module named 'pdfplumber'"**

**Cause:** Dependencies not installed.

**Solution:**
```cmd
pip install -r requirements.txt
```

Or:
```cmd
python -m pip install -r requirements.txt
```

---

## 📁 File/Path Issues

### **Problem: "No such file or directory: data/exports/..."**

**Cause:** You're not in the project root directory.

**Solution:**
```cmd
cd C:\Users\ezrashiv\Desktop\27z-6_role_evaluator
```

Check you're in the right place:
```cmd
dir
```

You should see folders: `app`, `data`, `docs`, `scripts`, `tools`

---

### **Problem: "Access is denied"**

**Cause:** File permissions or file is open in another program.

**Solution:**
1. Close any programs that might be using the files
2. Try running Command Prompt as Administrator:
   - Right-click Command Prompt
   - Choose "Run as administrator"

---

## 🔧 CLI Tool Issues

### **Problem: "File not found: data\exports\impacts_by_facility.csv"**

**Cause:** Data files haven't been generated yet.

**Solution:**
1. Make sure you have the raw data files in `data\raw\`
2. Run the data pipeline to generate exports
3. Or check if the file path is correct

---

### **Problem: Tool runs but shows no results**

**Possible causes:**
1. Facility code is wrong (check spelling/capitalization)
2. Job title doesn't match exactly
3. No data for that facility/title combination

**Solution:**
- Try a known facility: `SEA40`, `SEA93`, `SEA104`
- Try a common title: `"Program Manager III"`, `"Software Dev Engineer II"`
- Check the data files to see what's available

---

## 🌐 Network/Firewall Issues

### **Problem: "Connection refused" when accessing localhost**

**Solution:**
1. Check if firewall is blocking Python
2. Try a different port:
   ```cmd
   python -m http.server 8080
   ```
3. Check if another program is using the port

---

### **Problem: Geocoding fails or times out**

**Cause:** Rate limiting from OpenStreetMap Nominatim.

**Solution:**
1. Increase `SLEEP_SECONDS` in `tools\geocode_refresh_from_addresses.py`
2. Run the script again (it will skip already-geocoded facilities)
3. Be patient - geocoding takes time

---

## 💾 Git Issues

### **Problem: "fatal: not a git repository"**

**Cause:** You're not in a Git repository, or Git isn't initialized.

**Solution:**
```cmd
git init
git remote add origin https://github.com/chromaglow/27z-6_role_evaluator.git
```

---

### **Problem: Can't push to GitHub**

**Possible causes:**
1. Not authenticated
2. Wrong remote URL
3. No permission

**Solution:**
```cmd
git remote -v
git remote set-url origin https://github.com/chromaglow/27z-6_role_evaluator.git
```

---

## 🧪 Testing Issues

### **Problem: "pytest: command not found"**

**Cause:** pytest not installed.

**Solution:**
```cmd
pip install -r requirements-dev.txt
```

---

### **Problem: Tests fail with import errors**

**Cause:** Python path not set correctly.

**Solution:**
Run tests from project root:
```cmd
cd C:\Users\ezrashiv\Desktop\27z-6_role_evaluator
pytest
```

---

## 🎯 Quick Fixes

### **Reset Everything:**
```cmd
# Navigate to project
cd C:\Users\ezrashiv\Desktop\27z-6_role_evaluator

# Reinstall dependencies
pip install -r requirements.txt

# Rebuild map data
scripts\build_map_data.bat

# Test CLI
python tools\risk_assessment.py --help
```

---

### **Check Your Setup:**
```cmd
# Check Python
python --version

# Check pip
pip --version

# Check you're in the right folder
cd

# List files
dir
```

---

## 📞 Still Stuck?

1. **Read the error message carefully** - It usually tells you what's wrong
2. **Check which step failed** - Go back to that step in the guide
3. **Try the alternative method** - If .bat doesn't work, try .ps1
4. **Ask for help** - Show someone the exact error message

---

## 🔍 Diagnostic Commands

Run these to gather information:

```cmd
# System info
python --version
pip --version
where python
where pip

# Project structure
dir
dir scripts
dir tools
dir data\exports

# Check if files exist
dir scripts\run_map.bat
dir app\public\facilities.geojson
dir data\exports\impacts_by_facility.csv
```

Copy the output and share it when asking for help.

---

## 💡 Pro Tips

1. **Always run commands from project root** - Not from subdirectories
2. **Use Tab completion** - Type `scri` and press Tab to autocomplete
3. **Check spelling** - Commands are case-sensitive on some systems
4. **Read error messages** - They're usually helpful
5. **One step at a time** - Don't skip steps in the guides

---

**Most problems are simple fixes!** Take a deep breath and try the solutions above. 🚀
