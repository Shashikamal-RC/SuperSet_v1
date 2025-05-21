#!/bin/bash
# filepath: c:\Users\lenovo\Documents\Freelancing\SuperSet_v1\setup.sh
set -e

echo "Setting up Chrome and ChromeDriver..."

# Install Chrome
echo "Installing Chrome..."
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get update -qq
apt-get install -qqy ./google-chrome-stable_current_amd64.deb

# Verify Chrome installation
echo "Verifying Chrome installation..."
CHROME_VERSION=$(google-chrome --version | awk '{ print $3 }' | cut -d '.' -f 1)
echo "Detected Chrome version: $CHROME_VERSION"

# Install matching ChromeDriver
echo "Installing matching ChromeDriver for Chrome $CHROME_VERSION..."
CHROMEDRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION)
echo "Matching ChromeDriver version: $CHROMEDRIVER_VERSION"

if [ -z "$CHROMEDRIVER_VERSION" ]; then
    echo "Failed to determine ChromeDriver version. Using latest version instead."
    CHROMEDRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
    echo "Latest ChromeDriver version: $CHROMEDRIVER_VERSION"
fi

wget -N -q https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
unzip -qq chromedriver_linux64.zip
chmod +x chromedriver
mv -f chromedriver /usr/local/bin/chromedriver

# Verify ChromeDriver installation
echo "Verifying ChromeDriver installation..."
INSTALLED_VERSION=$(/usr/local/bin/chromedriver --version | awk '{ print $2 }')
echo "ChromeDriver $INSTALLED_VERSION has been installed."

# Clean up
rm -f google-chrome-stable_current_amd64.deb chromedriver_linux64.zip

echo "Setup completed successfully."
