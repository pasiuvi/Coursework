"""
Book scraper module for extracting book data from books.toscrape.com.

This module implements a web scraper that collects book information including
title, price, rating, category, and availability from books.toscrape.com
and saves the data to a CSV file.
"""

import csv
import logging
import os
import random
import re
import time
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class BookScraper:
    """
    A web scraper for extracting book data from books.toscrape.com.
    
    This class provides functionality to scrape book information including
    title, price, rating, category, and availability from the website.
    """
    
    # Class constants
    BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
    DETAIL_BASE_URL = "http://books.toscrape.com/catalogue/"
    
    def __init__(self, output_file: str = 'data/scraped_books.csv', max_pages: int = 1, logger=None):
        """
        Initialize the BookScraper.
        
        Args:
            output_file: Path to the output CSV file
            max_pages: Maximum number of pages to scrape (0 = all pages)
            logger: Optional logger to use instead of creating one
        """
        self.output_file = output_file
        self.max_pages = max_pages
        self.session = requests.Session()
        if logger:
            self.logger = logger
        else:
            self._setup_logging()
        self._setup_session()
        self.logger.info("BookScraper initialized successfully")
        self.logger.info(f"Output file set to: {self.output_file}")
        self.logger.info(f"Max pages to scrape: {self.max_pages if self.max_pages > 0 else 'unlimited'}")
    
    def _setup_logging(self) -> None:
        """Set up logging configuration for the scraper."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('scraper.log')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _setup_session(self) -> None:
        """Set up the requests session with headers and configuration."""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.logger.info("HTTP session configured with user agent")
    
    def _random_delay(self) -> None:
        """Apply a random delay between 1-3 seconds."""
        delay = random.uniform(1, 3)
        self.logger.debug(f"Applying random delay of {delay:.2f} seconds")
        time.sleep(delay)
    
    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url: The URL to fetch
            
        Returns:
            BeautifulSoup object if successful, None otherwise
        """
        self.logger.debug(f"Fetching page: {url}")
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            self.logger.debug(f"Successfully fetched page: {url} (Status: {response.status_code})")
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.HTTPError as e:
            if hasattr(e, 'response') and e.response.status_code == 404:
                self.logger.info(f"Reached end of pages - Page {url} not found (404)")
                return None
            self.logger.error(f"HTTP error occurred while fetching {url}: {e}")
            return None
        except requests.exceptions.Timeout:
            self.logger.warning(f"Timeout occurred while fetching {url}, retrying once...")
            try:
                response = self.session.get(url, timeout=60)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except Exception as retry_e:
                self.logger.error(f"Retry failed for {url}: {retry_e}")
                return None
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection error occurred while fetching {url}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error occurred while fetching {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error occurred while fetching {url}: {e}")
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
            title = book_element.h3.a['title']
            self.logger.debug(f"Extracted title: {title}")
            return title
        except (AttributeError, KeyError):
            self.logger.warning("Failed to extract book title, using default")
            return "Unknown Title"
    
    def _extract_price(self, book_element) -> str:
        """
        Extract book price from book element, preserving currency symbol.
        
        Args:
            book_element: BeautifulSoup element containing book data
            
        Returns:
            Price as string with currency symbol, '0.0' if extraction fails
        """
        try:
            price_str = book_element.find('p', class_='price_color').text.strip()
            # Keep the currency symbol and numeric value
            self.logger.debug(f"Extracted price: {price_str}")
            return price_str
        except (AttributeError) as e:
            self.logger.warning(f"Failed to extract price: {e}")
            return '0.0'
    
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
            rating = rating_map.get(rating_class, 0)
            self.logger.debug(f"Extracted rating: {rating}/5 stars")
            return rating
        except (AttributeError, IndexError, TypeError):
            self.logger.warning("Failed to extract rating, using default value 0")
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
            self.logger.debug(f"Fetching book details from: {book_url}")
            book_soup = self._fetch_page(book_url)
            
            if book_soup is None:
                self.logger.warning("Failed to fetch book detail page")
                return details
            
            # Extract category
            category = self._extract_category(book_soup)
            if category:
                details["category"] = category
                self.logger.debug(f"Extracted category: {category}")
            
            # Extract availability
            availability = self._extract_availability(book_soup)
            details["availability"] = availability
            self.logger.debug(f"Extracted availability: {'In Stock' if availability else 'Out of Stock'}")
            
        except (AttributeError, KeyError) as e:
            self.logger.error(f"Error getting book details: {e}")
        
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
        Extract availability count from book detail page.
        
        Args:
            book_soup: BeautifulSoup object of book detail page
            
        Returns:
            Number of items available in stock, 0 if out of stock
        """
        try:
            availability_tag = book_soup.find('p', class_='instock availability')
            if availability_tag:
                availability_text = availability_tag.text.strip()
                # Extract number from text like "In stock (22 available)"
                import re
                match = re.search(r'\((\d+) available\)', availability_text)
                if match:
                    return int(match.group(1))
                elif 'In stock' in availability_text:
                    # If no specific count is found but it's in stock, return 1
                    return 1
        except (AttributeError, ValueError):
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
        self.logger.debug("Starting book data extraction")
        title = self._extract_title(book_element)
        price = self._extract_price(book_element)
        rating = self._extract_rating(book_element)
        details = self._extract_book_details(book_element)
        
        book_data = {
            'title': title,
            'price': price,
            'rating': rating,
            'availability': details['availability'],
            'category': details['category']
        }
        
        self.logger.info(f"Successfully extracted: '{title}'")
        return book_data
    
    def _save_to_csv(self, books_data: List[Dict[str, any]]) -> None:
        """
        Save book data to CSV file.
        
        Args:
            books_data: List of dictionaries containing book information
        """
        self.logger.info(f"Saving {len(books_data)} books to CSV file: {self.output_file}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        self.logger.debug(f"Created output directory: {os.path.dirname(self.output_file)}")
        
        fieldnames = ['title', 'price', 'rating', 'availability', 'category']
        
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(books_data)
            self.logger.info(f"Successfully saved {len(books_data)} books to {self.output_file}")
        except Exception as e:
            self.logger.error(f"Failed to save data to CSV: {e}")
            raise
    
    def scrape_books(self) -> None:
        """
        Main method to scrape all books from the website.
        
        This method iterates through all pages, extracts book data,
        and saves it to a CSV file.
        """
        self.logger.info("Starting book scraping process")
        all_books = []
        page_num = 1
        limited_pages = self.max_pages  # Use the max_pages parameter
        books_processed = 0

        while limited_pages == 0 or page_num <= limited_pages:
            try:
                url = self.BASE_URL.format(page_num)
                self.logger.info(f"Scraping page {page_num}: {url}")
                
                soup = self._fetch_page(url)
                if soup is None:
                    self.logger.info(f"No more pages available. Stopped at page {page_num}")
                    break
                
                books = soup.find_all('article', class_='product_pod')
                if not books:
                    self.logger.info(f"No books found on page {page_num}. Reached end of content.")
                    break
                
                self.logger.info(f"Found {len(books)} books on page {page_num}")
                
                page_books_processed = 0
                for book in tqdm(books, desc=f"Processing books on page {page_num}", unit="book"):
                    try:
                        book_data = self._extract_book_data(book)
                        all_books.append(book_data)
                        books_processed += 1
                        page_books_processed += 1
                        # Removed debug log to avoid cluttering with tqdm
                    except Exception as e:
                        self.logger.error(f"Failed to process book {books_processed + 1} on page {page_num}: {e}")
                        continue
                
                self.logger.info(f"Completed page {page_num}, successfully processed {page_books_processed}/{len(books)} books")
                
                # Add random delay between page requests (but not after the last page)
                if limited_pages == 0 or page_num < limited_pages:
                    self._random_delay()
                
            except KeyboardInterrupt:
                self.logger.warning(f"Scraping interrupted by user at page {page_num}")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error on page {page_num}: {e}")
                self.logger.info("Attempting to continue with next page...")
                
            page_num += 1
        
        # Save the data to CSV file
        try:
            if all_books:
                self._save_to_csv(all_books)
                self.logger.info(f"Scraping complete! Total books processed: {len(all_books)} from {page_num - 1} pages")
                print(f"Scraping complete! {len(all_books)} books saved to {self.output_file}")
            else:
                self.logger.warning("No books were scraped successfully")
                print("Warning: No books were scraped. Please check the website or your connection.")
        except Exception as e:
            self.logger.error(f"Failed to save scraped data: {e}")
            print(f"Error: Failed to save data - {e}")
            raise


def main() -> None:
    """Main function to run the scraper."""
    print("Starting Book Scraper...")
    try:
        scraper = BookScraper()
        scraper.scrape_books()
        print("Scraping completed successfully!")
    except Exception as e:
        print(f"Scraping failed with error: {e}")
        logging.error(f"Scraping failed: {e}")


if __name__ == "__main__":
    main()