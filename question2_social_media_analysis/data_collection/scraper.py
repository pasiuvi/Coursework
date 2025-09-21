# question2_social_media_analysis/data_collection/scraper.py

import requests
from bs4 import BeautifulSoup
import csv
import time
import re

def scrape_books():
    """
    Scrapes book data from http://books.toscrape.com/, including title, price,
    category, rating, and availability, and saves it to a CSV file.
    """
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_books = []
    page_num = 1
    
    # Mapping for converting star rating text to a number
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

    while True:
        url = base_url.format(page_num)
        print(f"Scraping page {page_num}...")
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print("End of pages reached.")
                break
            else:
                print(f"HTTP error occurred: {e}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Request error occurred: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find_all('article', class_='product_pod')

        if not books:
            print("No more books found. Stopping.")
            break

        for book in books:
            title = book.h3.a['title']
            
            # --- Extract Price ---
            price_str = book.find('p', class_='price_color').text
            try:
                # Remove all non-numeric characters except decimal point
                price_numeric = re.sub(r'[^\d.]', '', price_str)
                price_cleaned = float(price_numeric)
            except (ValueError, AttributeError) as e:
                print(f"Error processing price '{price_str}': {e}")
                price_cleaned = 0.0  # Default value if conversion fails

            # --- Extract Rating ---
            try:
                rating_tag = book.find('p', class_=re.compile(r'star-rating'))
                rating_class = rating_tag['class'][1] # e.g., 'Three'
                rating = rating_map.get(rating_class, 0) # Default to 0 if not found
            except (AttributeError, IndexError, TypeError) as e:
                print(f"Error getting rating for book '{title}': {e}")
                rating = 0

            # --- Navigate to the book's detail page for category and availability ---
            category = "Unknown"
            availability = 0
            try:
                book_relative_url = book.h3.a['href']
                book_url = 'http://books.toscrape.com/catalogue/' + book_relative_url.replace('../', '')
                book_response = requests.get(book_url)
                book_soup = BeautifulSoup(book_response.content, 'html.parser')
                
                # Get category
                breadcrumb = book_soup.find('ul', class_='breadcrumb')
                if breadcrumb and len(breadcrumb.find_all('li')) > 2:
                    category = breadcrumb.find_all('li')[2].a.text.strip()
                
                # Get availability
                availability_tag = book_soup.find('p', class_='instock availability')
                if availability_tag:
                    # Use regex to find all digits in the string
                    availability_match = re.search(r'(\d+)', availability_tag.text)
                    if availability_match:
                        availability = int(availability_match.group(1))

            except (AttributeError, IndexError, requests.exceptions.RequestException) as e:
                print(f"Error getting details for book '{title}': {e}")
                # Defaults are already set, so we can just continue

            all_books.append({
                'title': title,
                'price': price_cleaned,
                'rating': rating,
                'availability': availability,
                'category': category
            })
        
        # Be a good web citizen by adding a delay between requests
        time.sleep(1)
        page_num += 1

    # Save the data to a CSV file
    csv_file = 'scraped_books.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['title', 'price', 'rating', 'availability', 'category']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_books)

    print(f"Scraping complete! {len(all_books)} books saved to {csv_file}")


if __name__ == "__main__":
    scrape_books()

# ... (all the import statements) ...

def scrape_books():
    # ... (the rest of the scraping code is the same) ...

    # Save the data to a CSV file in the 'data' subfolder
    csv_file = '../data/scraped_books.csv' # <-- This line is updated
    # ... (the rest of the code for writing the CSV file) ...