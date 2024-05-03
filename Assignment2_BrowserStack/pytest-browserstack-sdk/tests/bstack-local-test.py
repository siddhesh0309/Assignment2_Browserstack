import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

OptionsCheck = ChromeOptions()
OptionsCheck.set_capability('sessionName', 'BStack Local Test')

WebDriver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=OptionsCheck)

try:
    WebDriver.get('http://bs-local.com:45454')
    PageTitle = WebDriver.title
    
    if 'BrowserStack Local' in PageTitle:     
        WebDriver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Local Test ran successfully"}}')
    else:
        
        WebDriver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Local test setup failed"}}')
except Exception as err:
    Message = 'Exception: ' + str(err.__class__) + str(err.msg)
    WebDriver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(Message) + '}}')

WebDriver.quit()
