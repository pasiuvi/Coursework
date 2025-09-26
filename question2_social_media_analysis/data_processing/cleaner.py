"""
Comprehensive data cleaning pipeline for social media and text data.

This module provides a robust data cleaning system following OOP principles
and PEP standards for handling messy real-world data.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

import pandas as pd


class DataCleaner:
    """
    A comprehensive data cleaning pipeline that handles various data quality issues.
    
    This class provides methods for text preprocessing, missing data handling,
    duplicate removal, feature extraction, and data validation.
    """
    
    def __init__(self, 
                 numerical_fill_value: float = 0.0,
                 categorical_fill_value: str = 'Unknown',
                 required_columns: Optional[List[str]] = None):
        """
        Initialize the DataCleaner with configurable parameters.
        
        Args:
            numerical_fill_value: Value to fill missing numerical data
            categorical_fill_value: Value to fill missing categorical data
            required_columns: List of columns that must have values
        """
        self.numerical_fill_value = numerical_fill_value
        self.categorical_fill_value = categorical_fill_value
        self.required_columns = required_columns or ['title']
        self.processing_stats = {}
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load data from a CSV file with error handling.
        
        Args:
            file_path: Path to the input CSV file
            
        Returns:
            Loaded DataFrame
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            pd.errors.EmptyDataError: If the file is empty
        """
        try:
            df = pd.read_csv(file_path)
            print(f"Successfully loaded data. Initial shape: {df.shape}")
            self.processing_stats['initial_rows'] = len(df)
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found at {file_path}")
        except pd.errors.EmptyDataError:
            raise pd.errors.EmptyDataError(f"File is empty: {file_path}")
    
    def remove_duplicates(self, df: pd.DataFrame, 
                         subset: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Remove duplicate rows from the DataFrame.
        
        Args:
            df: Input DataFrame
            subset: Columns to consider for identifying duplicates
            
        Returns:
            DataFrame with duplicates removed
        """
        initial_rows = len(df)
        subset = subset or ['title']
        
        df_cleaned = df.drop_duplicates(subset=subset, keep='first')
        
        duplicates_removed = initial_rows - len(df_cleaned)
        print(f"Removed {duplicates_removed} duplicate entries.")
        self.processing_stats['duplicates_removed'] = duplicates_removed
        
        return df_cleaned
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with missing values handled
        """
        print("Handling missing values...")
        df_cleaned = df.copy()
        
        # Fill numerical columns
        numerical_cols = df_cleaned.select_dtypes(include=['float64', 'int64']).columns
        for col in numerical_cols:
            if col in df_cleaned.columns:
                df_cleaned[col] = df_cleaned[col].fillna(self.numerical_fill_value)
        
        # Fill categorical columns
        categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col in df_cleaned.columns and col not in self.required_columns:
                df_cleaned[col] = df_cleaned[col].fillna(self.categorical_fill_value)
        
        # Drop rows with missing required columns
        initial_rows = len(df_cleaned)
        df_cleaned = df_cleaned.dropna(subset=self.required_columns)
        
        missing_handled = initial_rows - len(df_cleaned)
        print(f"Handled missing values. Dropped {missing_handled} rows with missing required data.")
        self.processing_stats['missing_handled'] = missing_handled
        
        return df_cleaned
    
    def clean_text(self, text: Any) -> str:
        """
        Clean and normalize text data.
        
        Args:
            text: Input text to clean
            
        Returns:
            Cleaned text string
        """
        if not isinstance(text, str):
            return ''
        
        # Convert to lowercase and strip whitespace
        text = text.lower().strip()
        
        # Remove special characters, keep alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def extract_hashtags(self, text: str) -> List[str]:
        """
        Extract hashtags from text.
        
        Args:
            text: Input text
            
        Returns:
            List of hashtags found in text
        """
        if not isinstance(text, str):
            return []
        
        hashtags = re.findall(r'#\w+', text)
        return [tag.lower() for tag in hashtags]
    
    def extract_mentions(self, text: str) -> List[str]:
        """
        Extract mentions from text.
        
        Args:
            text: Input text
            
        Returns:
            List of mentions found in text
        """
        if not isinstance(text, str):
            return []
        
        mentions = re.findall(r'@\w+', text)
        return [mention.lower() for mention in mentions]
    
    def extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """
        Extract keywords from text.
        
        Args:
            text: Input text
            min_length: Minimum length for keywords
            
        Returns:
            List of keywords
        """
        if not isinstance(text, str):
            return []
        
        # Simple keyword extraction - split and filter
        words = text.lower().split()
        keywords = [word for word in words if len(word) >= min_length]
        
        return keywords
    
    def standardize_datetime(self, df: pd.DataFrame, 
                           datetime_columns: List[str]) -> pd.DataFrame:
        """
        Standardize datetime columns to a consistent format.
        
        Args:
            df: Input DataFrame
            datetime_columns: List of column names containing datetime data
            
        Returns:
            DataFrame with standardized datetime columns
        """
        df_cleaned = df.copy()
        
        for col in datetime_columns:
            if col in df_cleaned.columns:
                try:
                    df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')
                    print(f"Standardized datetime format for column: {col}")
                except Exception as e:
                    print(f"Warning: Could not standardize datetime for column {col}: {e}")
        
        return df_cleaned
    
    def validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform data validation and quality checks.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary containing validation results
        """
        validation_results = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicate_rows': df.duplicated().sum(),
            'data_types': df.dtypes.to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum()
        }
        
        # Check for empty strings in text columns
        text_columns = df.select_dtypes(include=['object']).columns
        empty_strings = {}
        for col in text_columns:
            empty_count = (df[col] == '').sum()
            if empty_count > 0:
                empty_strings[col] = empty_count
        
        validation_results['empty_strings'] = empty_strings
        
        return validation_results
    
    def convert_prices_to_usd(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert prices from various currencies to USD.
        Detects currency symbols (£, €, $) and converts accordingly.
        If no currency symbol, assumes USD.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with prices converted to USD
        """
        if 'price' not in df.columns:
            print("Warning: No 'price' column found for currency conversion")
            return df
        
        df = df.copy()
        
        # Define conversion rates (as of September 2025)
        rates = {
            '£': 1.27,  # GBP to USD
            '€': 1.10,  # EUR to USD
            '$': 1.0    # USD to USD (no conversion needed)
        }
        
        converted_count = 0
        
        def convert_price(price):
            nonlocal converted_count
            if pd.isna(price):
                return price
            
            # Convert to string to check for currency symbols
            price_str = str(price).strip()
            
            for symbol, rate in rates.items():
                if price_str.startswith(symbol):
                    # Remove symbol and convert
                    numeric_part = price_str[len(symbol):].strip()
                    try:
                        numeric_value = float(numeric_part)
                        converted_value = numeric_value * rate
                        converted_count += 1
                        return round(converted_value, 2)
                    except ValueError:
                        print(f"Warning: Could not convert price '{price_str}'")
                        return price
            
            # No currency symbol found, assume USD
            try:
                return float(price_str)
            except ValueError:
                print(f"Warning: Could not parse price '{price_str}'")
                return price
        
        # Apply conversion
        df['price'] = df['price'].apply(convert_price)
        
        print(f"Converted {converted_count} prices to USD")
        print(f"Assumed {len(df) - converted_count} prices were already in USD")
        
        self.processing_stats['currency_conversion'] = {
            'converted_prices': converted_count,
            'assumed_usd': len(df) - converted_count,
            'rates_used': rates
        }
        
        return df
    
    def preprocess_text_columns(self, df: pd.DataFrame, 
                               text_columns: List[str]) -> pd.DataFrame:
        """
        Apply text preprocessing to specified columns.
        
        Args:
            df: Input DataFrame
            text_columns: List of column names to preprocess
            
        Returns:
            DataFrame with preprocessed text columns
        """
        df_cleaned = df.copy()
        
        print("Applying text preprocessing...")
        for col in text_columns:
            if col in df_cleaned.columns:
                # Store original for feature extraction
                original_col = df_cleaned[col].copy()
                
                # Clean the text
                df_cleaned[col] = df_cleaned[col].apply(self.clean_text)
                
                # Extract features for social media analysis (using original text)
                if 'title' in col.lower() or 'text' in col.lower():
                    # Convert lists to strings for CSV storage
                    hashtags = original_col.apply(self.extract_hashtags)
                    mentions = original_col.apply(self.extract_mentions)
                    keywords = original_col.apply(self.extract_keywords)
                    
                    df_cleaned[f'{col}_hashtags'] = hashtags.apply(lambda x: ','.join(x) if x else '')
                    df_cleaned[f'{col}_mentions'] = mentions.apply(lambda x: ','.join(x) if x else '')
                    df_cleaned[f'{col}_keywords'] = keywords.apply(lambda x: ','.join(x[:5]) if x else '')  # Limit to 5 keywords
        
        # Remove rows with empty text in required columns
        for col in text_columns:
            if col in self.required_columns:
                df_cleaned = df_cleaned[df_cleaned[col] != '']
        
        return df_cleaned
    
    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        """
        Save cleaned data to a CSV file.
        
        Args:
            df: DataFrame to save
            output_path: Path for the output file
        """
        try:
            # Convert to absolute path
            abs_output_path = Path(output_path).resolve()
            
            # Ensure output directory exists
            output_dir = abs_output_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"Saving to absolute path: {abs_output_path}")
            print(f"Directory exists: {output_dir.exists()}")
            
            df.to_csv(abs_output_path, index=False)
            
            # Verify file was created
            if abs_output_path.exists():
                file_size = abs_output_path.stat().st_size
                print(f"Cleaned data successfully saved to {abs_output_path}")
                print(f"File size: {file_size} bytes")
            else:
                print(f"WARNING: File was not created at {abs_output_path}")
                
            self.processing_stats['final_rows'] = len(df)
            
        except Exception as e:
            print(f"Error saving file: {e}")
            import traceback
            traceback.print_exc()
    
    def process_pipeline(self, input_path: str, output_path: str,
                        text_columns: Optional[List[str]] = None,
                        datetime_columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Execute the complete data cleaning pipeline.
        
        Args:
            input_path: Path to input CSV file
            output_path: Path for output CSV file
            text_columns: Columns to apply text preprocessing
            datetime_columns: Columns to standardize datetime format
            
        Returns:
            Cleaned DataFrame
        """
        print(f"Starting comprehensive data cleaning pipeline for {input_path}...")
        
        # Set default columns if not provided
        text_columns = text_columns or ['title', 'category']
        datetime_columns = datetime_columns or []
        
        # Execute pipeline steps
        df = self.load_data(input_path)
        df = self.convert_prices_to_usd(df)
        df = self.remove_duplicates(df)
        df = self.handle_missing_values(df)
        df = self.preprocess_text_columns(df, text_columns)
        
        if datetime_columns:
            df = self.standardize_datetime(df, datetime_columns)
        
        # Validate final data
        validation_results = self.validate_data(df)
        print("\nData validation results:")
        print(f"Final shape: {df.shape}")
        print(f"Missing values: {sum(validation_results['missing_values'].values())}")
        
        # Save cleaned data
        self.save_data(df, output_path)
        
        # Print processing summary
        self._print_processing_summary()
        
        return df
    
    def _print_processing_summary(self) -> None:
        """Print a summary of the processing statistics."""
        print("\n" + "="*50)
        print("DATA CLEANING SUMMARY")
        print("="*50)
        
        initial = self.processing_stats.get('initial_rows', 0)
        final = self.processing_stats.get('final_rows', 0)
        duplicates = self.processing_stats.get('duplicates_removed', 0)
        missing = self.processing_stats.get('missing_handled', 0)
        
        print(f"Initial rows: {initial}")
        print(f"Duplicates removed: {duplicates}")
        print(f"Missing data handled: {missing}")
        print(f"Final rows: {final}")
        print(f"Total rows processed: {initial - final}")
        print(f"Data retention rate: {(final/initial)*100:.2f}%" if initial > 0 else "N/A")
        
        # Print currency conversion info if available
        currency_info = self.processing_stats.get('currency_conversion')
        if currency_info:
            print(f"Currency conversion: {currency_info['converted_prices']} prices converted, {currency_info['assumed_usd']} assumed USD")
            print(f"Exchange rates used: {currency_info['rates_used']}")


def main():
    """Main function to run the data cleaning pipeline."""
    # Initialize the data cleaner
    cleaner = DataCleaner(
        numerical_fill_value=0.0,
        categorical_fill_value='Unknown',
        required_columns=['title']
    )
    
    # Define file paths using absolute paths to work from any directory
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / 'data'
    input_path = str(data_dir / 'scraped_books.csv')
    output_path = str(data_dir / 'cleaned_books.csv')
    
    try:
        # Run the complete pipeline
        cleaned_df = cleaner.process_pipeline(
            input_path=input_path,
            output_path=output_path,
            text_columns=['title', 'category'],
            datetime_columns=[]  # Add datetime columns if present
        )
        
        print(f"\nData cleaning pipeline completed successfully!")
        print(f"Input file: {input_path}")
        print(f"Output file: {output_path}")
        print(f"Output file exists: {Path(output_path).exists()}")
        
    except Exception as e:
        print(f"Error during data cleaning: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()