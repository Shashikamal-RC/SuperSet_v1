import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import subprocess

st.title("Test ChromeDriver on Streamlit Cloud")

# Get installed chromium version
chromium_version = subprocess.run(["chromium-browser", "--version"], capture_output=True, text=True).stdout.strip()
st.write(f"Chromium version detected: {chromium_version}")

# Extract major version
major_version = chromium_version.split(" ")[1].split(".")[0]

# Download matching ChromeDriver
chromedriver_version = subprocess.run(
    ["curl", "-s", f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"],
    capture_output=True,
    text=True
).stdout.strip()

st.write(f"Matching ChromeDriver version: {chromedriver_version}")

# Download ChromeDriver
subprocess.run(["wget", f"https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_linux64.zip"], check=True)
subprocess.run(["unzip", "-o", "chromedriver_linux64.zip"], check=True)
subprocess.run(["chmod", "+x", "chromedriver"], check=True)
subprocess.run(["mv", "chromedriver", "/usr/local/bin/chromedriver"], check=True)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/local/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://example.com")

st.write(f"Page title: {driver.title}")
driver.quit()
