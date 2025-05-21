import streamlit as st
import subprocess
import shutil
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

st.title("Selenium ChromeDriver Test on Streamlit Cloud")

# 1. Find Chrome or Chromium binary dynamically
chrome_binary = shutil.which("chromium") or shutil.which("google-chrome") or shutil.which("chromium-browser")

if not chrome_binary:
    st.error("Chrome or Chromium browser binary not found on this system.")
    st.stop()

st.write(f"Found browser binary: {chrome_binary}")

# 2. Get browser version
version_result = subprocess.run([chrome_binary, "--version"], capture_output=True, text=True)
if version_result.returncode != 0:
    st.error("Failed to get browser version")
    st.stop()

browser_version = version_result.stdout.strip()
st.write(f"Browser version: {browser_version}")

# Extract major version number for chromedriver
try:
    major_version = browser_version.split()[1].split(".")[0]
except Exception as e:
    st.error(f"Failed to parse browser version: {e}")
    st.stop()

st.write(f"Using Chrome major version: {major_version}")

# 3. Download matching ChromeDriver
chromedriver_version_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
chromedriver_version = subprocess.run(["curl", "-s", chromedriver_version_url], capture_output=True, text=True).stdout.strip()

if not chromedriver_version:
    st.error("Could not get ChromeDriver version for Chrome version.")
    st.stop()

st.write(f"ChromeDriver version to download: {chromedriver_version}")

chromedriver_zip = "chromedriver_linux64.zip"
chromedriver_url = f"https://chromedriver.storage.googleapis.com/{chromedriver_version}/{chromedriver_zip}"

if not os.path.exists(chromedriver_zip):
    st.write("Downloading ChromeDriver...")
    download_result = subprocess.run(["wget", "-q", chromedriver_url])
    if download_result.returncode != 0:
        st.error("Failed to download ChromeDriver.")
        st.stop()

# 4. Unzip and move chromedriver binary
if not os.path.exists("chromedriver"):
    st.write("Extracting ChromeDriver...")
    unzip_result = subprocess.run(["unzip", "-o", chromedriver_zip])
    if unzip_result.returncode != 0:
        st.error("Failed to unzip ChromeDriver.")
        st.stop()

st.write("Making chromedriver executable and moving it to /usr/local/bin...")
subprocess.run(["chmod", "+x", "chromedriver"])
subprocess.run(["mv", "chromedriver", "/usr/local/bin/chromedriver"])

# 5. Setup Selenium options for headless Chrome
options = Options()
options.binary_location = chrome_binary
options.add_argument("--headless=new")  # use new headless mode if supported
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

service = Service("/usr/local/bin/chromedriver")

try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://example.com")
    st.write(f"Page title is: {driver.title}")
    driver.quit()
except Exception as e:
    st.error(f"Selenium WebDriver error: {e}")
