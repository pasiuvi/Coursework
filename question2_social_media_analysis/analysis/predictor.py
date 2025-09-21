import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def perform_predictive_analysis(file_path):
    """
    Loads cleaned data and runs a series of predictive analyses.
    """
    print("--- Starting Predictive Analysis ---")
    
    try:
        df = pd.read_csv(file_path).dropna(subset=['title', 'category'])
        print(f"Successfully loaded '{file_path}'. Shape: {df.shape}\n")
    except FileNotFoundError:
        print(f"Error: Analysis failed. File not found at '{file_path}'")
        return

    # Run each analysis section
    predict_price_from_rating(df.copy())
    analyze_category_pricing(df.copy())
    build_recommendation_system(df.copy())
    analyze_stock_vs_price(df.copy())

    print("--- Predictive Analysis Complete ---")


def predict_price_from_rating(df):
    """
    1. Uses simple linear regression to predict book prices based on ratings.
    """
    print("## 1. Predicting Price from Rating (Linear Regression) ##")
    
    X = df[['rating']] # Feature
    y = df['price']   # Target

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions and evaluate
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    
    print(f"Model Equation: price = {model.coef_[0]:.2f} * rating + {model.intercept_:.2f}")
    print(f"R-squared (R²): {r2:.3f}")
    print(f"Mean Squared Error: {mse:.2f}")
    
    if r2 < 0:
        print("Interpretation: The negative R² value indicates that the model performs worse than simply predicting the mean price for all books.")
    else:
        print(f"Interpretation: The model explains {r2*100:.1f}% of the variance in book prices.")
    
    print("Overall: Star rating alone is a very poor predictor of a book's price.")
    print("-" * 50 + "\n")


def analyze_category_pricing(df):
    """
    2. Identifies and displays patterns in category pricing.
    """
    print("## 2. Identifying Patterns in Category Pricing ##")
    
    # Group by category and calculate price statistics
    category_prices = df.groupby('category')['price'].agg(['mean', 'median', 'count']).sort_values('mean', ascending=False)
    
    print("Top 5 Most Expensive Categories (by mean price):")
    print(category_prices.head(5))
    print("\nTop 5 Least Expensive Categories (by mean price):")
    print(category_prices.tail(5))
    print("-" * 50 + "\n")


def build_recommendation_system(df):
    """
    3. Creates a basic recommendation system using statistical similarity.
    """
    print("## 3. Basic Recommendation System (by Category Similarity) ##")

    # Use TF-IDF to vectorize the 'category' text
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['category'])
    
    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Create a mapping from book title to index
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    def get_recommendations(title, cosine_sim=cosine_sim, indices=indices):
        if title not in indices:
            return f"Book with title '{title}' not found."
        
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6] # Get top 5, excluding the book itself
        book_indices = [i[0] for i in sim_scores]
        return df['title'].iloc[book_indices]

    # --- Demonstrate the recommender ---
    # Pick a sample book to get recommendations for
    sample_title = df['title'].iloc[0] 
    recommendations = get_recommendations(sample_title)
    
    print(f"Recommendations for '{sample_title}':")
    print(recommendations)
    print("\nInterpretation: The system recommends books from the same or very similar categories.")
    print("-" * 50 + "\n")


def analyze_stock_vs_price(df):
    """
    4. Analyzes trends in stock availability versus pricing.
    """
    print("## 4. Analyzing Stock Availability vs. Price ##")
    
    # Calculate the Pearson correlation coefficient
    correlation = df['availability'].corr(df['price'])
    
    print(f"Pearson Correlation between Availability and Price: {correlation:.3f}")
    print("Interpretation: A correlation near 0 suggests there is no linear relationship between a book's price and its stock level.")
    print("-" * 50)


if __name__ == "__main__":
    # Path assumes this script is in 'analysis' and the data is in 'data'
    input_file_path = '../data/cleaned_books.csv'
    perform_predictive_analysis(input_file_path)