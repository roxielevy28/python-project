from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup

home_url= requests.get('https://books.toscrape.com/index.html')
page = requests.get(home_url)
soup = BeautifulSoup(page.content, 'html.parser')

category_links= []
page_content= soup.find(id="default")
category_list = page.find_all(class_= 'nav nav-list')
print(category_list)
