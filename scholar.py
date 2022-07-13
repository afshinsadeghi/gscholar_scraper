#from search import Search
from getdriver import GetDriver
from selenium.webdriver.support.select import Select
import time
from selenium.webdriver.common.touch_actions import TouchActions

import imp
from pkgutil import ImpImporter
from time import sleep
import time
#import requests
import json
import random
import pandas as pd

from getwebpage import GetWebPage 

GOOGLE_URLS = {'GOOGLE': 'https://www.google.com/search?q={}&start={}', 
               'GOOGLE_SCHOLAR': 'https://scholar.google.com/scholar?q={}&start={}', 
              }



from bs4 import BeautifulSoup
from urllib.parse import unquote
import re

class GScholar():


    URL = GOOGLE_URLS['GOOGLE_SCHOLAR']
    LABELS = ['year', 'title', 'description', 'authors', 'link', 
              'pdf_link', 'journal_domain', 'domain', 'many_version','abstract']

    def __init__(self, search_word, start_page=1, max_page=1):
        #super().__init__(search_word, start_page, max_page)
        self.start_page_num = (start_page-1) * 10
        self.max_page_num = (max_page-1) * 10
        self.driver_get = GetDriver()
        self.driver = self.driver_get.driver
        
        self.years = []
        self.titles = []
        self.descs = []
        self.authors = []
        self.links = []
        self.pdf_links = []
        self.journal_domains = []
        self.domains = []
        self.many_versions = []
        self.abstracts = []

        self.result_dic = []
        self.search_word = search_word
        self.start_page = self.start_page_num
        self.max_page = self.max_page_num

        self.sleep = []
        self.dict_of_td = {}
        self.dataframe = None
        self.json_of_td = []
        
        self.pages = self.process(self.driver, GScholar.URL, self.start_page_num, self.max_page_num)

    def lastocc(snt, lst):
        '''
        Return: int, Last occurence id of specific element value.
        Parameter: 
        snt -> element value to get index.
        lst -> iterable.
        Example:
        >>> data = ['study', 'from', 'home', 'study', 'from', 'school']
        >>> Search.lastocc('from', data)
        4
        '''

        rvs_lst = lst[::-1]
        snt_id = len(lst) - rvs_lst.index(snt) - 1

        return snt_id


    def process(self, driver, url, page_num, max_page_num):
        '''
        Return: dict, page number: response of website. Used by Internal Function.
        Parameter: 
        url -> string, url to get response
        page_num -> int, page number of Search Engine to starting get response.
        max_page_num -> int, maximum page number of of Search Engine to stop get response.
        '''
        num = self.start_page
        result = {}
        self.sleep = []
        get_page =  GetWebPage(driver)
       
        while page_num <= max_page_num:
            if page_num == 0:  #google recognizes it as bot.
                page_num_to_send = -10
            else:
                page_num_to_send = page_num
            search_url = url.format(self.search_word, page_num_to_send)
            self.page = get_page.get_url(search_url) # #page = requests.get(search_url)
            
            result.update({num: self.page})  #result.update({num: page.content})
            
            self.result_dic.append(self.get_all())
            self.reset_page_values()
            page_num += 10
            num += 1

            time_wait = random.uniform(1, 2)
            time.sleep(2)
        
            self.sleep.append(time_wait)
            sleep(time_wait)
        return result


    def to_dict(self, label, *data):
        '''
        Return: dict, {label1: data1, label2: data2, ..., labeln: datan} 
                all attribute in results. Used by get_all() function. If
                you want to get dictionary result, use get_all() instead
                of to_dict().
        Parameter: 
        label -> list of string to be label of data.
        data -> list of row data and all attributes needed.
        '''

        if self.dict_of_td:
            return self.dict_of_td

        for i in range(len(label)):
            self.dict_of_td.update({label[i]: data[i]})
            print(label[i], len(data[i]))
        return self.dict_of_td


    def to_pd(self):
        '''
        Return: dataframe, all column and row based on attributes.
        Example:
        >>> search_news = GNews('events today')
        >>> print(search_news.to_pd())
        '''

        if self.dataframe:
            return self.dataframe

        self.dataframe = pd.DataFrame(self.get_all())
        return self.dataframe


    def to_json(self):
        '''
        Return: json, all attribute in results.
        Example:
        >>> search_news = GNews('events today')
        >>> print(search_news.to_json())
        '''

        if self.json_of_td:
            return self.json_of_td

        result = self.to_pd().to_json(orient='index')
        parsed = json.loads(result)
        self.json_of_td = json.dumps(parsed, indent=4, ensure_ascii=False)
        return self.json_of_td


    def reset_page_values(self):
        self.years = []
        self.titles = []
        self.descs = []
        self.authors = []
        self.links = []
        self.pdf_links = []
        self.journal_domains = []
        self.domains = []
        self.many_versions = []
        self.abstracts = []

    def close_page(self):
        self.driver.close()
        del self.driver_get

    def get_main(self, tag, attr, findAll=False):
        '''
        Return: result -> list, the value is BS4 object. This function 
                is used by all another function inside this class.
        Parameter:
        tag -> string, html tag to gather.
        attr -> string, attribute from a tag. 
        [findAll] !optional -> boolean, the result will be 2D list instead of 1D, 
                               because BS4 will search all tag and attr 
                               that meet the criteria, not the first match.
        Example:
        >>> search_thesis = GScholar('informatics and technology thesis')
        >>> print(search_thesis.get_main('h3', {'class': 'gs_rt'})) # you get title
        '''

        res = []
        
        #for page_num in self.pages :
        #    page = self.pages[page_num] #google recognizes the first page as bot so redoing it
        page = self.page
        soup = BeautifulSoup(page, 'html.parser')
        texts_parse = soup.findAll('div', {'class': 'gs_r gs_or gs_scl'})

        for t in texts_parse:
            get_attr = t.findAll(tag, attr) if findAll else t.find(tag, attr)

            if get_attr:
                res.append(get_attr)
            else:
                res.append(None)

        return res


    def get_year(self):
        '''
        Return: year -> list, year of result.
        Example:
        >>> search_thesis = GScholar('informatics and technology thesis')
        >>> print(search_thesis.get_year())
        '''

        if self.years:
            return self.years

        dates_tmp = self.get_main('div', {'class': 'gs_a'})
        for d in dates_tmp:
            d = d.text
            pattern = r"\d{4}"
            found_year = re.search(pattern, str(d))
            if found_year:
                self.years.append(found_year.group(0))
            else:
                self.years.append(None)

        return self.years


    def get_title(self):
        '''
        Return: title -> list, title of result.
        Example:
        >>> search_thesis = GScholar('informatics and technology thesis')
        >>> print(search_thesis.get_title())
        '''

        if self.titles:
            return self.titles

        res = [res.text for res in self.get_main('h3', {'class': 'gs_rt'})]
        self.titles.extend(res)
        return self.titles


    def get_desc(self):
        '''
        Return: description -> list, description of result.
        Example:
        >>> search_thesis = GScholar('informatics and technology thesis')
        >>> print(search_thesis.get_desc())
        '''

        if self.descs:
            return self.descs

        res = [res.text for res in self.get_main('div', {'class': 'gs_rs'})]
        self.descs.extend(res)
        return self.descs


    def get_author(self):
        '''
        Return: author -> list, author of result.
        Example:
        >>> search_thesis = GScholar('informatics and technology thesis')
        >>> print(search_thesis.get_author())
        '''

        if self.authors:
            return self.authors

        split_sym = '-'
        dates_tmp = self.get_main('div', {'class': 'gs_a'})
        for d in dates_tmp:
            d = d.text
            if split_sym in d:
                id_split_sym = d.index(split_sym)
                self.authors.append(d[:id_split_sym-1])
            else:
                self.authors.append(None)

        return self.authors


    def get_link(self):
        '''
        Return: link -> list, link of result.
        Example:
        Example:
        >>> search_thesis = GScholar('informatics and technology thesis')
        >>> print(search_thesis.get_link())
        '''

        if self.links:
            return self.links
        out_res = []
        for res in self.get_main('h3', {'class': 'gs_rt'}):
            
            if res is None:
                value_ = ''
            else:
                res2 = res.find('a')
                if res2 is None:
                    value_ = ''
                else:
                    value_ = unquote(res2['href'])
            out_res.append(value_)
        #res = [unquote(res.find('a')['href']) for res in self.get_main('h3', {'class': 'gs_rt'})]
        self.links.extend(out_res)

        return self.links


    def get_pdflink(self):
        '''
        Return: pdflink -> list, if the result have pdf, then the 
                           element must not be None.
        Example: 
        >>> search_thesis = GScholar('informatics and technology thesis')
        >>> print(search_thesis.get_pdflink())
        '''

        if self.pdf_links:
            return self.pdf_links

        self.pdf_links = [unquote(res.find('a')['href'])
                         if res 
                         else None 
                         for res in self.get_main('div', {'class': 'gs_or_ggsm'})]

        return self.pdf_links

    
    def get_abstract(self):
        if self.abstracts:
            return self.abstracts #gsh_csp

        #links = self.get_link()
        #pop_up = self.get_main('h3', {'class': 'gs_rt'})
        from selenium.webdriver.common.by import By
        #abs_ = ByChained(By.tagName("h3"),By.className("gs_rt"))
        
        #byXpath = '//*[@id="gs_res_ccl_mid"]/div[2]/div/h3' # and (@class = 'gs_rt')]
        
        #elements = self.driver.find_elements_by_xpath(byXpath)#find_elements_by_class_name("gs_rt")
        elements = self.driver.find_elements_by_class_name("gs_rt")
        for elem in elements:
            
            #elem = self.driver.find_element_by_class_name("gs_rt")
            self.touch = TouchActions(self.driver)
            self.touch.tap(elem).perform()
            time.sleep( random.uniform(2, 3))
            res = self.driver.find_element_by_class_name("gsh_csp").get_attribute('innerHTML')
            self.abstracts.append(res)
            time.sleep(1.5)
            self.touch2 = TouchActions(self.driver)
            
            res_close = self.driver.find_element_by_id("gs_qabs-x")
            self.touch2.tap(res_close).perform()
            time.sleep(random.uniform(2, 3))
            

        return self.abstracts
        
    def get_journal_domain(self):
        '''
        Return: journal_domain -> list, domain or subdomain that used 
                                  for online publication.
        Example:
        >>> search_thesis = GScholar('informatics and technology thesis')
        >>> print(search_thesis.get_journal_domain())
        '''

        if self.journal_domains:
            return self.journal_domains

        split_sym = '-'
        journal_dom_tmp = self.get_main('div', {'class': 'gs_a'})
        for j in journal_dom_tmp:
            j = j.text
            pattern = r"([a-z0-9][a-z0-9\-]{0,61}[a-z0-9]\.)+[a-z0-9][a-z0-9\-]*[a-z0-9]"
            found_domain = re.search(pattern, str(j))
            if found_domain:
                self.journal_domains.append(found_domain.group(0))
            else:
                self.journal_domains.append(None)

        return self.journal_domains


    def get_domain(self):
        '''
        Return: domain -> list, domain or subdomain that extracted from link.
        Example:
        >>> search_thesis = GScholar('informatics and technology thesis')
        >>> print(search_thesis.get_domain())
        '''

        if self.domains:
            return self.domains

        subdomains = self.get_journal_domain()
        for s in subdomains:
            found_domain = re.search(r"(\w{2,}\.\w{2,3}\.\w{2,3}|\w{2,}\.\w{2,3})$", str(s))
            if found_domain:
                self.domains.append(found_domain.group(1))
            else:
                self.domains.append(None)

        return self.domains


    def get_many_version(self):
        '''
        Return: many of version -> list, available version of result.
        Example:
        >>> search_thesis = GScholar('informatics and technology thesis')
        >>> print(search_thesis.get_many_version())
        '''

        if self.many_versions:
            return self.many_versions

        self.many_versions = [res[-1].text
                              if res 
                              else None 
                              for res in self.get_main('a', {'class': 'gs_nph'}, findAll=True)]

        return self.many_versions


    def get_results(self):
        
        return self.to_dict(GScholar.LABELS,self.result_dic)

    #notice the get abstract is for one page only
    def get_all(self):
        '''
        Return: all attributes of result -> dict.
        Example:
        >>> search_thesis = GScholar('informatics and technology thesis')
        >>> print(search_thesis.get_all())
        '''

        years = self.get_year()
        titles = self.get_title()
        descs = self.get_desc()
        authors = self.get_author()
        links = self.get_link()
        pdf_links = self.get_pdflink()
        journal_domains = self.get_journal_domain()
        domains = self.get_domain()
        many_versions = self.get_many_version()
        abstracts = self.get_abstract()
        return [years, titles, descs, authors, 
                            links, pdf_links, journal_domains, domains, many_versions,abstracts]#

