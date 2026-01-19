"""
Web scraper for SMP Portal using HTTP requests
Extracts latest milk and biscuit data for all schools
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import Dict, List, Optional
import config

# Set up logging - console only
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SMPScraper:
    """Scraper for School Meal Program Portal"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        self.csrf_token = None
        
    def _get_csrf_token(self, html: str) -> Optional[str]:
        """Extract CSRF token from HTML"""
        try:
            soup = BeautifulSoup(html, 'lxml')
            csrf_input = soup.find('input', {'name': '_token'})
            if csrf_input and csrf_input.get('value'):
                return csrf_input['value']
            logger.error("CSRF token not found in page")
            return None
        except Exception as e:
            logger.error(f"Error extracting CSRF token: {e}")
            return None
    
    def login(self) -> bool:
        """
        Login to the portal and maintain session
        Returns True if successful, False otherwise
        """
        try:
            # IMPORTANT: Must visit base URL first, not /login directly!
            logger.info("Fetching portal home page to get CSRF token...")
            response = self.session.get(config.PORTAL_URL, timeout=config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            # Extract CSRF token
            self.csrf_token = self._get_csrf_token(response.text)
            if not self.csrf_token:
                logger.error("Failed to get CSRF token")
                return False
            
            logger.info("CSRF token obtained successfully")
            
            # Prepare login data
            login_data = {
                '_token': self.csrf_token,
                'emis_code': config.USERNAME,
                'password': config.PASSWORD
            }
            
            logger.info(f"Logging in with username: {config.USERNAME}")
            response = self.session.post(
                config.LOGIN_URL,
                data=login_data,
                timeout=config.REQUEST_TIMEOUT,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # Check if login was successful - should redirect to dashboard
            if 'dashboard' in response.url.lower() or config.USERNAME.upper() in response.text.upper():
                logger.info(f"Login successful! Redirected to: {response.url}")
                return True
            else:
                logger.error("Login failed - not redirected to dashboard")
                return False
                
        except requests.RequestException as e:
            logger.error(f"Login request failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            return False
    
    def _extract_latest_table_data(self, soup: BeautifulSoup, table_title: str) -> Optional[Dict]:
        """
        Extract the LAST (latest) entry from a table
        
        Args:
            soup: BeautifulSoup object of the page
            table_title: Title to search for (e.g., "Summary Date Wise (Milk)")
        
        Returns:
            Dictionary with the latest row data or None if not found
        """
        try:
            # Find the card with the specific header title
            headers = soup.find_all('h4', class_='header-title')
            target_card = None
            
            for header in headers:
                if table_title in header.text:
                    target_card = header.find_parent('div', class_='card-body')
                    break
            
            if not target_card:
                logger.warning(f"Table '{table_title}' not found")
                return None
            
            # Find the table within this card
            table = target_card.find('table')
            if not table:
                logger.warning(f"No table found in '{table_title}' section")
                return None
            
            # Get all data rows (skip header)
            tbody = table.find('tbody')
            if not tbody:
                logger.warning(f"No tbody found in '{table_title}' table")
                return None
            
            rows = tbody.find_all('tr')
            if not rows:
                logger.warning(f"No data rows found in '{table_title}' table")
                return None
            
            # Get the LAST row (latest data)
            last_row = rows[-1]
            cells = last_row.find_all('td')
            
            if len(cells) < 6:
                logger.warning(f"Incomplete data in '{table_title}' table")
                return None
            
            # Extract data from cells
            data = {
                'sr': cells[0].text.strip(),
                'date': cells[1].text.strip(),
                'received_quantity': cells[2].text.strip(),
                'present_stock': cells[3].text.strip(),
                'consumption': cells[4].text.strip(),
                'remaining_balance': cells[5].text.strip()
            }
            
            return data
            
        except Exception as e:
            logger.error(f"Error extracting data from '{table_title}': {e}")
            return None
    
    def get_school_data(self, emis_code: str, school_name: str) -> Dict:
        """
        Get latest milk and biscuit data for a specific school
        
        Args:
            emis_code: EMIS code of the school
            school_name: Name of the school
        
        Returns:
            Dictionary with school data
        """
        logger.info(f"Fetching data for {emis_code} - {school_name}")
        
        result = {
            'emis': emis_code,
            'name': school_name,
            'milk': None,
            'biscuit': None
        }
        
        try:
            # First, visit the detail-report page to get a fresh CSRF token
            logger.info("  Getting detail-report page for fresh CSRF token...")
            page_response = self.session.get(config.DETAIL_REPORT_URL, timeout=config.REQUEST_TIMEOUT)
            page_response.raise_for_status()
            
            # Extract CSRF token - try meta tag first (preferred for authenticated pages)
            soup_temp = BeautifulSoup(page_response.text, 'lxml')
            meta_csrf = soup_temp.find('meta', {'name': 'csrf-token'})
            
            if meta_csrf and meta_csrf.get('content'):
                fresh_csrf = meta_csrf.get('content')
                logger.info("  Using CSRF token from meta tag")
            else:
                # Fall back to hidden input
                fresh_csrf = self._get_csrf_token(page_response.text)
                if not fresh_csrf:
                    logger.error("  Failed to get CSRF token from detail-report page")
                    return result
                logger.info("  Using CSRF token from hidden input")
            
            # Prepare POST data to filter by school
            post_data = {
                'districtId': config.DISTRICT_ID,
                'tehsilId': config.TEHSIL_ID,
                'markazId': config.MARKAZ_ID,
                'schoolNameId': emis_code,
                'daterange': '',
                'emiscode': ''
            }
            
            # Make POST request to get school data (AJAX call)
            headers = {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': fresh_csrf,
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'text/html, */*; q=0.01',
                'Referer': config.DETAIL_REPORT_URL
            }
            
            logger.info(f"  Making AJAX request for school data...")
            response = self.session.post(
                config.DETAIL_REPORT_URL,
                json=post_data,
                headers=headers,
                timeout=config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            # Parse the response
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract milk data (last entry)
            milk_data = self._extract_latest_table_data(soup, "Summary Date Wise (Milk)")
            if milk_data:
                result['milk'] = milk_data
                logger.info(f"  Milk data: {milk_data['date']}")
            else:
                logger.warning(f"  No milk data found for {emis_code}")
            
            # Extract biscuit data (last entry)
            biscuit_data = self._extract_latest_table_data(soup, "Summary Date Wise (Biscuit)")
            if biscuit_data:
                result['biscuit'] = biscuit_data
                logger.info(f"  Biscuit data: {biscuit_data['date']}")
            else:
                logger.warning(f"  No biscuit data found for {emis_code}")
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.5)
            
        except requests.RequestException as e:
            logger.error(f"Request failed for {emis_code}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for {emis_code}: {e}")
        
        return result
    
    def scrape_all_schools(self) -> List[Dict]:
        """
        Scrape data for all schools defined in config
        
        Returns:
            List of dictionaries containing school data
        """
        logger.info("Starting to scrape all schools...")
        all_data = []
        
        for school in config.SCHOOLS:
            data = self.get_school_data(school['emis'], school['name'])
            all_data.append(data)
        
        logger.info(f"Completed scraping {len(all_data)} schools")
        return all_data


def test_login():
    """Test login functionality"""
    scraper = SMPScraper()
    success = scraper.login()
    if success:
        print("Login test passed!")
        return True
    else:
        print("Login test failed!")
        return False


def test_single_school(emis_code: str):
    """Test data extraction for a single school"""
    scraper = SMPScraper()
    
    if not scraper.login():
        print("Login failed!")
        return False
    
    # Find the school in config
    school = next((s for s in config.SCHOOLS if s['emis'] == emis_code), None)
    if not school:
        print(f"School {emis_code} not found in config!")
        return False
    
    data = scraper.get_school_data(school['emis'], school['name'])
    
    print("\n" + "="*60)
    print(f"Data for {data['emis']} - {data['name']}")
    print("="*60)
    
    if data['milk']:
        print("\nMilk Data (Latest):")
        for key, value in data['milk'].items():
            print(f"  {key}: {value}")
    else:
        print("\nMilk Data: N/A")
    
    if data['biscuit']:
        print("\nBiscuit Data (Latest):")
        for key, value in data['biscuit'].items():
            print(f"  {key}: {value}")
    else:
        print("\nBiscuit Data: N/A")
    
    print("="*60)
    return True


if __name__ == "__main__":
    # Test the scraper
    print("Testing scraper...")
    test_login()
