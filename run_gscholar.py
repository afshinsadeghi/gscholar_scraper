
from scholar import GScholar 




first_page = 1
last_page = 2
keywords = 'visual transformer'

search_scraper = GScholar(keywords,first_page,last_page)

#print(search_scraper.get_main('h3', {'class': 'gs_rt'})) # you get title

#print(search_scraper.get_year())
#print(search_scraper.get_author())
#print(search_scraper.get_link())

#print(search_scraper.to_json())
#Json Formatting
try:
    dic = search_scraper.get_results()
    search_scraper.close_page()
except:
    search_scraper.close_page()
#Dictionary
import json
with open('mytestsearch.json', 'w') as f:
    json.dump(dic, f)


import pandas as pd
df = pd.DataFrame(dic)
df.to_csv('mytestsearch.csv')

