from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


#from webdriver_manager.chrome import ChromeDriverManager
import logging
import os
import fnmatch
import time

class GetWebPage:
    def __init__(self) -> None:
        pass

    def findChromeDriver(self):
        for root, dirs, files in os.walk(os.getcwd()):
            for name in files:
                if fnmatch.fnmatch(name, "*.exe"):
                    return os.path.join(root, name)
        raise Exception("Chrome driver not found: chromedriver.exe")


    def wait(self,driver, by, elem_identifier):
        try:
            element_present = EC.presence_of_element_located((by, elem_identifier))
            WebDriverWait(driver, 5).until(element_present)
        except TimeoutException:
            print("Timed out waiting for element " + elem_identifier + " to load")


    def get_url(self,url):
        #driver_path = self.findChromeDriver() #this is for windows. for mac read in my manual 
        driver_path = '/Users/asadeghi/bin/chromedriver'

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(driver_path, options=options)
        #driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        time.sleep(0.5)
        driver.get(url)
        content = driver.findElement(By.tagName("body")).getText();
        time.sleep(5)
        driver.close()
        return content
