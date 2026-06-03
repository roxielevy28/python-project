import requests
from bs4 import BeautifulSoup

page = requests.get('https://books.toscrape.com/catalogue/set-me-free_988/index.html')
soup = BeautifulSoup (page.content, 'html.parser')
print(soup)
product = soup.find(id="default")
print (product)

items = product.find_all(class_= 'col-sm-6 product_main')
print(items)

print(items[0].find(class_= 'instock availability')
print(items[0].find(class_= 'star-rating Five')

quantity_available = [items[0].find(class_= 'instock availability')
review_rating = [items[0].find(class_= 'star-rating Five')
                 

items_2 = product.find_all(class_= 'table table-striped')

print(items[2].find(class_= '')
      
universal_ product_code (upc) = items_2[0].find_
price_including_tax = items_2[0].find_
price_excluding_tax

print(quantity_available)
print(review_rating)


Book_Report = pd.DataFrame(
    {
    "product_page_url",
    "universal_product_code",
    "book_title",
    "price_including_tax",
    "price_excluding_tax",
    "quantity_available",
    "product_description",
    "category",
    "review_rating",
    "image_url"
    })
    