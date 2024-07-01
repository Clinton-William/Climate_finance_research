from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Configure Chrome options to set the download directory
download_dir = '/Users/clinton/Downloads/csv'  # Replace with your desired download directory
chrome_options = webdriver.ChromeOptions()
prefs = {
    'download.default_directory': download_dir,
    'download.prompt_for_download': False,
    'directory_upgrade': True,
    'safebrowsing.enabled': True
}
chrome_options.add_experimental_option('prefs', prefs)

# Set up the WebDriver with options
driver = webdriver.Chrome(options=chrome_options)

# Open the website
website_url = 'https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series/1/tavg/12/4/1895-2024?base_prd=true&begbaseyear=1901&endbaseyear=2000'
driver.get(website_url)

# Wait for the dropdowns to be present
wait = WebDriverWait(driver, 10)

# Set the timescale year dropdown
timescale_dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#timescale')))
timescale_select = Select(driver.find_element(By.CSS_SELECTOR, '#timescale'))
timescale_select.select_by_value('1')

# Set the month dropdown
month_dropdown=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#month')))
month_select=Select(driver.find_element(By.CSS_SELECTOR,'#month'))
month_select.select_by_value('0')

# Set the end year dropdown
beg_year_dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#begyear')))
beg_year_select = Select(driver.find_element(By.CSS_SELECTOR, '#begyear'))
beg_year_select.select_by_value('1980')

# Set the end year dropdown
end_year_dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#endyear')))
end_year_select = Select(driver.find_element(By.CSS_SELECTOR, '#endyear'))
end_year_select.select_by_value('2024')

plot_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))


# Wait for the state dropdown to be present
dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#location')))

# Find the state dropdown menu element
dropdown = Select(driver.find_element(By.CSS_SELECTOR, '#location'))

# Function to rename the latest downloaded file
def rename_latest_file(state_name, download_dir):
    # Wait for a short period to ensure the file is downloaded
    time.sleep(5)
    # Get a list of files in the download directory
    files = os.listdir(download_dir)
    # Find the latest file
    files.sort(key=lambda x: os.path.getmtime(os.path.join(download_dir, x)), reverse=True)
    latest_file = files[0]
    # Create a new filename based on the state name
    new_filename = f"{state_name}.csv"
    # Rename the file
    os.rename(os.path.join(download_dir, latest_file), os.path.join(download_dir, new_filename))

# Iterate through each option in the state dropdown menu
for option in dropdown.options:
    state_name = option.text

    
    # Select the option
    dropdown.select_by_visible_text(state_name)

    # Wait for the page to update
    time.sleep(2)

    # Find the download CSV button and ensure it's clickable
    download_button = wait.until(EC.element_to_be_clickable((By.ID, 'csv-download')))

    plot_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
    
    # Scroll to the download button to ensure it is visible
    driver.execute_script("arguments[0].scrollIntoView(true);", download_button)

    # Try clicking the button, using JavaScript click as a fallback
    try:
        plot_button.click()
        
        download_button.click()
    except:
        driver.execute_script("arguments[0].click();",plot_button)
        driver.execute_script("arguments[0].click();", download_button)

    # Rename the latest downloaded file
    rename_latest_file(state_name, download_dir)

# Close the WebDriver
driver.quit()