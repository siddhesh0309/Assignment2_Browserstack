import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time


OptionsToSelect = ChromeOptions()
ChromeWebDriver = webdriver.Chrome(options=OptionsToSelect)

try:
    ChromeWebDriver.get("https://www.flipkart.com")

    
    SearchElement = ChromeWebDriver.find_element("name", "q")
    SearchElement.send_keys("Samsung Galaxy S10")
    SearchElement.send_keys(Keys.RETURN)

    WebDriverWait(ChromeWebDriver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tUxRFH"))
    )

    ChromeWebDriver.find_element("link text", "Mobiles").click()

    FilterSamsung = WebDriverWait(ChromeWebDriver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[1]/div[1]/div/div[1]/div/section[3]/div[2]/div/div/div/label/div[1]"))
    )
    FilterSamsung.click()
    time.sleep(10)

    FilterChange = WebDriverWait(ChromeWebDriver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[1]/div[1]/div/div[1]/div/section[4]/label/div[1]"))
    )
    FilterChange.click()
    time.sleep(5)


    HighToLow_Filter = WebDriverWait(ChromeWebDriver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[1]/div[2]/div[1]/div/div/div[3]/div[4]"))
    )
    HighToLow_Filter.click()
    time.sleep(10)
    


    ChromeWebDriver.implicitly_wait(5)
    ProductElement = ChromeWebDriver.find_elements(By.CLASS_NAME, "tUxRFH")
    ProductList = []

    for Product_Elements in ProductElement:
        ProductName = Product_Elements.find_element(By.CLASS_NAME, "KzDlHZ").text
        PriceDisplay = Product_Elements.find_element(By.CLASS_NAME, "Nx9bqj._4b5DiR").text
        ProductURL = Product_Elements.find_element(By.TAG_NAME, "a").get_attribute("href")

        ProductDictionary = {
            "Product Name": ProductName,
            "Display Price": PriceDisplay,
            "Link to Product Details Page": ProductURL
        }

        ProductList.append(ProductDictionary) 
    with open("product_list.txt", "w") as file:
        for ProductDictionary in ProductList:
            file.write(json.dumps(ProductDictionary) + "\n")      

    
    for ProductDictionary in ProductList:
        print(ProductDictionary)
except NoSuchElementException as err:
    print('Exception: ', err)
except Exception as err:
    print('Exception: ', err)
finally:
    
    ChromeWebDriver.quit()










import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup the WebDriver using Service
service = Service('C:/Users/SIDDHESH/OneDrive/Desktop/HSBC DOC/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)

try:
    # Navigate to the webpage
    driver.get('https://www.amfiindia.com/research-information/other-data/mf-scheme-performance-details')

    # Wait until the iframe is present and switch to it
    wait = WebDriverWait(driver, 10)
    iframe = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[5]/div[2]/iframe")))
    driver.switch_to.frame(iframe)

    # XPaths for dropdowns and buttons
    first_dropdown_xpath = "/html[1]/body[1]/form[1]/div[1]/div[1]/div[2]/div[1]/div[1]"  # Adjust if needed
    second_dropdown_xpath = "/html[1]/body[1]/form[1]/div[1]/div[1]/div[3]/div[1]/div[1]"  # Adjust if needed
    go_button_xpath = "//button[normalize-space()='Go']"
    download_button_xpath = "//small[normalize-space()='Download Excel']"

    # Get all options from the first dropdown
    first_options = wait.until(EC.presence_of_all_elements_located((By.XPATH, first_dropdown_xpath)))

    for first_option in first_options:
        first_option_text = first_option.text.strip()
        if first_option.is_displayed() and first_option.is_enabled():
            print(f"Selecting first option: {first_option_text}")
            first_option.click()

            # Get all options from the second dropdown
            second_options = wait.until(EC.presence_of_all_elements_located((By.XPATH, second_dropdown_xpath)))

            for second_option in second_options:
                second_option_text = second_option.text.strip()
                if second_option.is_displayed() and second_option.is_enabled():
                    print(f"Selecting second option: {second_option_text}")
                    second_option.click()

                    # Click the 'Go' button
                    go_button = wait.until(EC.element_to_be_clickable((By.XPATH, go_button_xpath)))
                    go_button.click()
                    time.sleep(5)  # Wait for the page to refresh (optional)

                    # Click the download button (optional)
                    download_button = wait.until(EC.element_to_be_clickable((By.XPATH, download_button_xpath)))
                    download_button.click()
                    time.sleep(5)  # Wait for the download (optional)

                    # Re-select the first option for the next iteration of the second dropdown
                    first_option = wait.until(EC.presence_of_element_located((By.XPATH, first_dropdown_xpath)))
                    first_option.click()

    # Switch out of the iframe when done
    driver.switch_to.default_content()

finally:
    # Close the WebDriver when done
    driver.quit()
