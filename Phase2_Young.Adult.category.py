from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

category_url = "https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html"
page = requests.get(category_url)
# print(category_url) # this works, i get the url

soup = BeautifulSoup(page.text,'html.parser')

# link from each book on the page
product = soup.find(id="default")
books_on_page= soup.find_all(class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')

for book_element in books_on_page:
    link = book_element.find('h3').find('a')['href']
    full_url = urljoin(category_url, link)
    # print(full_url) 
    # this works now. i got all the links on the first page

next_button = soup.find(class_='next')
if next_button:
        next_page = next_button.find("a")["href"]
        additional_url = urljoin(category_url, next_page)

else:
    additional_url = None

all_books = []
for url in all_book_urls:
    book_data = scrape_one_book(url)
    all_books.append(book_data)

master_report = pd.DataFrame(all_books)
master_report.to_csv('all_books.csv', index=False)



