"""
Book scraper module for extracting book data from books.toscrape.com.

This module implements a web scraper that collects book information including
title, price, rating, category, and availability from books.toscrape.com
and saves the data to a CSV file.
"""

import csv
import os
import random
import re
import time
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class BookScraper:
    """
    A web scraper for extracting book data from books.toscrape.com.
    
    This class provides functionality to scrape book information including
    title, price, rating, category, and availability from the website.
    """
    
    # Class constants
    BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
    DETAIL_BASE_URL = "http://books.toscrape.com/catalogue/"
    
    def __init__(self, output_file: str = 'question2_social_media_analysis/data/scraped_books.csv'):
        """
        Initialize the BookScraper.
        
        Args:
            output_file: Path to the output CSV file
        """
        self.output_file = output_file
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self) -> None:
        """Set up the requests session with headers and configuration."""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _random_delay(self) -> None:
        """Apply a random delay between 1-3 seconds."""
        delay = random.uniform(1, 3)
        time.sleep(delay)
    
    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url: The URL to fetch
            
        Returns:
            BeautifulSoup object if successful, None otherwise
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print("End of pages reached.")
                return None
            print(f"HTTP error occurred: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error occurred: {e}")
            return None
    
    def _extract_title(self, book_element) -> str:
        """
        Extract book title from book element.
        
        Args:
            book_element: BeautifulSoup element containing book data
            
        Returns:
            Book title as string
        """
        try:
            return book_element.h3.a['title']
        except (AttributeError, KeyError):
            return "Unknown Title"
    
    def _extract_price(self, book_element) -> float:
        """
        Extract and clean book price from book element.
        
        Args:
            book_element: BeautifulSoup element containing book data
            
        Returns:
            Price as float, 0.0 if extraction fails
        """
        try:
            price_str = book_element.find('p', class_='price_color').text
            # Remove all non-numeric characters except decimal point
            price_numeric = re.sub(r'[^\d.]', '', price_str)
            return float(price_numeric)
        except (ValueError, AttributeError) as e:
            print(f"Error processing price: {e}")
            return 0.0
    
    def _extract_rating(self, book_element) -> int:
        """
        Extract book rating from book element.
        
        Args:
            book_element: BeautifulSoup element containing book data
            
        Returns:
            Rating as integer (1-5), 0 if extraction fails
        """
        try:
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            rating_tag = book_element.find('p', class_=re.compile(r'star-rating'))
            rating_class = rating_tag['class'][1]  # e.g., 'Three'
            return rating_map.get(rating_class, 0)
        except (AttributeError, IndexError, TypeError):
            return 0
    
    def _extract_book_details(self, book_element) -> Dict[str, str]:
        """
        Extract detailed information from book's detail page.
        
        Args:
            book_element: BeautifulSoup element containing book data
            
        Returns:
            Dictionary containing category and availability
        """
        details = {"category": "Unknown", "availability": 0}
        
        try:
            book_relative_url = book_element.h3.a['href']
            book_url = urljoin(self.DETAIL_BASE_URL, book_relative_url.replace('../', ''))
            book_soup = self._fetch_page(book_url)
            
            if book_soup is None:
                return details
            
            # Extract category
            category = self._extract_category(book_soup)
            if category:
                details["category"] = category
            
            # Extract availability
            availability = self._extract_availability(book_soup)
            details["availability"] = availability
            
        except (AttributeError, KeyError) as e:
            print(f"Error getting book details: {e}")
        
        return details
    
    def _extract_category(self, book_soup: BeautifulSoup) -> Optional[str]:
        """
        Extract category from book detail page.
        
        Args:
            book_soup: BeautifulSoup object of book detail page
            
        Returns:
            Category name or None if not found
        """
        try:
            breadcrumb = book_soup.find('ul', class_='breadcrumb')
            if breadcrumb and len(breadcrumb.find_all('li')) > 2:
                return breadcrumb.find_all('li')[2].a.text.strip()
        except (AttributeError, IndexError):
            pass
        return None
    
    def _extract_availability(self, book_soup: BeautifulSoup) -> int:
        """
        Extract availability status from book detail page.
        
        Args:
            book_soup: BeautifulSoup object of book detail page
            
        Returns:
            1 if in stock, 0 if out of stock
        """
        try:
            availability_tag = book_soup.find('p', class_='instock availability')
            if availability_tag and 'In stock' in availability_tag.text:
                return 1
        except AttributeError:
            pass
        return 0
    
    def _extract_book_data(self, book_element) -> Dict[str, any]:
        """
        Extract all data for a single book.
        
        Args:
            book_element: BeautifulSoup element containing book data
            
        Returns:
            Dictionary containing all book information
        """
        title = self._extract_title(book_element)
        price = self._extract_price(book_element)
        rating = self._extract_rating(book_element)
        details = self._extract_book_details(book_element)
        
        return {
            'title': title,
            'price': price,
            'rating': rating,
            'availability': details['availability'],
            'category': details['category']
        }
    
    def _save_to_csv(self, books_data: List[Dict[str, any]]) -> None:
        """
        Save book data to CSV file.
        
        Args:
            books_data: List of dictionaries containing book information
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        fieldnames = ['title', 'price', 'rating', 'availability', 'category']
        
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(books_data)
    
    def scrape_books(self) -> None:
        """
        Main method to scrape all books from the website.
        
        This method iterates through all pages, extracts book data,
        and saves it to a CSV file.
        """
        all_books = []
        page_num = 1
        limited_pages = 1  # Limit to first 50 pages for demonstration

        while page_num <= limited_pages:
            url = self.BASE_URL.format(page_num)
            print(f"Scraping page {page_num}...")
            
            soup = self._fetch_page(url)
            if soup is None:
                break
            
            books = soup.find_all('article', class_='product_pod')
            if not books:
                print("No more books found. Stopping.")
                break
            
            for book in books:
                book_data = self._extract_book_data(book)
                all_books.append(book_data)
            
            # Add random delay between page requests
            self._random_delay()
            page_num += 1
        
        # Save the data to CSV file
        self._save_to_csv(all_books)
        print(f"Scraping complete! {len(all_books)} books saved to {self.output_file}")


def main() -> None:
    """Main function to run the scraper."""
    scraper = BookScraper()
    scraper.scrape_books()


if __name__ == "__main__":
    main()