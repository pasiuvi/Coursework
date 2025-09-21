import pandas as pd
import re
import os

def clean_text(text):
    """
    Cleans and normalizes a string by converting to lowercase and removing
    special characters, keeping only alphanumeric characters and spaces.
    
    Args:
        text (str): The input string to clean.
        
    Returns:
        str: The cleaned string.
    """
    if not isinstance(text, str):
        return '' # Return an empty string for non-string inputs (like NaN)
    
    text = text.lower()  # Normalize text to lowercase
    # Remove all characters that are not letters, numbers, or spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = text.strip() # Remove leading/trailing whitespace
    return text

def handle_missing_values(df):
    """
    Handles missing values in the DataFrame.
    - Fills missing 'price', 'rating', 'availability' with 0.
    - Fills missing 'category' with 'Unknown'.
    - Drops rows where the 'title' is missing.

    Args:
        df (pd.DataFrame): The input DataFrame.
        
    Returns:
        pd.DataFrame: The DataFrame with missing values handled.
    """
    print("Handling missing values...")
    
    # Fill numerical columns with 0
    for col in ['price', 'rating', 'availability']:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    # Fill categorical columns with a placeholder
    if 'category' in df.columns:
        df['category'] = df['category'].fillna('Unknown')

    # Drop rows with no title, as they are not useful
    df.dropna(subset=['title'], inplace=True)
    
    return df

def process_data(input_path, output_path):
    """
    Main function to load, clean, and save the book data.
    """
    print(f"Starting data processing for {input_path}...")
    
    try:
        df = pd.read_csv(input_path)
        print(f"Successfully loaded data. Initial shape: {df.shape}")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return

    # --- 1. Handle Duplicates ---
    # Removes duplicate rows based on the book title [cite: 56]
    initial_rows = len(df)
    df.drop_duplicates(subset=['title'], keep='first', inplace=True)
    rows_after_duplicates = len(df)
    print(f"Removed {initial_rows - rows_after_duplicates} duplicate entries.")
    
    # --- 2. Handle Missing Data ---
    # Fills or removes rows with missing information [cite: 56]
    df = handle_missing_values(df)

    # --- 3. Text Preprocessing ---
    # Cleans the 'title' and 'category' fields using regex [cite: 55]
    print("Applying text preprocessing to 'title' and 'category' columns...")
    if 'title' in df.columns:
        df['title'] = df['title'].apply(clean_text)
    if 'category' in df.columns:
        df['category'] = df['category'].apply(clean_text)

    # Remove any rows that might have become empty after cleaning the title
    df = df[df['title'] != '']
    
    print(f"Data cleaning complete. Final shape: {df.shape}")

    # --- 4. Save Cleaned Data ---
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data successfully saved to {output_path}")

if __name__ == "__main__":
    # Define file paths based on the project structure
    # Assumes this script is in 'data_processing' and data is in 'data'
    input_csv_path = '../data/scraped_books.csv'
    output_csv_path = '../data/cleaned_books.csv'
    
    process_data(input_csv_path, output_csv_path)