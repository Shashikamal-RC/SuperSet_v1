import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

def get_driver():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920x1080")

    # Explicit path to ChromeDriver
    service = Service("/usr/local/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

st.title("✅ ChromeDriver Test on Streamlit Cloud")

try:
    driver = get_driver()
    driver.get("https://example.com")
    time.sleep(2)
    page_title = driver.title
    st.success(f"Chrome is working! Page title: {page_title}")
    driver.quit()
except Exception as e:
    st.error(f"Something went wrong: {e}")
