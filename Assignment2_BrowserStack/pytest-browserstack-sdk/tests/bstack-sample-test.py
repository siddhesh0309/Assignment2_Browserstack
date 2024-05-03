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
OptionsToSelect.set_capability('sessionName', 'BStack Sample Test')
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
    time.sleep(10)


    HighToLow_Filter = WebDriverWait(ChromeWebDriver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div[1]/div[2]/div[1]/div/div/div[3]/div[4]"))
    )
    HighToLow_Filter .click()
    time.sleep(10)
    


    ChromeWebDriver.implicitly_wait(5)
    ProductElement  = ChromeWebDriver.find_elements(By.CLASS_NAME, "tUxRFH")
    ProductList = []

    for Product_Elements in ProductElement :
        ProductName = Product_Elements .find_element(By.CLASS_NAME, "KzDlHZ").text
        PriceDisplay = Product_Elements .find_element(By.CLASS_NAME, "Nx9bqj._4b5DiR").text
        ProductURL = Product_Elements .find_element(By.TAG_NAME, "a").get_attribute("href")

        ProductDictionary  = {
            "Product Name": ProductName ,
            "Display Price": PriceDisplay ,
            "Link to Product Details Page": ProductURL 
        }

        ProductList.append(ProductDictionary )

    with open("product_list.txt", "w") as file:
        for ProductDictionary in ProductList:
            file.write(json.dumps(ProductDictionary) + "\n")   

    
    for ProductDictionary  in ProductList :
        print(ProductDictionary )
except NoSuchElementException as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    ChromeWebDriver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
except Exception as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    ChromeWebDriver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
finally:
    
    ChromeWebDriver.quit()