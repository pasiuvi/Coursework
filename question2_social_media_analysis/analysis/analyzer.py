import pandas as pd
import numpy as np
from scipy import stats

def perform_analysis(file_path):
    """
    Loads the cleaned book data and performs advanced statistical analysis.
    """
    print("--- Starting Advanced Statistical Analysis ---")
    
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded '{file_path}'. Shape: {df.shape}\n")
    except FileNotFoundError:
        print(f"Error: Analysis failed. File not found at '{file_path}'")
        return

    numerical_cols = ['price', 'rating', 'availability']

    # --- 1. Descriptive Statistics ---
    # Calculates mean, median, mode, and standard deviation[cite: 69].
    print("## 1. Descriptive Statistics ##")
    print("Summary for numerical columns:")
    print(df[numerical_cols].describe())
    print("\nMedian values:")
    print(df[numerical_cols].median())
    print("\nMode values:")
    print(df[numerical_cols].mode().iloc[0]) # Display the first mode if multiple exist
    print("-" * 40 + "\n")

    # --- 2. Outlier Identification ---
    # Identifies outliers in pricing and ratings using the IQR method[cite: 70].
    print("## 2. Outlier Identification (using IQR method) ##")
    for col in ['price', 'rating']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        
        print(f"Found {len(outliers)} outliers in '{col}' (values outside {lower_bound:.2f}-{upper_bound:.2f}).")
        if not outliers.empty:
            print(f"Examples of outlier prices:\n{outliers.head()}\n")
    print("-" * 40 + "\n")

    # --- 3. Correlation Analysis ---
    # Performs correlation analysis between numerical variables[cite: 71].
    print("## 3. Correlation Analysis ##")
    correlation_matrix = df[numerical_cols].corr()
    print("Correlation matrix between price, rating, and availability:")
    print(correlation_matrix)
    print("\nInterpretation: Values close to 1 or -1 indicate a strong linear relationship.")
    print("-" * 40 + "\n")

    # --- 4. Frequency Distribution for Categories ---
    # Creates a frequency distribution for categorical data to analyze popularity[cite: 72, 66].
    print("## 4. Category Popularity Analysis ##")
    category_counts = df['category'].value_counts()
    print("Top 10 most popular book categories:")
    print(category_counts.head(10))
    print("-" * 40 + "\n")

    # --- 5. Hypothesis Testing ---
    # Uses a t-test to compare the prices of two categories (e.g., fiction vs. science)[cite: 73].
    print("## 5. Hypothesis Testing (Fiction vs. Science Prices) ##")
    
    # Create two sample groups
    fiction_prices = df[df['category'] == 'fiction']['price']
    science_prices = df[df['category'] == 'science']['price']

    if len(fiction_prices) > 1 and len(science_prices) > 1:
        # State hypotheses
        print("H₀ (Null Hypothesis): The mean price of Fiction books is equal to the mean price of Science books.")
        print("H₁ (Alternative Hypothesis): The mean prices are not equal.\n")
        
        # Perform independent t-test
        t_stat, p_value = stats.ttest_ind(fiction_prices, science_prices, equal_var=False) # Welch's t-test
        
        print(f"T-statistic: {t_stat:.4f}")
        print(f"P-value: {p_value:.4f}")
        
        # Interpret the result
        alpha = 0.05
        if p_value < alpha:
            print(f"\nConclusion: Since the p-value ({p_value:.4f}) is less than {alpha}, we reject the null hypothesis.")
            print("There is a statistically significant difference in prices between Fiction and Science books.")
        else:
            print(f"\nConclusion: Since the p-value ({p_value:.4f}) is greater than {alpha}, we fail to reject the null hypothesis.")
            print("There is not enough evidence to claim a significant difference in prices.")
    else:
        print("Could not perform hypothesis test: not enough data for 'fiction' or 'science' categories.")
        
    print("-" * 40)
    print("--- Analysis Complete ---")


if __name__ == "__main__":
    # Path assumes this script is in 'analysis' and the data is in 'data'
    input_file_path = '../data/cleaned_books.csv'
    perform_analysis(input_file_path)