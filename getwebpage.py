import logging

import time

class GetWebPage:
    def __init__(self,driver) -> None:
        self.driver = driver


    def get_url(self,url):
        time.sleep(0.5)
        self.driver.get(url)
        #content = driver.findElement(By.tagName("body")).getText();
        element = self.driver.find_element_by_tag_name("body")
        
        content = element.get_attribute('innerHTML')
        #content_text = element.text  #this is the text a user see without tags etc
        #print(content)
        #print(element_text)
        
        return content
