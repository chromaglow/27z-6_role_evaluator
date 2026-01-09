# 📘 HOW TO USE THIS TOOL - Simple Guide for Everyone

**A Step-by-Step Guide for Non-Technical Users**

*No coding experience needed! Just follow these simple steps.*

---

## 🎯 What This Tool Does

This tool helps you understand if your facility and job title appear in published layoff notices. It shows you:
- ✅ Whether your facility is mentioned in any notices
- ✅ Whether your job title appears at your facility
- ✅ What other job titles are affected at your facility
- ✅ Where else your job title appears

**⚠️ Important:** This tool does NOT predict if you will be laid off. It only shows what's in published public notices.

---

## 📋 What You Need Before Starting

- ✅ A Windows computer
- ✅ Python installed (we'll help you check this)
- ✅ 10 minutes of time
- ✅ Your facility code (like "SEA40" or "SEA93")
- ✅ Your job title (like "Program Manager III")

---

## 🚀 Step-by-Step Instructions

### **STEP 1: Check if Python is Installed**

1. Press the **Windows key** on your keyboard (or click the Start button)
2. Type `cmd` and press **Enter**
3. A black window will open (this is called "Command Prompt")
4. Type this exactly and press **Enter**:
   ```
   python --version
   ```

**✅ What you should see:**
- Something like `Python 3.9.7` or `Python 3.10.2`

**❌ If you see an error:**
- Python is not installed
- Download it from: https://www.python.org/downloads/
- Click the big yellow "Download Python" button
- Run the installer
- **IMPORTANT:** Check the box that says "Add Python to PATH"
- Click "Install Now"
- Close and reopen Command Prompt, then try again

---

### **STEP 2: Download the Tool**

**Option A: If you already have the files**
- Skip to Step 3

**Option B: Download from GitHub**
1. Go to: https://github.com/chromaglow/27z-6_role_evaluator
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Save it to your **Desktop**
5. Right-click the ZIP file and choose **"Extract All"**
6. Click **"Extract"**

You should now have a folder called `27z-6_role_evaluator` on your Desktop.

---

### **STEP 3: Open Command Prompt in the Right Place**

**Easy Method:**
1. Open **File Explorer** (the folder icon on your taskbar)
2. Go to your **Desktop**
3. Find the `27z-6_role_evaluator` folder
4. **Double-click** to open it
5. Click in the **address bar** at the top (where it shows the folder path)
6. Type `cmd` and press **Enter**

A black Command Prompt window will open, already in the right folder!

**Alternative Method (if the above doesn't work):**
1. Press **Windows key**
2. Type `cmd` and press **Enter**
3. Type this and press **Enter**:
   ```
   cd Desktop\27z-6_role_evaluator
   ```

---

### **STEP 4: Install Required Software (One-Time Setup)**

**You only need to do this ONCE, the first time you use the tool.**

In the Command Prompt window, type this exactly and press **Enter**:

```
python -m pip install -r requirements.txt
```

**What you'll see:**
- Text scrolling by as it installs things
- This might take 1-2 minutes
- When it's done, you'll see a new line where you can type

**⚠️ If you see "pip is not recognized":**
- This is normal! Use the command above with `python -m pip` instead of just `pip`

**If you see "python is not recognized":**
- Try: `py -m pip install -r requirements.txt`
- If that doesn't work, Python isn't installed (go back to Step 1)

---

### **STEP 5: Run the Tool**

Now you're ready! Type this command, but **replace the parts in CAPS** with your information:

```
python tools\risk_assessment.py --facility YOUR_FACILITY --title "Your Job Title"
```

**📝 Real Examples:**

**Example 1:** Someone at SEA93 who is a Program Manager III:
```
python tools\risk_assessment.py --facility SEA93 --title "Program Manager III"
```

**Example 2:** Someone at SEA40 who is a Software Development Engineer II:
```
python tools\risk_assessment.py --facility SEA40 --title "Software Development Engineer II"
```

**Example 3:** Someone who works remotely in Washington:
```
python tools\risk_assessment.py --facility REMOTE_WA --title "Product Manager II"
```

**Example 4:** Someone at SEA104 who is a Full Lifecycle Recruiter III:
```
python tools\risk_assessment.py --facility SEA104 --title "Full Lifecycle Recruiter III"
```

**💡 Important Tips:**
- Put **quotes** around job titles with spaces
- Facility codes are usually ALL CAPS (SEA93, not sea93)
- Job titles should match exactly as they appear in official documents

**Press Enter** and wait a few seconds.

---

### **STEP 6: Read Your Results**

You'll see a report that looks like this:

```
================================================================================
RISK ASSESSMENT REPORT
================================================================================
Facility: SEA93
Title:    Program Manager III

Facility Totals (Impact-Driven):
----------------------------------------
  Total Affected:    11
  Job Title Count:   5
  Notice Count:      1

Direct Match at Your Facility:
----------------------------------------
  Affected Count:    2
  Notices:           ['notice_2']

Top Titles at SEA93 (by affected count):
----------------------------------------
      5  HR Assistant II
      2  Program Manager III
      2  Product Manager II
      1  HRBP II (Field)
      1  Product Manager I

Where Else 'Program Manager III' Appears (top facilities):
----------------------------------------
      7  SEA40           notices=['notice_1', 'notice_2']
      2  SEA93           notices=['notice_2']
      1  SEA104          notices=['notice_1']

================================================================================
```

---

## 📖 Understanding Your Results

### **Section 1: Facility Totals**
This shows the overall impact at your facility:
- **Total Affected:** Total number of people at your facility mentioned in notices
- **Job Title Count:** How many different job titles are affected
- **Notice Count:** How many different notices mention your facility

### **Section 2: Direct Match at Your Facility**
This is the most important section for you:
- **Affected Count:** Number of people with your exact job title at your facility
- **Notices:** Which specific notice(s) mention this combination

**What the numbers mean:**
- **0** = Your job title is not mentioned at your facility
- **1+** = Your job title appears in the notice(s)

### **Section 3: Top Titles at Your Facility**
Shows which job titles are most affected at your facility:
- Numbers show how many people with each title
- Helps you understand the broader impact at your location

### **Section 4: Where Else Your Title Appears**
Shows other facilities where your job title is mentioned:
- Helps you see if your role is affected across multiple locations
- Numbers show how many people at each facility

---

## 🗺️ Using the Interactive Map (Optional)

The tool also includes a visual map to explore facilities.

### **How to Start the Map:**

**Option 1 (Easiest):**
In Command Prompt, type:
```
scripts\run_map.bat
```

**Option 2:**
```
powershell -ExecutionPolicy Bypass -File scripts\run_map.ps1
```

**What happens:**
- Your web browser will open automatically
- You'll see a map with facility locations marked

### **How to Use the Map:**

- **Circles on the map** = Facilities
- **Bigger circles** = More people affected
- **Click any circle** to see:
  - Facility name and code
  - Total affected count
  - Top affected job titles
- **Labels** show facility codes (like SEA40, SEA93)
- **Zoom in/out** using your mouse wheel or the +/- buttons

### **How to Close the Map:**

1. Close your web browser
2. Go back to Command Prompt
3. Press **Ctrl+C** on your keyboard
4. If asked "Terminate batch job (Y/N)?", type `Y` and press **Enter**

---

## ❓ Frequently Asked Questions

### **Q: What if I don't know my facility code?**
**A:** Your facility code is usually on your badge or in your email signature. Common codes:
- **SEA##** = Seattle area buildings (SEA20, SEA40, SEA93, etc.)
- **BFI##** = Boeing Field area facilities
- **GEG##** = Spokane area
- **REMOTE_WA** = Remote workers in Washington state

Ask your manager or HR if you're not sure.

### **Q: What if my job title has spaces or special characters?**
**A:** Always put quotes around your job title:
```
python tools\risk_assessment.py --facility SEA93 --title "Program Manager III"
```

### **Q: What if I see "File not found"?**
**A:** Make sure you're in the right folder. The Command Prompt should show something like:
```
C:\Users\YourName\Desktop\27z-6_role_evaluator>
```

If it doesn't, go back to Step 3.

### **Q: What if I see "command not found" or "python is not recognized"?**
**A:** Python might not be installed correctly. Go back to Step 1 and make sure to check "Add Python to PATH" when installing.

### **Q: Can I run this multiple times?**
**A:** Yes! You only need to do Step 4 (install) once. After that, you can run Step 5 as many times as you want with different facilities or job titles.

### **Q: Will this tell me if I'm getting laid off?**
**A:** **No.** This tool only shows what's in published public notices. It does NOT predict individual outcomes. Think of it as a way to see published information in an organized format.

### **Q: Is my information being sent anywhere?**
**A:** No. Everything runs on your computer. No data leaves your machine.

### **Q: What if my results show 0?**
**A:** This means your specific facility and job title combination is not mentioned in the notices that have been processed. This could mean:
- Your facility/title is not affected
- The data hasn't been updated yet
- Your job title might be listed differently in the notices

---

## 🆘 Troubleshooting Common Problems

### **Problem: "Python is not recognized as an internal or external command"**
**Solution:**
1. Python is not installed or not in your PATH
2. Download Python from: https://www.python.org/downloads/
3. Run the installer
4. **CHECK THE BOX** that says "Add Python to PATH"
5. Restart your computer
6. Try again from Step 1

### **Problem: "pip is not recognized"**
**Solution:**
- Instead of `pip install -r requirements.txt`
- Try: `python -m pip install -r requirements.txt`

### **Problem: "No such file or directory: data/exports/..."**
**Solution:**
- Make sure you extracted ALL files from the ZIP
- Make sure you're in the `27z-6_role_evaluator` folder
- Check that the `data` folder exists in your project folder

### **Problem: The map won't open**
**Solution:**
1. Make sure you completed Step 4 (install)
2. Try the simpler command: `scripts\run_map.bat`
3. If that doesn't work, manually open a web browser and type: `http://localhost:8000`

### **Problem: "Access is denied" or "Permission error"**
**Solution:**
- Close any programs that might be using the files
- Try running Command Prompt as Administrator:
  - Right-click on Command Prompt
  - Choose "Run as administrator"

---

## 📞 Getting Help

If you're stuck:

1. **Read this guide again** - Carefully follow each step
2. **Check the error message** - It often tells you what's wrong
3. **Ask a technical colleague** - Show them this guide and the error
4. **Try restarting** - Close everything and start from Step 3
5. **Check the INSTALL.md file** - It has more technical details

---

## 🎯 Quick Reference Card

**Print this out or keep it handy!**

**To run the tool:**
```
python tools\risk_assessment.py --facility YOUR_FACILITY --title "Your Job Title"
```

**To see the map:**
```
scripts\run_map.bat
```

**To get help:**
```
python tools\risk_assessment.py --help
```

**To stop the map:**
- Press **Ctrl+C** in Command Prompt

---

## ✅ First-Time User Checklist

Before you start:
- [ ] Python is installed
- [ ] Files are downloaded and extracted to Desktop
- [ ] I know my facility code
- [ ] I know my exact job title

During setup:
- [ ] Command Prompt is open in the right folder
- [ ] Required software is installed (Step 4 - only once)

Running the tool:
- [ ] I've run the tool successfully
- [ ] I understand my results
- [ ] I know this doesn't predict individual outcomes

---

## 💡 Pro Tips for Success

1. **Write down your info first** - Have your facility code and job title ready before you start
2. **Keep this guide open** - Refer to it as you go through the steps
3. **Don't close Command Prompt** - You can run the tool multiple times without closing it
4. **Take your time** - It's okay if it takes a few tries to get it right
5. **Ask for help** - There's no shame in asking a colleague for assistance!
6. **Bookmark this page** - You might want to run this again later

---

## 🎓 Important Reminders

- ✅ This tool shows published notice data only
- ✅ It does NOT predict individual outcomes
- ✅ Results are based on facility and job title matches
- ✅ You can run it as many times as you want
- ✅ The data comes from official public notices
- ✅ Everything runs on your computer - nothing is sent anywhere
- ✅ This is a tool for information, not prediction

---

## 📊 Example Walkthrough

Let's say you're Jane, a Program Manager III at SEA93. Here's what you'd do:

1. **Open Command Prompt** in the project folder (Step 3)
2. **Type this command:**
   ```
   python tools\risk_assessment.py --facility SEA93 --title "Program Manager III"
   ```
3. **Press Enter**
4. **Read the results:**
   - If "Affected Count: 2" appears, it means 2 Program Manager IIIs at SEA93 are mentioned
   - The notices section shows which specific notices mention this
   - The "Where Else" section shows if this title appears at other facilities

That's it! You now have the information from the published notices.

---

## 🌟 You've Got This!

This might seem complicated at first, but thousands of people use tools like this every day. Just follow the steps one at a time, and don't hesitate to ask for help if you need it.

**Remember:** This is just a tool to help you see published information in an organized way. It's not making predictions or decisions.

---

**Good luck, and take your time!** 🚀

---

*Last updated: January 2026*  
*Version: 1.0*  
*For technical support, see INSTALL.md or CONTRIBUTING.md*
