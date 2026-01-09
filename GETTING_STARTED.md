# Getting Started (For Non-Tech Folks)

Hey! I wrote this guide for people who aren't super comfortable with code. If you can follow step-by-step instructions, you'll be fine.

---

## What You'll Need

1. **A Windows computer** (that's what I tested on)
2. **Python installed** (I'll show you how)
3. **10-15 minutes** (first time setup)

---

## Step 1: Install Python

**Check if you already have it:**
1. Press `Windows key + R`
2. Type `cmd` and press Enter
3. Type `python --version` and press Enter

If you see something like "Python 3.8" or higher, **skip to Step 2**.

**If you don't have Python:**
1. Go to https://www.python.org/downloads/
2. Click the big yellow "Download Python" button
3. Run the installer
4. **IMPORTANT:** Check the box that says "Add Python to PATH" at the bottom
5. Click "Install Now"
6. Wait for it to finish

---

## Step 2: Download This Tool

**Option A - If you have Git:**
```bash
git clone https://github.com/chromaglow/27z-6_role_evaluator.git
cd 27z-6_role_evaluator
```

**Option B - No Git? No problem:**
1. Go to the GitHub page
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file somewhere (like your Desktop)
5. Remember where you put it!

---

## Step 3: Install Dependencies

This is the part that sounds scary but isn't. We're just installing some helper libraries.

1. Open the folder where you extracted/cloned the tool
2. Hold `Shift` and right-click in the empty space
3. Click "Open PowerShell window here" (or "Open command window here")
4. Type this and press Enter:
   ```bash
   pip install -r requirements.txt
   ```
5. Wait for it to download and install stuff (takes 1-2 minutes)

You'll see a bunch of text scroll by. That's normal! Wait until you see your cursor blinking again.

---

## Step 4: Run the Map

Now the fun part!

**In the same PowerShell/command window**, type:
```bash
scripts\run_map.bat
```

You should see:
- Some text about building map data
- "Starting local web server..."
- Your browser should open automatically

If your browser doesn't open, manually go to: `http://localhost:8000`

---

## Using the Map

**You'll see a loading screen first:**
- It shows some sci-fi movie quotes (I got bored)
- Press any key to skip it
- Or wait 7 seconds

**Once the map loads:**
- **Green terminal box** (top left) - that's your control panel
- **Colored circles** - those are facilities
  - Bigger circle = more people affected
  - Red = high impact, blue = low impact
- **Legend** (top right) - shows what the colors mean

**To search for a facility:**
1. Type the facility code in the box (like "SEA40")
2. Click "EXECUTE"
3. The map will zoom to that facility

**Music:**
- Click anywhere on the map and music starts playing
- Use the "MUTE" button to turn it off
- Adjust volume with the slider

---

## Using the Command Line Tool

Want more details about a specific facility? Use the command line tool.

**In PowerShell/command window:**
```bash
python tools\risk_assessment.py --facility SEA40 --title "Program Manager"
```

Replace:
- `SEA40` with your facility code
- `"Program Manager"` with your job title (keep the quotes!)

**What you'll see:**
- Exact matches in layoff notices
- Nearby facilities with similar impacts
- The actual notice text

**Pro tip:** On the map, click a facility and use the "Copy CLI command" button. It generates the command for you!

---

## Stopping the Map

When you're done:
1. Go back to the PowerShell/command window
2. Press `Ctrl + C`
3. Type `Y` if it asks to terminate

---

## Troubleshooting

**"Python is not recognized"**
- You need to install Python (see Step 1)
- Make sure you checked "Add Python to PATH" during installation

**"pip is not recognized"**
- Same as above - reinstall Python with PATH checked

**Map won't load**
- Make sure you ran `scripts\run_map.bat`
- Check if something else is using port 8000
- Try closing and reopening your browser

**"Module not found" errors**
- Run `pip install -r requirements.txt` again
- Make sure you're in the right folder

**Music won't play**
- Click anywhere on the map first (browsers block auto-play)
- Check your browser's sound settings
- Try refreshing the page

**Still stuck?**
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more help
- Or open an issue on GitHub with details about what went wrong

---

## What the Files Mean

You don't need to understand all this, but in case you're curious:

- `app/` - The map interface
- `data/` - All the layoff notice data
- `tools/` - Python scripts that process the data
- `scripts/` - Helper scripts to run things easily
- `requirements.txt` - List of libraries needed

---

## Next Steps

Once you're comfortable:
- Try the CLI tool with different facilities
- Check out the [docs/](docs/) folder for more details
- Explore the data files in `data/exports/`

---

## A Note on the Data

All the data comes from public WARN notices (Worker Adjustment and Retraining Notification). These are legally required announcements when companies do mass layoffs.

**This tool doesn't predict anything.** It just shows you what's already been publicly announced.

---

## Questions?

If something's not clear or not working:
1. Read through this guide again (sometimes I miss stuff)
2. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. Open an issue on GitHub

I tried to make this as simple as possible, but I know everyone's computer is different. Don't hesitate to ask for help!

---

**You got this!** 💪
