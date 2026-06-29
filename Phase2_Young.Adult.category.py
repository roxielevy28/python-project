from urllib.parse import urljoin
# Harold: (Milestone 3) Added below import — needed to build and export a DataFrame from all scraped books
import pandas as pd
import requests
from bs4 import BeautifulSoup
from scrapetest import scrape_one_book

# =============================================================================
# 🔴 ISSUE #2 — NO ERROR HANDLING: One bad book crashes the whole script
# =============================================================================
# Harold: (2026-06-28, Milestone 3) Right now, if scrape_one_book() fails on
# even ONE book (network timeout, missing HTML element, etc.), the entire script
# crashes and you lose ALL the books you already scraped.
#
# ✅ FIX: Wrap each scrape call in try/except so one failure doesn't stop
#    the whole loop. See the example further down in this file.

category_url = "https://books.toscrape.com/catalogue/category/books/young-adult_21/index.html"

url_for_all_books_in_category=[]

page = requests.get(category_url)
soup = BeautifulSoup(page.text,'html.parser')

product = soup.find(id="default")
books_on_page= soup.find_all(class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')

for book_element in books_on_page:
        link = book_element.find('h3').find('a')['href']
        complete_url = urljoin(category_url, link)
        url_for_all_books_in_category.append(complete_url)
    
print(url_for_all_books_in_category)

all_books = []

# Harold: (Milestone 3, Step 1) Scrape all books on page 1 FIRST
# url_for_all_books_in_category already holds every book link from the first page
# Harold: (2026-06-28, connects to Issue #2) ⚠️ NO ERROR HANDLING here — if one
# book page fails, the whole script crashes. Here's what to change:
#
#   CURRENT (fragile):
#       for url in url_for_all_books_in_category:
#           book_data = scrape_one_book(url)
#           all_books.append(book_data)
#
#   BETTER (resilient):
#       for url in url_for_all_books_in_category:
#           try:
#               book_data = scrape_one_book(url)
#               all_books.append(book_data)
#           except Exception as e:
#               print(f"  ⚠️ Skipped {url}: {e}")
#               continue
#
# 🎯 WHY: With 30+ books in this category, even a 5% failure rate means you'd
#    lose 1-2 books silently — or worse, crash before saving anything.
for url in url_for_all_books_in_category:
    # Harold: (connects to Milestone 2) Calling the reusable function — pass it one URL, get back a dictionary of all 10 fields
    book_data = scrape_one_book(url)
    all_books.append(book_data)

# Harold: (Milestone 3, Step 2) NOW loop through remaining pages using pagination
# 'while True' keeps going until we run out of 'next' buttons
# Harold: (2026-06-28, Milestone 3) ✅ The pagination logic itself is CORRECT —
# it checks for a 'next' button and stops when there isn't one. Good work!
# But the same error-handling issue from Step 1 applies here too.
while True:
    next_button = soup.find(class_='next')
    if not next_button:
        # Harold: No 'next' button means we've hit the last page — time to stop
        break
    
    # Harold: Build the URL for the next page (e.g., page-2.html, page-3.html, etc.)
    next_page = next_button.find("a")["href"]
    category_url = urljoin(category_url, next_page)
    
    # Harold: Fetch and parse THAT next page
    page = requests.get(category_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Harold: Extract all book links from this new page, same as we did for page 1
    books_on_page = soup.find_all(class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    for book_element in books_on_page:
        link = book_element.find('h3').find('a')['href']
        complete_url = urljoin(category_url, link)
        # Harold: Scrape each book and add it to the SAME master list (all_books keeps growing)
        book_data = scrape_one_book(complete_url)
        all_books.append(book_data)

# =============================================================================
# 🟡 ISSUE #3 — OUTPUT FILENAME: 'all_books.csv' is too generic
# =============================================================================
# Harold: (2026-06-28, Milestone 3 → connects to Milestone 4) This file always
# saves to 'all_books.csv'. But All_Category.py saves each category to its own
# named file like 'young_adult.csv', 'mystery.csv', etc. This is inconsistent.
#
# ✅ FIX: Change the filename to match the category:
#
#       master_report.to_csv('young_adult.csv', index=False)
#
# 🎯 WHY: Consistency. When you look at your folder later, you'll immediately
#    know which file is which. Also avoids overwriting if you run both scripts.

# Harold: (Milestone 3, Step 3) Export everything to ONE CSV — all books from every page in this category
master_report = pd.DataFrame(all_books)
master_report.to_csv('all_books.csv', index=False)

# =============================================================================
# 🟡 ISSUE #4 — quantity_available contains extra text
# =============================================================================
# Harold: (2026-06-28, connects to Milestone 2) The quantity_available field
# stores "In stock (19 available)" as a string. If you ever want to analyze
# stock levels numerically (e.g., "which books have fewer than 5 in stock?"),
# you'd need to parse this first.
#
# ✅ FIX (in scrapetest.py): Extract just the number:
#
#       import re
#       raw_quantity = items[0].find(class_='instock availability').text.strip()
#       quantity_available = int(re.search(r'\d+', raw_quantity).group())
#
# 🎯 WHY: Numbers let you sort, filter, and do math. Strings like
#    "In stock (19 available)" can't be compared numerically.

# =============================================================================
# 🟡 ISSUE #5 — Product descriptions appear duplicated
# =============================================================================
# Harold: (2026-06-28, connects to Milestone 2) In the CSV output, descriptions
# appear to repeat the same paragraph twice. This is happening in
# scrape_one_book() where it finds the <p> tag after .sub-header.
#
# ✅ FIX (in scrapetest.py): The issue is likely that find_next('p') is picking
#    up a description that already includes the "..." truncated version plus
#    the full version. Try being more specific about which <p> tag to grab,
#    or check if the page has multiple <p> tags in that section.
#
# 🎯 WHY: Duplicated text inflates file size and makes analysis less accurate.

# =============================================================================
# 🟢 QUICK WINS — Minor cleanup
# =============================================================================
# Harold: (2026-06-28, Milestone 3) Small things that'll keep this file clean:
#
# 1. The `product` variable on line 23 is found but never used in this file.
#    (It's used INSIDE scrape_one_book, but not here.) You can delete:
#        product = soup.find(id="default")
#
# 2. The `url_for_all_books_in_category` list is built but only used in the
#    loop below. Consider adding a count print so you know how many books
#    were found:
#        print(f"Found {len(url_for_all_books_in_category)} books on page 1")
#
# 3. After the final CSV save, add a confirmation:
#        print(f"✅ Saved {len(all_books)} books to young_adult.csv")
#    This way you see in the terminal that it worked.

# =============================================================================
# 🟡 ISSUE #6 — CSV FILES SCATTERED IN ROOT FOLDER: Use a subfolder
# =============================================================================
# Harold: (2026-06-28, Milestone 3 → connects to Milestone 4) Right now all
# your CSV files (young_adult.csv, mystery.csv, etc.) are saved directly in
# the project root folder, mixed in with your .py files. With 50+ CSVs this
# gets messy fast.
#
# ✅ FIX: Save all CSVs into a dedicated folder like `csv_reports/`.
#    You need to make TWO changes:
#
#    CHANGE 1 — At the top of this file, add:
#        import os
#
#    CHANGE 2 — Before the to_csv line, add:
#        os.makedirs('csv_reports', exist_ok=True)
#
#    CHANGE 3 — Update the filename path:
#        master_report.to_csv('csv_reports/young_adult.csv', index=False)
#
#    🎯 SAME FIX NEEDED IN All_Category.py:
#        os.makedirs('csv_reports', exist_ok=True)
#        df.to_csv(f"csv_reports/{safe_name}.csv", index=False)
#
# 🎯 WHY: Keeps your project organized — code in one place, data in another.
#    Also makes it easy to delete all CSVs at once (just delete the folder)
#    without accidentally deleting your scripts.

# =============================================================================
# 📋 SUMMARY: What's documented vs what still needs actual code changes
# =============================================================================
# Harold: (2026-06-28, Milestones 2/3/4) This file has COMMENTS explaining
# every issue, but the actual code has NOT been changed yet. Here's your
# checklist of what to fix and WHERE:
#
# ┌─────┬──────────────────────────────┬─────────────────────┬──────────┐
│  #  │ Issue                        │ Fix in which file   │ Status   │
# ├─────┼──────────────────────────────┼─────────────────────┼──────────┤
│  1  │ List-wrapped CSV values      │ scrapetest.py       │ done  │
│  2  │ No error handling            │ Phase2 + All_Cat    │ ❌ TODO  │
│  3  │ Generic 'all_books.csv' name │ Phase2_Young...py   │ ❌ TODO  │
│  4  │ quantity_available is string │ scrapetest.py       │ done  │
│  5  │ Duplicated descriptions      │ scrapetest.py       │ done  │
│  6  │ CSVs scattered in root       │ Phase2 + All_Cat    │ ❌ TODO  │
│  7  │ 'Books' homepage in loop     │ All_Category.py     │ ❌ TODO  │
│  8  │ Image download no error hdlg │ Image_files.py      │ ❌ TODO  │
│  9  │ catergory_name typo          │ All_Category.py     │ ❌ TODO  │
│ 10  │ Unused variables             │ All_Category.py     │ ❌ TODO  │
└─────┴──────────────────────────────┴─────────────────────┴──────────┘
#
# 🎯 RECOMMENDED ORDER:
#    Fix #1 first (scrapetest.py) — it affects EVERYTHING downstream
#    Fix #2 next — protects all your scraping from crashes
#    Fix #6 — keeps your folder clean before you regenerate all CSVs
#    Then fix the rest in any order




