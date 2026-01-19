"""
Main entry point for SMP Portal Data Extraction
Orchestrates scraping and image generation
"""

import sys
import logging
from scraper import SMPScraper, test_login, test_single_school
from data_formatter import DataFormatter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main execution flow"""
    print("\n" + "="*70)
    print("  School Meal Program - Portal Data Extraction")
    print("="*70 + "\n")
    
    # Initialize scraper and formatter
    scraper = SMPScraper()
    formatter = DataFormatter()
    
    # Step 1: Login
    print("[1/3] Logging in to portal...")
    if not scraper.login():
        print("✗ Login failed! Please check your credentials in config.py")
        return False
    print("✓ Login successful!\n")
    
    # Step 2: Scrape all schools
    print("[2/3] Extracting data for all schools...")
    schools_data = scraper.scrape_all_schools()
    
    if not schools_data:
        print("✗ No data extracted!")
        return False
    
    # Show summary
    successful = sum(1 for s in schools_data if s['milk'] or s['biscuit'])
    print(f"✓ Data extracted for {len(schools_data)} schools")
    print(f"  - {successful} schools have data")
    print(f"  - {len(schools_data) - successful} schools missing data (will show N/A)\n")
    
    # Step 3: Generate images
    print("[3/3] Generating JPG images...")
    output_files = formatter.generate_images(schools_data)
    print(f"✓ Image generation complete!\n")
    
    print("="*70)
    if output_files:
        print(f"✓ Output files created:")
        if 'milk' in output_files:
            print(f"  Milk data:    {output_files['milk']}")
        if 'biscuit' in output_files:
            print(f"  Biscuit data: {output_files['biscuit']}")
        
        # Show which files were skipped
        if 'milk' not in output_files:
            print(f"  ⓘ Milk data:    Skipped (no data for today)")
        if 'biscuit' not in output_files:
            print(f"  ⓘ Biscuit data: Skipped (no data for today)")
    else:
        print("⚠ No files created - no schools have data for today")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test-login":
            print("\n=== Testing Login ===\n")
            test_login()
        elif sys.argv[1] == "--test-single-school" and len(sys.argv) > 2:
            emis_code = sys.argv[2]
            print(f"\n=== Testing Single School: {emis_code} ===\n")
            test_single_school(emis_code)
        else:
            print("Usage:")
            print("  python main.py                              # Run full extraction")
            print("  python main.py --test-login                 # Test login only")
            print("  python main.py --test-single-school <EMIS>  # Test single school")
            print("\nExample:")
            print("  python main.py --test-single-school 32120163")
    else:
        # Run full extraction
        success = main()
        sys.exit(0 if success else 1)
