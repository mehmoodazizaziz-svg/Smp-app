import flet as ft
import logging
import threading
import os
import time
from datetime import datetime
from scraper import SMPScraper
from data_formatter import DataFormatter
import config

# Custom logging handler to redirect logs to the GUI
class GUIHandler(logging.Handler):
    def __init__(self, log_control):
        super().__init__()
        self.log_control = log_control

    def emit(self, record):
        log_entry = self.format(record)
        self.log_control.controls.append(ft.Text(log_entry, size=12, font_family="monospace"))
        self.log_control.update()
        self.log_control.scroll_to(offset=-1, duration=100)

def main(page: ft.Page):
    page.title = "SMP Portal Data Extraction"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE

    # UI Elements
    status_text = ft.Text("Ready", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)
    progress_bar = ft.ProgressBar(width=400, color="blue", bgcolor="#eeeeee", visible=False)
    log_column = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=200, spacing=2)
    log_container = ft.Container(
        content=log_column,
        border=ft.border.all(1, ft.colors.OUTLINE),
        border_radius=5,
        padding=10,
        bgcolor=ft.colors.GREY_50
    )

    milk_image = ft.Image(src="", width=600, visible=False, fit=ft.ImageFit.CONTAIN)
    biscuit_image = ft.Image(src="", width=600, visible=False, fit=ft.ImageFit.CONTAIN)
    
    image_container = ft.Column([
        ft.Text("Generated Reports:", size=18, weight=ft.FontWeight.BOLD, visible=False),
        milk_image,
        biscuit_image
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Setup logging to GUI
    logger = logging.getLogger()
    # Remove existing handlers to avoid duplicates in GUI
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    handler = GUIHandler(log_column)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    def run_extraction(e):
        btn_run.disabled = True
        progress_bar.visible = True
        status_text.value = "Starting extraction..."
        status_text.color = ft.colors.BLUE
        log_column.controls.clear()
        milk_image.visible = False
        biscuit_image.visible = False
        image_container.controls[0].visible = False
        page.update()

        def work():
            try:
                scraper = SMPScraper()
                formatter = DataFormatter()

                logging.info("[1/3] Logging in...")
                if not scraper.login():
                    status_text.value = "Login Failed!"
                    status_text.color = ft.colors.RED
                    return

                logging.info("[2/3] Extracting data...")
                schools_data = scraper.scrape_all_schools()
                
                if not schools_data:
                    status_text.value = "No data found!"
                    status_text.color = ft.colors.ORANGE
                    return

                logging.info("[3/3] Generating images...")
                output_files = formatter.generate_images(schools_data)
                
                if output_files:
                    status_text.value = "Check complete! Reports generated."
                    status_text.color = ft.colors.GREEN
                    
                    if 'milk' in output_files:
                        milk_image.src = output_files['milk']
                        milk_image.visible = True
                    if 'biscuit' in output_files:
                        biscuit_image.src = output_files['biscuit']
                        biscuit_image.visible = True
                    
                    image_container.controls[0].visible = True
                else:
                    status_text.value = "Task finished, but no data for today."
                    status_text.color = ft.colors.BLUE_GREY

            except Exception as ex:
                logging.error(f"Error: {str(ex)}")
                status_text.value = f"Error: {str(ex)}"
                status_text.color = ft.colors.RED
            
            finally:
                btn_run.disabled = False
                progress_bar.visible = False
                page.update()

        threading.Thread(target=work, daemon=True).start()

    btn_run = ft.ElevatedButton(
        "Run Data Extraction", 
        icon=ft.icons.PLAY_ARROW, 
        on_click=run_extraction,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE,
            padding=20
        )
    )

    # Layout
    page.add(
        ft.Column([
            ft.Row([
                ft.Icon(ft.icons.SCHOOL, color=ft.colors.BLUE, size=40),
                ft.Text("SMP Portal Extraction", size=28, weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Container(height=10),
            ft.Row([btn_run], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=10),
            ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([progress_bar], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Activity Log:"),
            log_container,
            ft.Divider(),
            image_container
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)
