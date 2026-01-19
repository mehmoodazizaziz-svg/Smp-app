# Running School Meal Program Automation on Android

## Recommended Option: Pydroid 3

**Pydroid 3 - IDE for Python 3** is the best choice for this project because:
- ✅ Built-in pip repository for easy package installation
- ✅ Supports matplotlib, pandas, and other dependencies
- ✅ Good UI for Android
- ✅ Free version works fine

### Installation Steps

#### 1. Install Pydroid 3
- Download from Google Play Store: [Pydroid 3 - IDE for Python 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3)
- Open the app and let it download the Python runtime

#### 2. Install Dependencies
In Pydroid 3, tap the menu (≡) → **Terminal** and run:

```bash
pip install requests beautifulsoup4 lxml pandas pillow matplotlib
```

**Note**: This may take 5-10 minutes on mobile. Be patient!

#### 3. Transfer Your Files
You have several options:

**Option A: GitHub (Recommended)**
1. Create a GitHub repository with your files
2. In Pydroid Terminal: `git clone <your-repo-url>`

**Option B: Google Drive/Dropbox**
1. Upload your project folder to cloud storage
2. Download to your Android device
3. Move to `/storage/emulated/0/` or accessible folder

**Option C: Direct Transfer**
1. Connect phone to PC via USB
2. Copy the entire `smp2025 scheme` folder to your phone's internal storage
3. Navigate to it in Pydroid 3 file browser

#### 4. Fix File Paths for Android
Create a new file called `config_android.py` with Android-specific paths:

```python
# Android Configuration
import os

# Portal settings
PORTAL_URL = "https://smp2025.pesrp.edu.pk"
LOGIN_URL = f"{PORTAL_URL}/login"
DETAIL_REPORT_URL = f"{PORTAL_URL}/detail-report"

# Credentials
USERNAME = "3210390175935"
PASSWORD = "12345678"

# School list (same as before)
SCHOOLS = [
    {'emis': '32120163', 'name': 'GPS HAJWANI'},
    {'emis': '32120164', 'name': 'GPS THATTA LAGHARI'},
    # ... rest of your schools
]

# Filter IDs
DISTRICT_ID = "7"
TEHSIL_ID = "124"
MARKAZ_ID = "5218"

# Android-specific output directory
# This will create output folder in Pydroid's working directory
OUTPUT_DIR = os.path.join(os.getcwd(), "output")

# Image settings
IMAGE_WIDTH = 15
IMAGE_HEIGHT = 12
IMAGE_DPI = 150  # Lower DPI for mobile (faster generation)

# Request settings
REQUEST_TIMEOUT = 30
USER_AGENT = 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36'
```

Then rename your current `config.py` to `config_windows.py` and use `config_android.py` when running on mobile.

#### 5. Fix Matplotlib Backend
Add this at the **TOP** of `data_formatter.py` (before other imports):

```python
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for Android
```

This prevents GUI errors on Android.

#### 6. Run Your Script
1. Open `main.py` in Pydroid 3
2. Tap the yellow play button (▶)
3. Check the output folder for generated images

---

## Alternative: Termux (Advanced Users)

If you want more control, use **Termux** (terminal emulator):

### Termux Installation
```bash
# Install Termux from F-Droid (NOT Play Store version)
# https://f-droid.org/en/packages/com.termux/

# Update packages
pkg update && pkg upgrade

# Install Python and dependencies
pkg install python python-pip git

# Install required packages
pip install requests beautifulsoup4 lxml pandas pillow matplotlib

# Clone/copy your project
cd ~/storage/downloads
# Copy your files here

# Run script
python main.py
```

**Pros**: More powerful, true Linux environment  
**Cons**: Steeper learning curve, command-line only

---

## Potential Issues & Solutions

### Issue 1: matplotlib Import Error
**Error**: `ImportError: cannot import name '_c_internal_utils'`

**Solution**: Use Agg backend (add to top of `data_formatter.py`):
```python
import matplotlib
matplotlib.use('Agg')
```

### Issue 2: pandas Installation Fails
**Error**: Build errors, compilation issues

**Solution**: 
- Pydroid 3 has pre-built wheels, should work automatically
- If fails, try older version: `pip install pandas==1.5.3`

### Issue 3: Output Folder Not Found
**Error**: `FileNotFoundError: output directory`

**Solution**: Folder paths differ on Android. Use:
```python
OUTPUT_DIR = os.path.join(os.getcwd(), "output")
```

### Issue 4: Slow Performance
**Cause**: Mobile processors are slower

**Solutions**:
- Lower `IMAGE_DPI` to 100-150 in config
- Reduce `IMAGE_WIDTH` and `IMAGE_HEIGHT`
- Run on WiFi for faster portal access

### Issue 5: Storage Permissions
**Error**: Can't save files

**Solution**: In Pydroid 3:
1. Go to Settings → Request Storage Permission
2. Allow storage access
3. Or save to app's internal directory

---

## Best Practices for Mobile

1. **Run on WiFi**: Portal access is data-intensive
2. **Lower Image Quality**: Set `IMAGE_DPI = 100` for faster generation
3. **Check Battery**: Keep phone plugged in or charged >50%
4. **Clear Space**: Ensure 500MB+ free storage
5. **Background Apps**: Close other apps for better performance

---

## Complete Android Setup Summary

### Quick Start (Pydroid 3)
1. ✅ Install Pydroid 3 from Play Store
2. ✅ Install packages: `pip install requests beautifulsoup4 lxml pandas pillow matplotlib`
3. ✅ Copy project files to phone
4. ✅ Add `matplotlib.use('Agg')` to top of `data_formatter.py`
5. ✅ Adjust paths in `config.py` if needed
6. ✅ Run `main.py`
7. ✅ Find output JPGs in `output/` folder

### Where to Find Output Images
In Pydroid 3:
- Menu (≡) → Open → Navigate to your project folder → `output/`
- Or use Android file manager: `Internal Storage/Pydroid/...`

Images can be:
- Shared via WhatsApp, Email, etc.
- Uploaded to Google Drive
- Viewed in any photo app

---

## Performance Expectations

**On Android (Mid-range phone)**:
- Login: ~5-10 seconds
- Data extraction (12 schools): ~2-3 minutes
- Image generation: ~10-20 seconds each
- **Total**: ~3-4 minutes per run

**On PC**:
- Total: ~2 minutes per run

---

## Automation on Android

While scheduling is beyond this guide, you can:
1. **Manual**: Open Pydroid daily and run
2. **Tasker** (advanced): Automate with Tasker app
3. **Cron** (Termux): Set up cron jobs in Termux

---

## Support & Troubleshooting

If you encounter issues:
1. Check Android version (8.0+ recommended)
2. Ensure stable internet connection
3. Verify all packages installed correctly: `pip list`
4. Check Pydroid logs for errors
5. Try clearing Pydroid cache and reinstalling packages

**Most Common Fix**: Add `matplotlib.use('Agg')` at the very top of `data_formatter.py`
