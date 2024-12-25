import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, init

# Initialize colorama for colored terminal output
init(autoreset=True)

# Function to load payloads from a text file
def load_payloads(file_path):
    if not os.path.isfile(file_path):
        print(Fore.RED + f"Error: Payload file not found at {file_path}")
        return []
    try:
        with open(file_path, 'r') as f:
            payloads = [line.strip() for line in f.readlines() if line.strip()]
        return payloads
    except Exception as e:
        print(Fore.RED + f"Error loading payloads from file: {e}")
        return []

# Function to load URLs from a file
def load_urls(file_path):
    if not os.path.isfile(file_path):
        print(Fore.RED + f"Error: URL file not found at {file_path}")
        return []
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
        return urls
    except Exception as e:
        print(Fore.RED + f"Error loading URLs from file: {e}")
        return []

# Initialize Selenium WebDriver
def init_browser():
    options = Options()
    options.headless = True  # Set to True for headless (no UI) testing
    service = Service("/bin/chromedriver")  # Provide the correct path to chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Simulate various user actions to trigger potential XSS
def simulate_user_actions(driver, payload):
    try:
        if "<a href=" in payload:
            link = driver.find_element(By.XPATH, "//a[contains(text(), 'Click Me')]")
            link.click()
            time.sleep(1)

        if "onmouseover=" in payload or "onmousemove=" in payload:
            element = driver.find_element(By.XPATH, "//*[contains(@onmouseover, 'alert')]")
            ActionChains(driver).move_to_element(element).perform()
            time.sleep(1)

        if "onfocus=" in payload or "onkeydown=" in payload or "onkeyup=" in payload:
            input_element = driver.find_element(By.XPATH, "//input")
            input_element.send_keys("Test")
            time.sleep(1)
            input_element.send_keys(Keys.RETURN)

        if "contextmenu" in payload:
            context_element = driver.find_element(By.XPATH, "//div[@id='contextMenu']")
            ActionChains(driver).context_click(context_element).perform()
            time.sleep(1)

        if "ondblclick=" in payload:
            double_click_element = driver.find_element(By.XPATH, "//div[@id='dblclickElement']")
            ActionChains(driver).double_click(double_click_element).perform()
            time.sleep(1)

        if "<form>" in payload:
            form_element = driver.find_element(By.XPATH, "//form")
            form_element.submit()
            time.sleep(1)

    except Exception as e:
        print(Fore.RED + f"Error simulating user actions: {e}")

# Test each XSS payload
def test_xss(url, payloads, valid_results):
    driver = init_browser()
    vulnerability_count = 0  # To count valid vulnerabilities
    total_scanned = 0  # To keep track of how many payloads are scanned
    payload_idx = 0  # To iterate through the payloads

    # Continue scanning until we decide to move to the next URL
    while payload_idx < len(payloads):
        payload = payloads[payload_idx]
        test_url = f"{url}{payload}"

        print(f"Testing payload: {payload}")

        driver.get(test_url)
        time.sleep(1)

        simulate_user_actions(driver, payload)

        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            print(Fore.GREEN + f"Potential XSS found! Alert triggered at: {test_url}")
            valid_results.append(f"Alert triggered: {test_url}")
            alert.accept()  # Accept the alert to continue testing
            vulnerability_count += 1

        except Exception:
            if payload in driver.page_source:
                print(Fore.GREEN + f"Potential XSS found! Payload reflected at: {test_url}")
                valid_results.append(f"Payload reflected: {test_url}")
                vulnerability_count += 1
            else:
                print(Fore.YELLOW + "No XSS detected for this payload.")

        total_scanned += 1
        payload_idx += 1

        # After scanning two valid payloads, ask the user to continue or stop
        if vulnerability_count >= 2 and vulnerability_count % 2 == 0:
            # Only ask if 2 vulnerabilities have been found
            user_input = input(Fore.YELLOW + "Two vulnerabilities found. Continue scanning this URL? (y/n): ")
            if user_input.lower() != 'y':
                print("Moving to next URL.")
                break  # Move to the next URL

    driver.quit()

# Save valid results to a file
def save_results(valid_results):
    if valid_results:
        save_input = input(Fore.CYAN + "Do you want to save the valid results to a text file? (y/n): ")
        if save_input.lower() == 'y':
            file_name = input(Fore.CYAN + "Enter the filename to save results: ")
            try:
                with open(file_name, 'w') as file:
                    for result in valid_results:
                        file.write(result + "\n")
                print(Fore.GREEN + f"Results saved to {file_name}")
            except Exception as e:
                print(Fore.RED + f"Error saving results: {e}")
        else:
            print(Fore.YELLOW + "Results were not saved.")
    else:
        print(Fore.YELLOW + "No valid results to save.")

# Main function to handle user input for both URLs and payloads
def main():
    # Ask the user for file paths
    url_file_path = input("Enter the path to the URL file (e.g., urls.txt): ")
    payload_file_path = input("Enter the path to the payload file (e.g., payloads.txt): ")

    # Load payloads from file
    payloads = load_payloads(payload_file_path)
    if not payloads:
        return

    # Load URLs from file or ask for a single URL
    if os.path.isfile(url_file_path):
        urls = load_urls(url_file_path)
        if not urls:
            return
    else:
        urls = [url_file_path]

    # List to store valid XSS results
    valid_results = []

    # Scan each URL for XSS vulnerabilities
    for url in urls:
        print(Fore.CYAN + f"Scanning URL: {url}")
        test_xss(url, payloads, valid_results)

    # After all scans, ask to save results
    save_results(valid_results)

if __name__ == "__main__":
    main()
