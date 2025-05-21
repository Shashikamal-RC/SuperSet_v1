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

def setup_driver_v1() -> WebDriver:
    """Set up the WebDriver for browser automation."""
    try:
        logger.info("Setting up WebDriver...")
        options = webdriver.ChromeOptions()
        
        options.add_argument("--headless")  # Modern headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Use ChromeDriverManager with version detection to match the browser version
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager(cache_valid_range=1).install()), 
            options=options
        )
        
        wait = WebDriverWait(driver, 15)
        logger.info("WebDriver setup completed successfully")
        return driver
    except WebDriverException as e:
        logger.error(f"WebDriver setup failed: {e}")
        raise

def setup_driver_v2() -> WebDriver:
    """Set up the WebDriver with multiple fallback approaches."""
    try:
        logger.info("Setting up WebDriver with fallback approaches...")
        options = webdriver.ChromeOptions()
        
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Try multiple approaches to initialize the driver
        try:
            # Approach 1: Use ChromeDriverManager with cache_valid_range=0 (always get latest)
            logger.info("Trying ChromeDriverManager with latest version...")
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager(cache_valid_range=0).install()),
                options=options
            )
            logger.info("ChromeDriverManager with latest version succeeded")
            return driver
        except WebDriverException as e1:
            logger.warning(f"First approach failed: {e1}")
            try:
                # Approach 2: Try with system ChromeDriver
                logger.info("Trying with system ChromeDriver...")
                driver = webdriver.Chrome(options=options)
                logger.info("System ChromeDriver succeeded")
                return driver
            except WebDriverException as e2:
                logger.warning(f"Second approach failed: {e2}")
                # Approach 3: Last resort, try with explicit ChromeDriver for Chromium
                logger.info("Trying with explicit 'latest' version for Chromium...")
                driver = webdriver.Chrome(
                    service=ChromeService(
                        ChromeDriverManager(chrome_type="chromium").install()
                    ),
                    options=options
                )
                logger.info("Explicit version approach succeeded")
                return driver
    except Exception as e:
        logger.error(f"All WebDriver setup approaches failed: {e}")
        raise

st.title("✅ ChromeDriver Test on Streamlit Cloud")

try:
    # Try the more robust setup method first
    try:
        st.info("Attempting to initialize Chrome with enhanced fallback mechanism...")
        driver = setup_driver_v2()
    except Exception as e1:
        st.warning(f"Enhanced setup failed, falling back to basic setup: {e1}")
        driver = setup_driver_v1()
    
    # Display browser version info for debugging
    st.info("Chrome initialized successfully. Testing connection...")
    
    # Test the connection
    driver.get("https://example.com")
    time.sleep(2)
    page_title = driver.title
    
    # Show success message with browser details
    browser_version = driver.capabilities.get('browserVersion', 'unknown')
    chrome_driver_version = driver.capabilities.get('chrome', {}).get('chromedriverVersion', 'unknown')
    
    st.success(f"✅ Chrome is working! Page title: {page_title}")
    st.info(f"Browser version: {browser_version}")
    st.info(f"ChromeDriver version: {chrome_driver_version}")
    
    driver.quit()
except Exception as e:
    st.error(f"Something went wrong: {e}")
