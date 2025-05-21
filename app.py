import os
import subprocess
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Install Chrome and ChromeDriver if not already installed
@st.cache_resource
def install_chrome():
    try:
        st.write("🔧 Installing Chrome and ChromeDriver...")

        # Download Chrome
        subprocess.run([
            "wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
        ], check=True)

        # Update apt and install Chrome
        subprocess.run(["apt", "update"], check=True)
        subprocess.run([
            "apt", "install", "-y", "./google-chrome-stable_current_amd64.deb"
        ], check=True)

        # Get Chrome major version
        chrome_version = subprocess.check_output(
            ["google-chrome", "--version"]
        ).decode("utf-8").split(" ")[2].split(".")[0]

        # Get matching ChromeDriver version
        chrome_driver_version = subprocess.check_output([
            "curl", "-s", f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{chrome_version}"
        ]).decode("utf-8").strip()

        # Download and install ChromeDriver
        subprocess.run([
            "wget", f"https://chromedriver.storage.googleapis.com/{chrome_driver_version}/chromedriver_linux64.zip"
        ], check=True)
        subprocess.run(["unzip", "chromedriver_linux64.zip"], check=True)
        subprocess.run(["chmod", "+x", "chromedriver"], check=True)
        subprocess.run(["mv", "chromedriver", "/usr/local/bin/chromedriver"], check=True)

        st.success("✅ Chrome and ChromeDriver installed.")
    except Exception as e:
        st.error(f"Error installing Chrome/ChromeDriver: {e}")

def get_driver():
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920x1080")

    service = Service("/usr/local/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

st.title("🧪 ChromeDriver Test on Streamlit Cloud")

install_chrome()

try:
    driver = get_driver()
    driver.get("https://example.com")
    time.sleep(2)
    title = driver.title
    st.success(f"✅ ChromeDriver working! Visited page: `{title}`")
    driver.quit()
except Exception as e:
    st.error(f"❌ Something went wrong: {e}")
