# Assignment2_Browserstack

Local Machine Output:
![Terminal Screenshot](https://github.com/siddhesh0309/Assignment2_Browserstack/assets/66249282/1ca2e3b7-22dd-4579-a1d9-0885508e0897)

BrowserStack Test Cases Output:
![5 PARALLEL TEST RESULT](https://github.com/siddhesh0309/Assignment2_Browserstack/assets/66249282/4f4fef50-39bb-4eb6-9981-4d08976f8fa6)

#DEMO
https://github.com/siddhesh0309/Assignment2_Browserstack/assets/66249282/63228554-ed5d-403c-ada9-c78f89cc4685



import os
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import datetime

# Set up time-based folder for downloads
time_based_subfolder = "AMFI_Performance_Reports_" + datetime.datetime.now().strftime('%Y%m%d')
download_directory = os.path.join(os.getcwd(), time_based_subfolder)

# Make sure the directory exists
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Set Chrome options to set the default download directory
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option("prefs", {
    "download.default_directory": download_directory,
    "download.directory_upgrade": True
})

# Initialize the Chrome driver
service = Service("C:/Users/45399619/Documents/AMFI/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the page
driver.get("https://www.amfiindia.com/research-information/other-data/mf-scheme-performance-details")
driver.maximize_window()
driver.delete_all_cookies()

# Switch to iframe
iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe")))
driver.switch_to.frame(iframe)

entities_list = []
sub_entities_list = []
Funds_data = []

# Extract the dropdown options
entities = driver.find_elements(By.XPATH, "/html/body/form/div/div/div[2]/div[1]/div[1]/select/option")
categories = driver.find_elements(By.XPATH, "/html/body/form/div/div/div[3]/div[1]/div[1]/select/option")
funds = driver.find_elements(By.XPATH, "/html/body/form/div/div/div[4]/div[1]/div[1]/select/option")

# Collect data from dropdowns
for i in funds:
    Funds_data.append(i.get_attribute('text'))
for i in entities:
    if i.get_attribute('text') != 'Select Category':
        entities_list.append(i.get_attribute('text'))
for i in categories:
    if i.get_attribute('text') != 'Sub Category':
        sub_entities_list.append(i.get_attribute('text'))

# Monitor and rename downloaded files
def rename_latest_file(new_name):
    # Find the latest file in the download directory
    files = sorted(os.listdir(download_directory), key=lambda x: os.path.getctime(os.path.join(download_directory, x)))
    latest_file = os.path.join(download_directory, files[-1])
    new_file_path = os.path.join(download_directory, new_name)
    
    # Rename the latest file
    os.rename(latest_file, new_file_path)

# Process entities and subcategories
for entity_index in range(len(entities_list)):
    entity_name = entities_list[entity_index]
    print(f"Processing entity: {entity_name}")
    
    for sub_index in range(len(sub_entities_list)):
        subcategory_name = sub_entities_list[sub_index]
        print(f"Processing subcategory: {subcategory_name}")
        
        try:
            # Try clicking the subcategory button and selecting a sub-entity
            subcategory_button = driver.find_element(By.XPATH, "/html/body/form/div/div/div[3]/div[1]/div[1]/button")
            subcategory_button.click()
            
            subcategory_option = driver.find_element(By.XPATH, "/html/body/div[2]/div/ul/li[" + str(sub_index + 1) + "]/a")
            subcategory_option.click()

            # Click submit to download the file
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

            # Wait for the download to complete (adjust sleep time as needed)
            time.sleep(10)

            # Rename the downloaded file
            rename_latest_file(f"{entity_name}_{subcategory_name}.xlsx")

        except Exception as e:
            print(f"Subcategory '{subcategory_name}' not found. Skipping...")

    # Reset for the next iteration
    driver.get("https://www.amfiindia.com/research-information/other-data/mf-scheme-performance-details")
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe")))
    driver.switch_to.frame(iframe)

# Close the driver when done
driver.quit()


