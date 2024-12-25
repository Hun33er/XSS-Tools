# XSS Vulnerability Testing Tool

## Overview
This is a Python-based XSS (Cross-Site Scripting) vulnerability testing tool that uses Selenium WebDriver to automate the process of testing URLs for potential XSS vulnerabilities. The tool accepts user input for both a list of URLs and a list of XSS payloads from text files. It then tests each URL for reflected XSS vulnerabilities by injecting the payloads and checking for potential vulnerabilities such as alert pop-ups or reflected scripts.

## Features
- **Support for Single URL or Multiple URLs**: The tool can test a single URL or a list of URLs provided in a text file.
- **Support for Custom Payloads**: You can provide a custom list of XSS payloads from a text file.
- **Interactive Scanning**: After finding two valid XSS vulnerabilities, the tool asks if you want to continue scanning the current URL or move on to the next one.
- **Continuous Scanning**: If you choose to continue scanning, it will keep scanning until it finds another two valid vulnerabilities, without prompting in between.
- **Result Saving**: After the scan, you have the option to save the valid results to a text file.
- **Headless Browser**: The tool uses Selenium's headless mode for faster testing without UI pop-ups, though you can switch to non-headless mode for visibility.

## Requirements

- **Python 3.x** or higher
- **Selenium**: A Python library for controlling web browsers.
- **ChromeDriver**: Required for Selenium to interact with Google Chrome.
- **Chrome Browser**: Selenium requires Google Chrome installed to function.

## Installation

### Step 1: Install Dependencies
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/xss-testing-tool.git
   cd xss-testing-tool
   ```

2. **Install Python dependencies**:
   - Install the required Python packages using `pip`:
     ```bash
     pip install -r requirements.txt
     ```

3. **Download ChromeDriver**:
   - You will need the appropriate version of ChromeDriver that matches your installed version of Chrome. You can download it from here: [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/).
   - Ensure that the `chromedriver` binary is either placed in the same directory as this script or update the path in the script accordingly.

### Step 2: Prepare Your Input Files
1. **URLs File**:
   - Create a text file that contains one URL per line. For example, `urls.txt`:
     ```
     http://example.com/page1
     http://example.com/page2
     ```

2. **Payloads File**:
   - Create a text file containing a list of XSS payloads. For example, `payloads.txt`:
     ```
     <script>alert('XSS')</script>
     <img src="x" onerror="alert('XSS')">
     <a href="javascript:alert('XSS')">Click me</a>
     ```

### Step 3: Run the Tool
Once you've set up the files, you can run the tool with the following command:

```bash
python xss_testing_tool.py
```

- You will be prompted to enter the path to the URLs file (e.g., `urls.txt`) and the payloads file (e.g., `payloads.txt`).
- The script will scan each URL, testing the provided payloads, and will ask if you want to continue scanning after detecting two valid XSS vulnerabilities.

### Example of Tool Execution:

```bash
Enter the path to the URL file (e.g., urls.txt): urls.txt
Enter the path to the payload file (e.g., payloads.txt): payloads.txt
Testing payload: <script>alert('XSS')</script>
Potential XSS found! Alert triggered at: http://example.com/page1?q=<script>alert('XSS')</script>
Testing payload: <img src="x" onerror="alert('XSS')">
Potential XSS found! Alert triggered at: http://example.com/page1?q=<img src="x" onerror="alert('XSS')">
Two vulnerabilities found. Continue scanning this URL? (y/n): y
Testing payload: <script>alert('XSS2')</script>
Testing payload: <img src="invalid" onerror="alert('XSS')">
Two vulnerabilities found. Continue scanning this URL? (y/n): n
Moving to next URL.
```

After scanning all URLs, the tool will ask if you want to save the results to a text file.

### Save Results Option:
If you choose to save the results, you can enter a filename, and the valid results will be saved to that file.

```bash
Do you want to save the valid results to a text file? (y/n): y
Enter the filename to save results: valid_results.txt
Results saved to valid_results.txt
```

## Configuration
You can adjust the following options directly in the code:
- **Headless Mode**: By default, the browser runs in headless mode (without UI). If you'd like to see the browser in action, set `options.headless = False` in the `init_browser()` function.

## How It Works
1. **Load Input Files**: The tool loads the URLs and XSS payloads from the provided text files.
2. **Scan Each URL**: For each URL, the tool appends each payload to the URL and simulates user interactions (such as clicking links or entering input) to check for XSS vulnerabilities.
3. **Alert Checking**: If an alert is triggered or the payload is reflected in the page source, the tool detects it as a potential XSS vulnerability.
4. **Interactive Mode**: After detecting two vulnerabilities, the user is asked if they want to continue scanning the same URL or move to the next one. The tool will continue scanning until another two vulnerabilities are found.

## Contributing
Feel free to contribute to this project! If you find any bugs or have improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Notes:
1. **Replace `yourusername` in the GitHub URL** with your actual username when publishing the repo.
2. **Ensure the `requirements.txt` file includes necessary libraries**, such as `selenium`, `colorama`, and `webdriver-manager`.

This should cover the setup, functionality, and usage of your tool for GitHub. Let me know if you'd like to add or modify anything else!
