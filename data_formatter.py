"""
Data formatter for SMP Portal scraper
Generates JPG images from scraped data
"""

# Configure matplotlib for non-GUI environments (Android, headless servers)
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
from datetime import datetime
from typing import List, Dict
import logging
import config

logger = logging.getLogger(__name__)


class DataFormatter:
    """Format and visualize scraped school data"""
    
    def __init__(self):
        # Ensure output directory exists
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    def _prepare_milk_dataframe(self, schools_data: List[Dict]) -> pd.DataFrame:
        """
        Convert scraped data into a DataFrame for Milk data only
        Filters to only show schools with TODAY's milk data
        
        Args:
            schools_data: List of school data dictionaries
        
        Returns:
            Formatted pandas DataFrame with milk data for today only
        """
        rows = []
        
        # Get today's date in the same format as portal (dd-mm-yyyy)
        today = datetime.now().strftime("%d-%m-%Y")
        logger.info(f"Filtering milk data for today's date: {today}")
        
        for school in schools_data:
            emis_name = f"{school['emis']} - {school['name']}"
            
            # Only include school if milk data exists AND matches today's date
            if school['milk'] and school['milk']['date'] == today:
                milk_row = {
                    'EMIS - School Name': emis_name,
                    'Date': school['milk']['date'],
                    'Received Quantity': school['milk']['received_quantity'],
                    'Present Stock': school['milk']['present_stock'],
                    'Consumption': school['milk']['consumption'],
                    'Remaining Balance': school['milk']['remaining_balance']
                }
                rows.append(milk_row)
            else:
                # Skip schools without today's milk data
                if school['milk']:
                    logger.debug(f"Skipping {emis_name} - milk data date is {school['milk']['date']}, not today ({today})")
                else:
                    logger.debug(f"Skipping {emis_name} - no milk data available")
        
        logger.info(f"Found {len(rows)} schools with milk data for today")
        return pd.DataFrame(rows)
    
    def _prepare_biscuit_dataframe(self, schools_data: List[Dict]) -> pd.DataFrame:
        """
        Convert scraped data into a DataFrame for Biscuit data only
        Filters to only show schools with TODAY's biscuit data
        
        Args:
            schools_data: List of school data dictionaries
        
        Returns:
            Formatted pandas DataFrame with biscuit data for today only
        """
        rows = []
        
        # Get today's date in the same format as portal (dd-mm-yyyy)
        today = datetime.now().strftime("%d-%m-%Y")
        logger.info(f"Filtering biscuit data for today's date: {today}")
        
        for school in schools_data:
            emis_name = f"{school['emis']} - {school['name']}"
            
            # Only include school if biscuit data exists AND matches today's date
            if school['biscuit'] and school['biscuit']['date'] == today:
                biscuit_row = {
                    'EMIS - School Name': emis_name,
                    'Date': school['biscuit']['date'],
                    'Received Quantity': school['biscuit']['received_quantity'],
                    'Present Stock': school['biscuit']['present_stock'],
                    'Consumption': school['biscuit']['consumption'],
                    'Remaining Balance': school['biscuit']['remaining_balance']
                }
                rows.append(biscuit_row)
            else:
                # Skip schools without today's biscuit data
                if school['biscuit']:
                    logger.debug(f"Skipping {emis_name} - biscuit data date is {school['biscuit']['date']}, not today ({today})")
                else:
                    logger.debug(f"Skipping {emis_name} - no biscuit data available")
        
        logger.info(f"Found {len(rows)} schools with biscuit data for today")
        return pd.DataFrame(rows)
    
    def _generate_single_image(self, df: pd.DataFrame, title: str, output_path: str) -> str:
        """
        Generate a single JPG image from a DataFrame
        
        Args:
            df: DataFrame with data
            title: Title for the image
            output_path: Path to save the image
        
        Returns:
            Path to the generated image file
        """
        # Handle empty DataFrame - skip file creation
        if df.empty:
            logger.warning(f"No data available for {title} - skipping file creation")
            return None
        
        # Calculate figure size based on number of rows
        num_rows = len(df)
        fig_height = max(10, num_rows * 0.35)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(15, fig_height))
        ax.axis('off')
        
        # Create table
        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            cellLoc='center',
            loc='center',
            colWidths=[0.28, 0.14, 0.14, 0.14, 0.14, 0.16]
        )
        
        # Style the table
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2.2)
        
        # Style header with better formatting
        for i in range(len(df.columns)):
            cell = table[(0, i)]
            cell.set_facecolor('#07215C')
            cell.set_text_props(weight='bold', color='white', fontsize=11, ha='center')
            cell.set_height(0.08)
        
        # Style data rows
        for i in range(1, len(df) + 1):
            for j in range(len(df.columns)):
                cell = table[(i, j)]
                
                # Alternate row colors
                if i % 2 == 1:
                    cell.set_facecolor('#f0f0f0')
                else:
                    cell.set_facecolor('white')
                
                # Bold school names
                if j == 0:
                    cell.set_text_props(weight='bold')
                
                # Highlight N/A values
                if df.iloc[i-1, j] == 'N/A':
                    cell.set_text_props(color='red', style='italic')
        
        # Add title with better formatting
        title_text = f'{title}\nGenerated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        plt.title(
            title_text,
            fontsize=18,
            fontweight='bold',
            pad=15,
            color='#07215C',
            loc='center'
        )
        
        # Adjust layout to bring title closer to table
        plt.subplots_adjust(top=0.95)
        
        # Save the figure
        plt.tight_layout()
        plt.savefig(output_path, dpi=config.IMAGE_DPI, bbox_inches='tight', format='jpg')
        plt.close()
        
        return output_path
    
    def generate_images(self, schools_data: List[Dict]) -> Dict[str, str]:
        """
        Generate separate JPG images for milk and biscuit data
        
        Args:
            schools_data: List of school data dictionaries
        
        Returns:
            Dictionary with paths to generated images {'milk': path, 'biscuit': path}
        """
        logger.info("Generating separate milk and biscuit data images...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        # Prepare milk DataFrame
        milk_df = self._prepare_milk_dataframe(schools_data)
        milk_filename = f"school_milk_data_{timestamp}.jpg"
        milk_path = os.path.join(config.OUTPUT_DIR, milk_filename)
        
        # Generate milk image (only if data exists)
        logger.info("  Creating milk data image...")
        milk_title = f"School Meal Program - Milk Data Report (Today: {timestamp})"
        milk_result = self._generate_single_image(
            milk_df,
            milk_title,
            milk_path
        )
        if milk_result:
            logger.info(f"  Milk image saved to: {milk_path}")
        
        # Prepare biscuit DataFrame
        biscuit_df = self._prepare_biscuit_dataframe(schools_data)
        biscuit_filename = f"school_biscuit_data_{timestamp}.jpg"
        biscuit_path = os.path.join(config.OUTPUT_DIR, biscuit_filename)
        
        # Generate biscuit image (only if data exists)
        logger.info("  Creating biscuit data image...")
        biscuit_title = f"School Meal Program - Biscuit Data Report (Today: {timestamp})"
        biscuit_result = self._generate_single_image(
            biscuit_df,
            biscuit_title,
            biscuit_path
        )
        if biscuit_result:
            logger.info(f"  Biscuit image saved to: {biscuit_path}")
        
        # Return only the files that were actually created
        result = {}
        if milk_result:
            result['milk'] = milk_path
        if biscuit_result:
            result['biscuit'] = biscuit_path
        
        return result


if __name__ == "__main__":
    # Test the formatter with sample data
    sample_data = [
        {
            'emis': '32120163',
            'name': 'GPS HAJWANI',
            'milk': {
                'sr': '1',
                'date': '09-12-2025',
                'received_quantity': '0',
                'present_stock': '1,431',
                'consumption': '93',
                'remaining_balance': '1,338'
            },
            'biscuit': {
                'sr': '1',
                'date': '04-12-2025',
                'received_quantity': '204',
                'present_stock': '479',
                'consumption': '91',
                'remaining_balance': '388'
            }
        },
        {
            'emis': '32120164',
            'name': 'GPS THATTA LAGHARI',
            'milk': None,
            'biscuit': None
        }
    ]
    
    formatter = DataFormatter()
    output_file = formatter.generate_image(sample_data, "test_output.jpg")
    print(f"Test image generated: {output_file}")
