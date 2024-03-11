import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import configparser

# List of search terms
search_terms = ["Keyboard", "Shower Carpet", "Air Fryer"]

# Function to perform search and validate results
def test_search_box():
    # Initialize Selenium webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.canadadealsonline.com/")
    properties = read_properties('config.ini')
    search_selector_id = properties.get('search_selector')
    search_dropdown_id = properties.get('search_dropdown')
    search_results_id = properties.get('search_results')

    try:
        for term in search_terms:
            # Find search box element and enter search term
            search_box = find_element_by_data_session_id(driver, search_selector_id)
            assert search_box, "Search box not found"
            search_box.clear()
            search_box.send_keys(term)

            # Wait for search dropdown to appear
            search_dropdown = find_element_by_data_session_id(driver, search_dropdown_id)
            assert search_dropdown, "Search dropdown not found"

            # Get search results
            time.sleep(1)
            search_results = search_dropdown.find_elements(By.CSS_SELECTOR, search_results_id)

            # Check if each search term has more than 1 search result in the drop down
            assert len(search_results) > 1, f"Search term '{term}' does not have more than 1 search result"

            # Check if the search term itself appears in the 3 top options in the search results
            top_options = [result.text for result in search_results[:3]]
            assert term in top_options, f"Search term '{term}' does not appear in the top options"

            # Click on the first search result
            first_result = search_results[0]
            first_result.click()

            # Wait for page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Check if no "http 404 not found" page appears
            assert "404" not in driver.title, "HTTP 404 Not Found page appeared after clicking on the first search result"
            #back to homepage
            logo_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "max-h-34")))
            logo_element.click()
    except (TimeoutException, NoSuchElementException) as e:
        driver.save_screenshot(f"failure_screenshot_e.png")
        pytest.fail(f"Failed to perform search for term : {str(e)}")
    finally:
        # Close the browser window
        driver.quit()


def find_element_by_data_session_id(driver, session_id, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, session_id))
        )
        return element
    except TimeoutException:
        return None

def read_properties(file_path):
    try:
        config = configparser.ConfigParser()
        config.read(file_path)
        return config['selectors']
    except Exception as e:
        print(f"Error reading properties from {file_path}: {e}")
        return None
# Add a README.txt file with instructions on how to run the automation script
