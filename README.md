# School Meal Program - Portal Data Extraction

Automated tool to extract daily milk and biscuit data from the SMP portal and generate a JPG report.

## Features

- ✅ **No browser required** - Uses direct HTTP requests (no Selenium)
- ✅ **Automatic login** - Handles CSRF tokens and session management
- ✅ **Latest data** - Extracts the most recent entry from each table
- ✅ **Error handling** - Shows "N/A" for missing data
- ✅ **Separate outputs** - Generates distinct JPG images for milk and biscuit data
- ✅ **No serial numbers** - Omits Sr# column from output as requested

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.py` to update:
- Portal credentials (if changed)
- School list
- Output settings

## Usage

### Full Extraction (All Schools)
```bash
python main.py
```
This will:
1. Login to the portal
2. Extract data for all 12 schools
3. Generate a JPG image in the `output` folder

### Test Login Only
```bash
python main.py --test-login
```

### Test Single School
```bash
python main.py --test-single-school 32120163
```

## Output

**JPG Images**: 
- `output/school_milk_data_YYYY-MM-DD.jpg` - Milk data for all schools
- `output/school_biscuit_data_YYYY-MM-DD.jpg` - Biscuit data for all schools

Each JPG image contains:
- EMIS code and school name
- Latest entry data (date, quantities, consumption, etc.)
- "N/A" for any missing data
- **Note**: Serial number (Sr#) column is excluded

**Logs**: Displayed in console only (not saved to file)

## Files

- `main.py` - Main entry point
- `scraper.py` - Web scraping logic
- `data_formatter.py` - Image generation
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies

## Troubleshooting

**Login fails:**
- Check credentials in `config.py`
- Check internet connection
- Check if portal is accessible

**Missing data:**
- Data will show as "N/A" in the output
- Check `scraper.log` for details
- Verify the school has data on the portal

**Dependencies error:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Daily Usage

Run this script daily to get the latest data:
```bash
python main.py
```

The output file will be saved with today's date in the filename.
