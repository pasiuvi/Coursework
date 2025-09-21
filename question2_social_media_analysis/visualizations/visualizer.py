import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os
import numpy as np

def create_visualizations(input_path, output_dir):
    """
    Main function to load data and generate all required visualizations.
    """
    print("--- Starting Visualization Generation ---")
    
    try:
        df = pd.read_csv(input_path)
        print(f"Successfully loaded '{input_path}'.")
    except FileNotFoundError:
        print(f"Error: Visualization failed. File not found at '{input_path}'")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Plots will be saved in '{output_dir}' directory.")
    
    # Set a professional theme for static plots
    sns.set_theme(style="whitegrid")

    # --- Generate each visualization ---
    plot_price_distribution(df, output_dir)
    plot_rating_vs_price_scatter(df, output_dir)
    plot_category_analysis(df, output_dir)
    plot_interactive_analysis(df, output_dir)
    
    print("\n--- Visualization Generation Complete ---")

def plot_price_distribution(df, output_dir):
    """
    Generates and saves a histogram and a box plot for price distribution.
    [cite: 73]
    """
    print("Generating price distribution plots...")
    # 1. Price Distribution Histogram
    plt.figure(figsize=(12, 6))
    sns.histplot(df['price'], bins=30, kde=True)
    plt.title('Distribution of Book Prices', fontsize=16)
    plt.xlabel('Price (£)')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, 'price_distribution_histogram.png'))
    plt.close()

    # 2. Box Plot by Top Categories
    top_categories = df['category'].value_counts().nlargest(10).index
    df_top_cat = df[df['category'].isin(top_categories)]
    
    plt.figure(figsize=(15, 8))
    sns.boxplot(x='category', y='price', data=df_top_cat)
    plt.title('Price Distribution for Top 10 Categories', fontsize=16)
    plt.xlabel('Category')
    plt.ylabel('Price (£)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'price_boxplot_by_category.png'))
    plt.close()
    print("...done.")

def plot_rating_vs_price_scatter(df, output_dir):
    """
    Generates and saves a scatter plot of rating vs. price with a trend line.
    [cite: 74]
    """
    print("Generating rating vs. price scatter plot...")
    plt.figure(figsize=(12, 7))
    sns.regplot(x='rating', y='price', data=df,
                scatter_kws={'alpha':0.4, 's':50},
                line_kws={'color': 'red', 'linestyle':'--'})
    plt.title('Book Price vs. Star Rating', fontsize=16)
    plt.xlabel('Star Rating (1-5)')
    plt.ylabel('Price (£)')
    plt.xticks(ticks=np.arange(1, 6, 1)) # Ensure integer ticks for ratings
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'price_vs_rating_scatter.png'))
    plt.close()
    print("...done.")

def plot_category_analysis(df, output_dir):
    """
    Generates and saves bar charts for category popularity and average ratings.
    [cite: 75]
    """
    print("Generating category analysis bar charts...")
    top_10_categories = df['category'].value_counts().nlargest(10)

    # 1. Category Popularity Bar Chart
    plt.figure(figsize=(12, 7))
    sns.barplot(x=top_10_categories.values, y=top_10_categories.index, hue=top_10_categories.index, palette='viridis', legend=False)
    plt.title('Top 10 Most Popular Book Categories', fontsize=16)
    plt.xlabel('Number of Books')
    plt.ylabel('Category')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'category_popularity.png'))
    plt.close()

    # 2. Average Rating by Category Bar Chart
    avg_rating_by_cat = df.groupby('category')['rating'].mean().loc[top_10_categories.index].sort_values()
    plt.figure(figsize=(12, 7))
    sns.barplot(x=avg_rating_by_cat.values, y=avg_rating_by_cat.index, hue=avg_rating_by_cat.index, palette='plasma', legend=False)
    plt.title('Average Rating for Top 10 Categories', fontsize=16)
    plt.xlabel('Average Rating')
    plt.ylabel('Category')
    plt.xlim(0, 5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'average_rating_by_category.png'))
    plt.close()
    print("...done.")

def plot_interactive_analysis(df, output_dir):
    """
    Generates and saves an interactive scatter plot using Plotly for exploration.
    
    """
    print("Generating interactive Plotly chart...")
    fig = px.scatter(df,
                     x='price',
                     y='rating',
                     color='category',
                     size='availability',
                     hover_name='title',
                     title='Interactive Analysis of Books: Price, Rating, and Availability',
                     labels={'price': 'Price (£)', 'rating': 'Star Rating', 'category': 'Category'})
    
    # Save as an HTML file
    output_file = os.path.join(output_dir, 'interactive_book_analysis.html')
    fig.write_html(output_file)
    print(f"...done. Interactive plot saved to '{output_file}'")


if __name__ == "__main__":
    # Path assumes this script is in 'visualizations' and the data is in 'data'
    input_file_path = '../data/cleaned_books.csv'
    output_directory = 'plots'
    create_visualizations(input_file_path, output_directory)