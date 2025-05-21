# SuperSet Automator

A Streamlit application that demonstrates browser automation using Selenium with multiple fallback mechanisms for Chrome/ChromeDriver compatibility.

## Features

- Multiple driver setup approaches to ensure compatibility
- Detailed logging and error handling
- Works in Streamlit Cloud environment

## Local Development

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run app.py
   ```

## Streamlit Cloud Deployment

This application is configured to run on Streamlit Cloud with:

- `requirements.txt`: Python dependencies 
- `packages.txt`: System dependencies
- `setup.sh`: Browser and driver installation script
- `.streamlit/config.toml`: Streamlit configuration

## Troubleshooting

If you encounter ChromeDriver compatibility issues:

1. Check Chrome and ChromeDriver versions:
   ```
   google-chrome --version
   chromedriver --version
   ```
   
2. The app tries three different setup methods:
   - Standard WebDriverManager
   - Multiple fallback approaches
   - Simple Chrome setup without WebDriverManager

3. If all methods fail, check the logs for specific error messages.

## License

MIT