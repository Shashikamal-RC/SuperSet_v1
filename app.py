import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
    ElementClickInterceptedException
)


# Configure logging
import logging
logger = logging.getLogger("superset_automator")
logger.setLevel(logging.INFO)

def setup_driver_v1() -> None:
    """Set up the WebDriver for browser automation."""
    try:
        logger.info("Setting up WebDriver...")
        options = webdriver.ChromeOptions()
        
        options.add_argument("--headless")  # Modern headless mode
        options.add_argument("--disable-gpu")
        
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=options
        )
        
        wait = WebDriverWait(driver, 15)
        logger.info("WebDriver setup completed successfully")
    except WebDriverException as e:
        logger.error(f"WebDriver setup failed: {e}")
        raise

st.title("✅ ChromeDriver Test on Streamlit Cloud")

try:
    driver = setup_driver_v1()
    driver.get("https://example.com")
    time.sleep(2)
    page_title = driver.title
    st.success(f"Chrome is working! Page title: {page_title}")
    driver.quit()
except Exception as e:
    st.error(f"Something went wrong: {e}")
