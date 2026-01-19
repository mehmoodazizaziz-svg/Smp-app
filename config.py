# Configuration file for SMP Portal Scraper
import os
import sys

# Detect platform
IS_MOBILE = hasattr(sys, 'getandroidapilevel') or os.environ.get('ANDROID_ROOT') is not None

# Portal credentials
PORTAL_URL = "https://smp2025.pesrp.edu.pk"
LOGIN_URL = f"{PORTAL_URL}/login"
DETAIL_REPORT_URL = f"{PORTAL_URL}/detail-report"

USERNAME = "3210390175935"
PASSWORD = "12345678"

# Filter parameters (based on the HTML provided)
DISTRICT_ID = "7"  # D.G. KHAN
TEHSIL_ID = "124"  # TAUNSA
MARKAZ_ID = "5218"  # KOT QAISRANI MALE

# Schools to extract data from
SCHOOLS = [
    {"emis": "32120163", "name": "GPS HAJWANI"},
    {"emis": "32120164", "name": "GPS THATTA LAGHARI"},
    {"emis": "32120167", "name": "GPS KOT QAISRANI NO.1"},
    {"emis": "32120168", "name": "GPS BASTI SHURNANI"},
    {"emis": "32120169", "name": "GPS SHEAHLANI GHARBI"},
    {"emis": "32120170", "name": "GPS KUKRA"},
    {"emis": "32120171", "name": "GPS CHAHPRI"},
    {"emis": "32120172", "name": "GPS SHER GARH"},
    {"emis": "32120173", "name": "GPS KOT QAISRANI NO. 2"},
    {"emis": "32120188", "name": "GPS BELWANI"},
    {"emis": "32120293", "name": "GPS HAMMAL WALI SHUMALI"},
    {"emis": "32120760", "name": "GPS BUKNA BASTI"},
]

# Request settings
REQUEST_TIMEOUT = 30  # seconds
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds between retries

# Output settings
if IS_MOBILE:
    # On mobile, we want to save in the app's internal storage or a visible folder
    # For Flet/Android, this usually works well:
    OUTPUT_DIR = os.path.join(os.getcwd(), "output")
else:
    OUTPUT_DIR = "output"

IMAGE_DPI = 150  # DPI for JPG output
IMAGE_WIDTH = 16  # inches
IMAGE_HEIGHT = 12  # inches (will auto-adjust based on data)

# User agent to mimic browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
