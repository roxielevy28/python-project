from urllib.parse import urljoin
import os
import requests
from bs4 import BeautifulSoup
from scrapetest import scrape_one_book

# =============================================================================
# 🔴 ISSUE #1 — NO ERROR HANDLING: One bad image crashes everything
# =============================================================================
# Harold: (2026-06-28, connects to Milestone 4) This script downloads hundreds
# of images. If ONE image URL is broken or the network times out, the entire
# script crashes and you lose all remaining downloads.
#
# ✅ FIX: Wrap the download loop in try/except:
#
#        for book_url in book_links:
#            try:
#                book_data = scrape_one_book(book_url)
#                download_image(...)
#            except Exception as e:
#                print(f"  ⚠️ Skipped {book_url}: {e}")
#                continue
#
# 🎯 WHY: Network requests fail sometimes. This lets the script keep going.

# =============================================================================
# 🟡 ISSUE #2 — download_image() has unnecessary complexity
# =============================================================================
# Harold: (2026-06-28, connects to Milestone 2) The download_image function
# has lots of isinstance() checks like:
#        if isinstance(category_type, (list, tuple)):
#            category_str = category_type[0] if category_type else "unknown"
#
# These were added to handle the list-wrapped values from scrape_one_book().
# Once you fix Issue #1 in scrapetest.py (remove the [...] wrapping), you can
# SIMPLIFY this function significantly:
#
#   BEFORE (current, defensive):
#        if isinstance(category_type, (list, tuple)):
#            category_str = category_type[0] if category_type else "unknown"
#        else:
#            category_str = category_type or "unknown"
#
#   AFTER (clean, once scrapetest.py is fixed):
#        category_str = category_type or "unknown"
#
# 🎯 WHY: Cleaner code is easier to read and maintain. Fix the root cause
#    in scrapetest.py instead of working around it everywhere.

# =============================================================================
# 🟡 ISSUE #3 — 'Books' homepage included again
# =============================================================================
# Harold: (2026-06-28, Milestone 4) Same as All_Category.py — the first item
# in category links is "Books" (the homepage). Skip it:
#
#        for category in all_categories[1:]:

def clean_filename(name):
    return "".join(c if c.isalnum() else "_" for c in name.lower())
 # this function will get all the category links from the main page of the website
def get_all_category_links():
    home_url = 'https://books.toscrape.com/index.html'
    page = requests.get(home_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    category_links = []
    category_list = soup.find(class_='nav nav-list')
    categories = category_list.find_all('a')
 # this loop will iterate through all the category links and get the name and url of each category
    for category_url in categories:
        catergory_name = category_url.text.strip()
        link = category_url['href']
        complete_link = urljoin(home_url, link)
        category_links.append({
            "name": catergory_name,
            "url": complete_link
        })
    return category_links
# this function will get all the book links from a category page and return them as a list
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
# this function will download the image from the given url and save it in a folder named after the category type
def download_image(image_url, category_type, book_title):
    if isinstance(category_type, (list, tuple)):
        category_str = category_type[0] if category_type else "unknown"
    else:
        category_str = category_type or "unknown"

    name_of_folder = clean_filename(category_str)
    # Normalize book_title to string
    if isinstance(book_title, (list, tuple)):
        book_title_str = book_title[0] if book_title else "untitled"
    else:
        book_title_str = book_title or "untitled"
 # this will clean the book title to create a valid filename
    file_name = clean_filename(book_title_str)
    folder_path = os.path.join("images", name_of_folder)
    os.makedirs(folder_path, exist_ok=True)

    
    if isinstance(image_url, (list, tuple)):
        image_url = image_url[0] if image_url else ""
 # this will get the file extension from the image url and if it doesn't have one, it will default to .jpg
    _, ext = os.path.splitext(image_url)
    if not ext:
        ext = ".jpg"
    image_path = os.path.join(folder_path, f"{file_name}{ext}")
 # this will download the image from the url and save it to the specified path
    response = requests.get(image_url)
    if response.status_code != 200:
        return None
 # this will write the image content to the file
    with open(image_path, "wb") as file:
        file.write(response.content)
    return image_path
all_categories = get_all_category_links()
for category in all_categories:
    category_type = category["name"]
    cat_url = category["url"]
    print(f"Downloading images from: {category_type}")
    # this will get all the book links from the category page and then scrape each book's data and download the image
    book_links = get_all_book_links(cat_url)
    for book_url in book_links:
        book_data = scrape_one_book(book_url)
        download_image(
            book_data["image_url"],
            book_data["category"],
            book_data["book_title"]
        )
print("All book images")