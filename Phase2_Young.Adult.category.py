from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

category_url = "https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html"
url_for_all_books= []

page = requests.get(category_url)
soup = BeautifulSoup(page.text,'html.parser')

# link from each book on the page
product = soup.find(id="default")
books_on_page= soup.find_all(class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')

for book_element in books_on_page:
    link = book_element.find('h3').find('a')['href']
    complete_url = urljoin(category_url, link)
    # print(complete_url) 
    url_for_all_books.append(complete_url)
     # this works now. i got all the links on the first page

next_button = soup.find(class_='next')
if next_button:
        next_page = next_button.find("a")["href"]
        additional_page_url = urljoin(category_url, next_page)

else:
    additional_page_url = None

all_books = []
for url in url_for_all_books:
    book_data = scrape_one_book(url)
    all_books.append(book_data)

master_report = pd.DataFrame(all_books)
master_report.to_csv('all_books.csv', index=False)



