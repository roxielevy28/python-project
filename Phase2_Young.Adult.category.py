import pandas as pd 
import request
from bs4 import BeautifulSoup

catergory= requests.get('https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html')
soup = BeautifulSoup (page.content, 'html.parser')

