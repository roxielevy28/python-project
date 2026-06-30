from urllib.parse import urljoin
import os
import requests
from bs4 import BeautifulSoup
from scrapetest import scrape_one_book

def clean_filename(name):
    return "".join(c if c.isalnum() else "_" for c in name.lower())
 
def get_all_category_links():
    home_url = 'https://books.toscrape.com/index.html'
    page = requests.get(home_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    category_links = []
    category_list = soup.find(class_='nav nav-list')
    categories = category_list.find_all('a')
 
    for category_url in categories:
        catergory_name = category_url.text.strip()
        link = category_url['href']
        complete_link = urljoin(home_url, link)
        category_links.append({
            "name": catergory_name,
            "url": complete_link
        })
    return category_links

def get_all_book_links(cat_url):
    all_book_urls = []
    while True:
        page = requests.get(cat_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        books_on_page = soup.find_all('article', class_='product_pod')
        for book_element in books_on_page:
            link = book_element.find('h3').find('a')['href']
            full_url = urljoin(cat_url, link)
            all_book_urls.append(full_url)

        next_button = soup.find(class_='next')
        if not next_button:
            break
        next_page = next_button.find('a')['href']
        cat_url = urljoin(cat_url, next_page)

    return all_book_urls

def download_image(image_url, category_type, book_title):
    if isinstance(category_type, (list, tuple)):
        category_str = category_type[0] if category_type else "unknown"
    else:
        category_str = category_type or "unknown"

    name_of_folder = clean_filename(category_str)
    
    if isinstance(book_title, (list, tuple)):
        book_title_str = book_title[0] if book_title else "untitled"
    else:
        book_title_str = book_title or "untitled"
 
    file_name = clean_filename(book_title_str)
    folder_path = os.path.join("images", name_of_folder)
    os.makedirs(folder_path, exist_ok=True)

    category_str = category_type or "unknown"

    _, ext = os.path.splitext(image_url)
    if not ext:
        ext = ".jpg"
    image_path = os.path.join(folder_path, f"{file_name}{ext}")
 
    response = requests.get(image_url)
    if response.status_code != 200:
        return None
 
    with open(image_path, "wb") as file:
        file.write(response.content)
    return image_path
all_categories = get_all_category_links()
for category in all_categories[1:]:
    category_type = category["name"]
    cat_url = category["url"]
    print(f"Downloading images from: {category_type}")
    
    book_links = get_all_book_links(cat_url)
    for book_url in book_links:
           try:
              book_data = scrape_one_book(book_url)
              download_image(...)
           except Exception as e:
                print(f"  ⚠️ Skipped {book_url}: {e}")
                continue

