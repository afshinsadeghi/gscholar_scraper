from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#in case using ChromeDriverManager enable this
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options

from webdriver_manager.firefox import GeckoDriverManager as FireFoxDriverManager
import os
import fnmatch
class GetDriver():
   
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


    def __init__(self):
        #driver_path = self.findChromeDriver() #this is for windows. for mac read in my manual 
        #driver_path = '/Users/asadeghi/bin/chromedriver'

        run_chrom = 1
        if run_chrom:

            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_experimental_option("excludeSwitches", ['enable-automation']);
            options.add_argument('--profile-directory=Default')
            mobile_emulation = {"deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
             "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}

            options.add_experimental_option("mobileEmulation", mobile_emulation)#mobile emulation to get abstracts
            options.add_experimental_option('w3c', False)#to run touch commands
            #driver = webdriver.Chrome(driver_path, options=options)
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        else:
            options = webdriver.FirefoxOptions()
            #options.add_argument('--profile-directory=Default')
            driver = webdriver.Firefox(FireFoxDriverManager().install(), options=options)
        
            #WebDriver driver = new FirefoxDriver(allProfiles.getProfile("default"))
        self.driver = driver