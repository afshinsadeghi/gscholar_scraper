
from scholar import GScholar 




first_page = 1
last_page = 4
keywords = 'visual transformer'
search_scraper = GScholar(keywords,first_page,last_page)
print(search_scraper.get_main('h3', {'class': 'gs_rt'})) # you get title

print(search_scraper.get_year())
print(search_scraper.get_author())
print(search_scraper.get_link())

print(search_scraper.to_json())
#Json Formatting
search_scraper.get_all()
#Dictionary