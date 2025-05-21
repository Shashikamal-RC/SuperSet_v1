#!/bin/bash
# filepath: c:\Users\lenovo\Documents\Freelancing\SuperSet_v1\setup.sh
# More robust setup script that tries multiple methods

# Exit on errors, but not if a command fails
set -e

echo "=================================="
echo "Setting up Chrome and ChromeDriver"
echo "=================================="

install_chrome() {
    echo "[1/4] Installing Chrome..."
    apt-get update -qq
    apt-get install -qqy chromium-browser || {
        echo "Chromium install failed, trying Google Chrome..."
        wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        apt-get install -qqy ./google-chrome-stable_current_amd64.deb
        rm -f google-chrome-stable_current_amd64.deb
    }
    
    # Detect which browser is installed
    if command -v google-chrome > /dev/null; then
        CHROME_CMD="google-chrome"
    elif command -v chromium-browser > /dev/null; then
        CHROME_CMD="chromium-browser"
    else
        echo "ERROR: No Chrome/Chromium browser installed!"
        return 1
    fi
    
    # Get browser version
    CHROME_VERSION=$($CHROME_CMD --version | awk '{ print $2 }' | cut -d '.' -f 1)
    if [ -z "$CHROME_VERSION" ]; then
        CHROME_VERSION=$($CHROME_CMD --version | awk '{ print $3 }' | cut -d '.' -f 1)
    fi
    
    echo "Detected browser version: $CHROME_VERSION"
    return 0
}

install_chromedriver_method1() {
    echo "[2/4] Installing ChromeDriver (Method 1)..."
    
    # Try to get matching version
    CHROMEDRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION)
    
    if [ -z "$CHROMEDRIVER_VERSION" ]; then
        echo "Failed to get matching version, trying latest..."
        CHROMEDRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
    fi
    
    if [ -z "$CHROMEDRIVER_VERSION" ]; then
        echo "Failed to determine ChromeDriver version."
        return 1
    fi
    
    echo "Installing ChromeDriver version: $CHROMEDRIVER_VERSION"
    wget -N -q https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
    unzip -o -qq chromedriver_linux64.zip
    chmod +x chromedriver
    mv -f chromedriver /usr/local/bin/chromedriver
    rm -f chromedriver_linux64.zip
    
    # Verify
    if command -v chromedriver > /dev/null; then
        echo "ChromeDriver installed successfully: $(chromedriver --version)"
        return 0
    else
        echo "ChromeDriver installation failed."
        return 1
    fi
}

install_chromedriver_method2() {
    echo "[3/4] Installing ChromeDriver (Method 2 - package manager)..."
    apt-get update -qq
    apt-get install -qqy chromium-driver || {
        echo "Package manager installation failed."
        return 1
    }
    
    # Verify
    if command -v chromedriver > /dev/null; then
        echo "ChromeDriver installed successfully: $(chromedriver --version)"
        return 0
    else
        echo "ChromeDriver installation failed."
        return 1
    fi
}

setup_python_dependencies() {
    echo "[4/4] Setting up Python dependencies..."
    pip install --upgrade pip
    pip install --no-cache-dir -r requirements.txt
    echo "Python dependencies installed."
}

# Main installation flow
install_chrome

# Try multiple methods for ChromeDriver
if ! install_chromedriver_method1; then
    echo "First method failed, trying alternative method..."
    if ! install_chromedriver_method2; then
        echo "WARNING: All ChromeDriver installation methods failed."
        echo "The application will try to use the system ChromeDriver or fallback methods."
    fi
fi

# Setup Python dependencies
setup_python_dependencies

echo "=================================="
echo "Setup completed!"
echo "Chrome/Chromium: $($CHROME_CMD --version)"
if command -v chromedriver > /dev/null; then
    echo "ChromeDriver: $(chromedriver --version)"
else
    echo "ChromeDriver: Not found (will try fallback methods)"
fi
echo "=================================="
