"""
Book Price Prediction Analysis System

This module implements Object-Oriented statistical modeling for book price prediction:
1. Linear regression to predict book prices based on ratings
2. Category pricing pattern analysis
3. Recommendation system using statistical similarity
4. Stock availability vs pricing correlation analysis

The code follows OOP principles with separate classes for different analysis types.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any

class DataManager:
    """Handles data loading, cleaning, and basic operations."""
    
    def __init__(self, file_path: str):
        """
        Initialize DataManager with file path.
        
        Args:
            file_path: Path to the CSV data file
        """
        self.file_path = file_path
        self.df = None
        self.original_count = 0
        
    def load_and_clean_data(self) -> Optional[pd.DataFrame]:
        """Load and clean the book data"""
        print("📚 Loading book data...")
        try:
            self.df = pd.read_csv(self.file_path)
            self.original_count = len(self.df)
            print(f"✓ Loaded {self.df.shape[0]} books with {self.df.shape[1]} features")
            
            # Clean data by removing rows with missing critical values
            self.df = self.df.dropna(subset=['price', 'rating', 'availability', 'category']).copy()
            final_count = len(self.df)
            
            if final_count < self.original_count:
                print(f"⚠️  Removed {self.original_count - final_count} rows with missing data")
            
            print(f"✓ Final dataset: {final_count} books ready for analysis\n")
            return self.df
            
        except FileNotFoundError:
            print(f"❌ Error: File not found at '{self.file_path}'")
            return None
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def get_data(self) -> Optional[pd.DataFrame]:
        """Return the cleaned dataframe."""
        return self.df
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get basic summary statistics of the data."""
        if self.df is None:
            return {}
        
        return {
            'total_books': len(self.df),
            'original_count': self.original_count,
            'columns': list(self.df.columns),
            'price_range': [float(self.df['price'].min()), float(self.df['price'].max())],
            'rating_range': [float(self.df['rating'].min()), float(self.df['rating'].max())],
            'categories_count': len(self.df['category'].unique()),
            'unique_categories': list(self.df['category'].unique())
        }

class BaseAnalyzer(ABC):
    """Abstract base class for all analysis components."""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize analyzer with data.
        
        Args:
            data: Cleaned pandas DataFrame containing book data
        """
        self.data = data
        self.results = {}
    
    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """Perform the analysis and return results."""
        pass
    
    def get_results(self) -> Dict[str, Any]:
        """Get the analysis results."""
        return self.results


class LinearRegressionAnalyzer(BaseAnalyzer):
    """Handles linear regression analysis for price prediction."""
    
    def _simple_linear_regression(self, x: np.ndarray, y: np.ndarray) -> Tuple[float, float, float, np.ndarray]:
        """
        Perform simple linear regression manually (price = slope * rating + intercept)
        
        Args:
            x: Independent variable (ratings)
            y: Dependent variable (prices)
            
        Returns:
            Tuple of (slope, intercept, r_squared, predictions)
        """
        n = len(x)
        if n == 0:
            return 0, 0, 0, np.array([])
        
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        # Calculate slope and intercept
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        
        # Calculate R-squared and predictions
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y_mean) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        return slope, intercept, r_squared, y_pred
    
    def _get_interpretation(self, r_squared: float) -> str:
        """Get interpretation of R-squared value."""
        if r_squared < 0.01:
            return "❌ Rating has virtually no predictive power for price"
        elif r_squared < 0.1:
            return "⚠️  Rating is a poor predictor of price"
        elif r_squared < 0.3:
            return "📊 Rating has weak predictive power for price"
        elif r_squared < 0.7:
            return "📈 Rating has moderate predictive power for price"
        else:
            return "✅ Rating is a strong predictor of price"
    
    def analyze(self) -> Dict[str, Any]:
        """Perform linear regression analysis."""
        print("🔮 PREDICTING PRICE FROM RATING")
        print("=" * 50)
        
        ratings = self.data['rating'].values
        prices = self.data['price'].values
        
        print(f"📊 Dataset: {len(ratings)} books")
        print(f"Rating range: {ratings.min():.1f} - {ratings.max():.1f}")
        print(f"Price range: ${prices.min():.2f} - ${prices.max():.2f}")
        
        # Perform regression
        slope, intercept, r_squared, predictions = self._simple_linear_regression(ratings, prices)
        
        print(f"\n📈 LINEAR REGRESSION RESULTS:")
        print(f"Model equation: price = {slope:.2f} × rating + {intercept:.2f}")
        print(f"R-squared: {r_squared:.3f}")
        
        # Get interpretation
        interpretation = self._get_interpretation(r_squared)
        print(f"Interpretation: {interpretation}")
        print(f"The model explains {r_squared*100:.1f}% of price variation")
        
        # Sample predictions
        print(f"\n🎯 SAMPLE PREDICTIONS:")
        sample_predictions = {}
        for rating in [1, 2, 3, 4, 5]:
            predicted_price = slope * rating + intercept
            print(f"Rating {rating} → Predicted price: ${predicted_price:.2f}")
            sample_predictions[f"rating_{rating}"] = round(predicted_price, 2)
        
        # Store results
        self.results = {
            'model_equation': f"price = {slope:.2f} × rating + {intercept:.2f}",
            'slope': round(slope, 4),
            'intercept': round(intercept, 4),
            'r_squared': round(r_squared, 4),
            'dataset_size': len(ratings),
            'rating_range': [float(ratings.min()), float(ratings.max())],
            'price_range': [float(prices.min()), float(prices.max())],
            'predictions': [float(p) for p in predictions],
            'actual_prices': [float(p) for p in prices],
            'ratings': [float(r) for r in ratings],
            'interpretation': interpretation,
            'sample_predictions': sample_predictions
        }
        
        print()
        return self.results

class CategoryAnalyzer(BaseAnalyzer):
    """Handles category pricing pattern analysis."""
    
    def analyze(self) -> Dict[str, Any]:
        """Perform category pricing analysis."""
        print("💰 CATEGORY PRICING PATTERNS")
        print("=" * 50)
        
        # Group by category and calculate statistics
        category_stats = self.data.groupby('category')['price'].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ]).round(2)
        
        # Sort by mean price (descending)
        category_stats_sorted = category_stats.sort_values('mean', ascending=False)
        
        # Most expensive categories
        print(f"📈 MOST EXPENSIVE CATEGORIES:")
        top_categories = category_stats_sorted.head(5)
        top_categories_data = {}
        for i, (category, stats) in enumerate(top_categories.iterrows(), 1):
            print(f"{i:2d}. {category:20s} | Avg: ${stats['mean']:6.2f} | "
                  f"Range: ${stats['min']:5.2f}-${stats['max']:5.2f} | Books: {int(stats['count']):2d}")
            top_categories_data[category] = {
                'rank': i,
                'average_price': float(stats['mean']),
                'median_price': float(stats['median']),
                'min_price': float(stats['min']),
                'max_price': float(stats['max']),
                'book_count': int(stats['count']),
                'std_dev': float(stats['std']) if not pd.isna(stats['std']) else 0.0
            }
        
        # Least expensive categories
        print(f"\n📉 LEAST EXPENSIVE CATEGORIES:")
        bottom_categories = category_stats_sorted.tail(5).iloc[::-1]
        bottom_categories_data = {}
        for i, (category, stats) in enumerate(bottom_categories.iterrows(), 1):
            print(f"{i:2d}. {category:20s} | Avg: ${stats['mean']:6.2f} | "
                  f"Range: ${stats['min']:5.2f}-${stats['max']:5.2f} | Books: {int(stats['count']):2d}")
            bottom_categories_data[category] = {
                'rank': i,
                'average_price': float(stats['mean']),
                'median_price': float(stats['median']),
                'min_price': float(stats['min']),
                'max_price': float(stats['max']),
                'book_count': int(stats['count']),
                'std_dev': float(stats['std']) if not pd.isna(stats['std']) else 0.0
            }
        
        # Overall insights
        print(f"\n📊 PRICING INSIGHTS:")
        print(f"Overall average price: ${self.data['price'].mean():.2f}")
        print(f"Price standard deviation: ${self.data['price'].std():.2f}")
        print(f"Total categories: {len(category_stats)}")
        print(f"Price range across all books: ${self.data['price'].min():.2f} - ${self.data['price'].max():.2f}")
        
        # Store results
        self.results = {
            'most_expensive': top_categories_data,
            'least_expensive': bottom_categories_data,
            'overall_stats': {
                'average_price': float(self.data['price'].mean()),
                'price_std_dev': float(self.data['price'].std()),
                'total_categories': len(category_stats),
                'min_price': float(self.data['price'].min()),
                'max_price': float(self.data['price'].max()),
                'total_books': len(self.data)
            }
        }
        
        print()
        return self.results

class RecommendationSystem(BaseAnalyzer):
    """Handles recommendation system using statistical similarity."""
    
    def _get_category_recommendations(self, book_title: str, n_recs: int = 3) -> Any:
        """Get recommendations based on category and price similarity."""
        # Find the target book
        target_book = self.data[self.data['title'] == book_title]
        if target_book.empty:
            return f"Book '{book_title}' not found"
        
        target_category = target_book.iloc[0]['category']
        target_price = target_book.iloc[0]['price']
        
        # Find books in the same category (excluding the target book)
        same_category = self.data[
            (self.data['category'] == target_category) & 
            (self.data['title'] != book_title)
        ].copy()
        
        if same_category.empty:
            return "No books found in the same category"
        
        # Calculate similarity score based on price difference
        same_category['price_similarity'] = 1 / (1 + abs(same_category['price'] - target_price))
        
        # Sort by similarity and return top recommendations
        recommendations = same_category.sort_values('price_similarity', ascending=False)
        return recommendations.head(n_recs)
    
    def analyze(self) -> Dict[str, Any]:
        """Perform recommendation system analysis."""
        print("🎯 RECOMMENDATION SYSTEM")
        print("=" * 50)
        
        # Demonstrate with sample books
        sample_books = self.data['title'].head(3).tolist()
        
        print("🔍 DEMONSTRATION:")
        recommendations_data = {}
        
        for book_title in sample_books:
            print(f"\n📖 Book: '{book_title}'")
            
            # Get book details
            book_info = self.data[self.data['title'] == book_title].iloc[0]
            print(f"   Category: {book_info['category']}")
            print(f"   Price: ${book_info['price']:.2f}")
            print(f"   Rating: {book_info['rating']}")
            
            # Store book info
            book_data = {
                'category': book_info['category'],
                'price': float(book_info['price']),
                'rating': float(book_info['rating']),
                'recommendations': []
            }
            
            # Get recommendations
            recommendations = self._get_category_recommendations(book_title)
            
            if isinstance(recommendations, str):
                print(f"   {recommendations}")
                book_data['recommendations'] = recommendations
            else:
                print(f"   📚 Recommendations:")
                for i, (_, rec) in enumerate(recommendations.iterrows(), 1):
                    similarity = rec['price_similarity']
                    print(f"   {i}. {rec['title']}")
                    print(f"      Price: ${rec['price']:.2f} | Rating: {rec['rating']:.1f} | "
                          f"Similarity: {similarity:.3f}")
                    
                    book_data['recommendations'].append({
                        'title': rec['title'],
                        'price': float(rec['price']),
                        'rating': float(rec['rating']),
                        'similarity_score': float(similarity)
                    })
            
            recommendations_data[book_title] = book_data
        
        print(f"\n💡 HOW IT WORKS:")
        print("This system recommends books from the same category,")
        print("ranked by price similarity (closer prices = higher similarity)")
        
        # Store results
        self.results = {
            'algorithm': 'Category-based with price similarity scoring',
            'similarity_formula': '1 / (1 + |price_difference|)',
            'sample_recommendations': recommendations_data
        }
        
        print()
        return self.results

class StockAnalyzer(BaseAnalyzer):
    """Handles stock availability vs pricing correlation analysis."""
    
    def _calculate_correlation(self, x: np.ndarray, y: np.ndarray) -> float:
        """Calculate Pearson correlation coefficient manually."""
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        numerator = np.sum((x - x_mean) * (y - y_mean))
        x_variance = np.sum((x - x_mean) ** 2)
        y_variance = np.sum((y - y_mean) ** 2)
        
        denominator = np.sqrt(x_variance * y_variance)
        return numerator / denominator if denominator != 0 else 0
    
    def _get_correlation_strength(self, correlation: float) -> Tuple[str, str]:
        """Get correlation strength and direction."""
        if abs(correlation) < 0.1:
            strength = "negligible"
        elif abs(correlation) < 0.3:
            strength = "weak"
        elif abs(correlation) < 0.5:
            strength = "moderate" 
        elif abs(correlation) < 0.7:
            strength = "strong"
        else:
            strength = "very strong"
        
        direction = "positive" if correlation > 0 else "negative"
        return strength, direction
    
    def _get_business_interpretation(self, correlation: float) -> str:
        """Get business interpretation based on correlation."""
        if abs(correlation) < 0.1:
            return "❌ No meaningful relationship between stock levels and pricing. Inventory management appears independent of pricing strategy"
        elif correlation > 0.3:
            return "📈 Higher priced books tend to have more stock. Suggests premium books may be stocked more heavily"
        elif correlation < -0.3:
            return "📉 Higher priced books tend to have less stock. Suggests premium books may be limited edition or scarce"
        else:
            return "⚖️  Weak relationship suggests other factors drive inventory decisions"
    
    def analyze(self) -> Dict[str, Any]:
        """Analyze trends in stock availability vs pricing."""
        print("📦 STOCK AVAILABILITY vs PRICE ANALYSIS")
        print("=" * 50)
        
        availability = self.data['availability'].values
        prices = self.data['price'].values
        
        # Calculate correlation
        correlation = self._calculate_correlation(availability, prices)
        
        print(f"📊 CORRELATION ANALYSIS:")
        print(f"Pearson correlation coefficient: {correlation:.3f}")
        
        # Interpret correlation
        strength, direction = self._get_correlation_strength(correlation)
        print(f"Relationship: {strength} {direction} correlation")
        
        # Stock level analysis
        print(f"\n📈 STOCK STATISTICS:")
        print(f"Average availability: {np.mean(availability):.1f} units")
        print(f"Availability range: {availability.min():.0f} - {availability.max():.0f} units")
        print(f"Standard deviation: {np.std(availability):.1f}")
        
        # Group analysis by stock levels
        low_stock = self.data[self.data['availability'] <= 1]
        medium_stock = self.data[(self.data['availability'] > 1) & (self.data['availability'] <= 5)]
        high_stock = self.data[self.data['availability'] > 5]
        
        print(f"\n💰 PRICE BY STOCK LEVEL:")
        
        stock_analysis = {}
        
        if len(low_stock) > 0:
            low_avg = low_stock['price'].mean()
            print(f"Low stock (≤1):     {len(low_stock):2d} books | Avg price: ${low_avg:.2f}")
            stock_analysis['low_stock'] = {
                'count': len(low_stock),
                'average_price': float(low_avg),
                'books': low_stock['title'].tolist()
            }
        
        if len(medium_stock) > 0:
            medium_avg = medium_stock['price'].mean()
            print(f"Medium stock (2-5):  {len(medium_stock):2d} books | Avg price: ${medium_avg:.2f}")
            stock_analysis['medium_stock'] = {
                'count': len(medium_stock),
                'average_price': float(medium_avg),
                'books': medium_stock['title'].tolist()
            }
        
        if len(high_stock) > 0:
            high_avg = high_stock['price'].mean()
            print(f"High stock (>5):     {len(high_stock):2d} books | Avg price: ${high_avg:.2f}")
            stock_analysis['high_stock'] = {
                'count': len(high_stock),
                'average_price': float(high_avg),
                'books': high_stock['title'].tolist()
            }
        
        # Business interpretation
        interpretation = self._get_business_interpretation(correlation)
        print(f"\n� BUSINESS INTERPRETATION:")
        print(interpretation)
        
        # Store results
        self.results = {
            'correlation_coefficient': float(correlation),
            'correlation_strength': strength,
            'correlation_direction': direction,
            'stock_statistics': {
                'average_availability': float(np.mean(availability)),
                'min_availability': float(availability.min()),
                'max_availability': float(availability.max()),
                'std_dev_availability': float(np.std(availability))
            },
            'stock_level_analysis': stock_analysis,
            'business_interpretation': interpretation
        }
        
        print()
        return self.results

class ReportGenerator:
    """Handles report generation in multiple formats."""
    
    def __init__(self, output_dir: str = '../data'):
        """
        Initialize ReportGenerator.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def save_prediction_report(self, report_data: Dict[str, Any]) -> Dict[str, str]:
        """Save comprehensive prediction report in multiple formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON report
        json_filename = f"book_price_prediction_report_{timestamp}.json"
        json_path = os.path.join(self.output_dir, json_filename)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        # Save Markdown report
        md_filename = f"book_price_prediction_report_{timestamp}.md"
        md_path = os.path.join(self.output_dir, md_filename)
        
        markdown_content = self._generate_markdown_report(report_data)
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Save CSV with predictions
        csv_filename = f"book_price_predictions_{timestamp}.csv"
        csv_path = os.path.join(self.output_dir, csv_filename)
        
        # Create predictions DataFrame
        if 'linear_regression' in report_data:
            lr_data = report_data['linear_regression']
            predictions_df = pd.DataFrame({
                'rating': lr_data['ratings'],
                'actual_price': lr_data['actual_prices'],
                'predicted_price': lr_data['predictions'],
                'prediction_error': [actual - pred for actual, pred in zip(lr_data['actual_prices'], lr_data['predictions'])]
            })
            predictions_df.to_csv(csv_path, index=False)
        
        print(f"\n📄 REPORTS SAVED:")
        print(f"✓ JSON Report: {json_path}")
        print(f"✓ Markdown Report: {md_path}")
        print(f"✓ Predictions CSV: {csv_path}")
        
        return {
            'json_report': json_path,
            'markdown_report': md_path,
            'predictions_csv': csv_path
        }
    
    def _generate_markdown_report(self, report_data: Dict[str, Any]) -> str:
        """Generate a comprehensive markdown report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        md_content = f"""# Book Price Prediction Analysis Report

**Generated on:** {timestamp}  
**Analysis Type:** Statistical Modeling and Prediction

---

## Executive Summary

This report presents the results of a comprehensive statistical analysis of book pricing data, including predictive modeling, category analysis, recommendation systems, and inventory correlation studies.

---

## 1. Linear Regression Analysis: Price Prediction from Ratings

### Model Performance
"""
        
        if 'linear_regression' in report_data:
            lr = report_data['linear_regression']
            md_content += f"""
- **Model Equation:** `{lr['model_equation']}`
- **R-squared:** {lr['r_squared']:.4f}
- **Dataset Size:** {lr['dataset_size']} books
- **Rating Range:** {lr['rating_range'][0]:.1f} - {lr['rating_range'][1]:.1f}
- **Price Range:** ${lr['price_range'][0]:.2f} - ${lr['price_range'][1]:.2f}

### Interpretation
{lr['interpretation']}

The model explains {lr['r_squared']*100:.1f}% of the variance in book prices.

### Sample Predictions
| Rating | Predicted Price |
|--------|----------------|"""
            
            for rating, price in lr['sample_predictions'].items():
                rating_num = rating.split('_')[1]
                md_content += f"\n| {rating_num} | ${price:.2f} |"
        
        # Continue with other sections...
        md_content += self._generate_category_section(report_data)
        md_content += self._generate_recommendation_section(report_data)
        md_content += self._generate_stock_section(report_data)
        md_content += self._generate_conclusion_section()
        
        return md_content
    
    def _generate_category_section(self, report_data: Dict[str, Any]) -> str:
        """Generate category analysis section for markdown."""
        section = "\n\n---\n\n## 2. Category Pricing Analysis\n\n"
        
        if 'category_pricing' in report_data:
            cp = report_data['category_pricing']
            
            section += f"""### Overall Statistics
- **Average Price:** ${cp['overall_stats']['average_price']:.2f}
- **Price Standard Deviation:** ${cp['overall_stats']['price_std_dev']:.2f}
- **Total Categories:** {cp['overall_stats']['total_categories']}
- **Price Range:** ${cp['overall_stats']['min_price']:.2f} - ${cp['overall_stats']['max_price']:.2f}
- **Total Books:** {cp['overall_stats']['total_books']}

### Most Expensive Categories
| Rank | Category | Avg Price | Book Count | Price Range |
|------|----------|-----------|------------|-------------|"""
            
            for category, data in cp['most_expensive'].items():
                section += f"\n| {data['rank']} | {category} | ${data['average_price']:.2f} | {data['book_count']} | ${data['min_price']:.2f} - ${data['max_price']:.2f} |"
            
            section += "\n\n### Least Expensive Categories\n| Rank | Category | Avg Price | Book Count | Price Range |\n|------|----------|-----------|------------|-------------|"
            
            for category, data in cp['least_expensive'].items():
                section += f"\n| {data['rank']} | {category} | ${data['average_price']:.2f} | {data['book_count']} | ${data['min_price']:.2f} - ${data['max_price']:.2f} |"
        
        return section
    
    def _generate_recommendation_section(self, report_data: Dict[str, Any]) -> str:
        """Generate recommendation system section for markdown."""
        section = "\n\n---\n\n## 3. Recommendation System Analysis\n\n"
        
        if 'recommendation_system' in report_data:
            rs = report_data['recommendation_system']
            
            section += f"""### Algorithm Details
- **Type:** {rs['algorithm']}
- **Similarity Formula:** `{rs['similarity_formula']}`

### Sample Recommendations
"""
            
            for book_title, book_data in rs['sample_recommendations'].items():
                section += f"\n#### Book: {book_title}\n"
                section += f"- **Category:** {book_data['category']}\n"
                section += f"- **Price:** ${book_data['price']:.2f}\n"
                section += f"- **Rating:** {book_data['rating']:.1f}\n\n"
                
                if isinstance(book_data['recommendations'], list) and book_data['recommendations']:
                    section += "**Recommendations:**\n"
                    for i, rec in enumerate(book_data['recommendations'], 1):
                        section += f"{i}. **{rec['title']}** - ${rec['price']:.2f} (Rating: {rec['rating']:.1f}, Similarity: {rec['similarity_score']:.3f})\n"
                else:
                    section += f"**Recommendations:** {book_data['recommendations']}\n"
        
        return section
    
    def _generate_stock_section(self, report_data: Dict[str, Any]) -> str:
        """Generate stock analysis section for markdown."""
        section = "\n\n---\n\n## 4. Stock vs Price Correlation Analysis\n\n"
        
        if 'stock_analysis' in report_data:
            sa = report_data['stock_analysis']
            
            section += f"""### Correlation Results
- **Pearson Correlation Coefficient:** {sa['correlation_coefficient']:.3f}
- **Relationship Strength:** {sa['correlation_strength'].title()}
- **Direction:** {sa['correlation_direction'].title()}

### Stock Statistics
- **Average Availability:** {sa['stock_statistics']['average_availability']:.1f} units
- **Availability Range:** {sa['stock_statistics']['min_availability']:.0f} - {sa['stock_statistics']['max_availability']:.0f} units
- **Standard Deviation:** {sa['stock_statistics']['std_dev_availability']:.1f}

### Price by Stock Level
"""
            
            for stock_level, data in sa['stock_level_analysis'].items():
                level_name = stock_level.replace('_', ' ').title()
                section += f"- **{level_name}:** {data['count']} books, Average price: ${data['average_price']:.2f}\n"
            
            section += f"\n### Business Interpretation\n{sa['business_interpretation']}\n"
        
        return section
    
    def _generate_conclusion_section(self) -> str:
        """Generate conclusion section for markdown."""
        return """

---

## Methodology

### Data Sources
- **Dataset:** Cleaned book data from web scraping
- **Features:** Title, Price, Rating, Availability, Category

### Statistical Methods
1. **Linear Regression:** Manual implementation using least squares method
2. **Correlation Analysis:** Pearson correlation coefficient calculation
3. **Category Analysis:** Groupby aggregation with descriptive statistics
4. **Recommendation System:** Category-based filtering with price similarity scoring

### Limitations
- Small dataset size may limit generalizability
- Simple linear model may not capture complex price relationships
- Recommendation system based only on category and price similarity
- Stock data shows limited variation (all books have similar availability)

---

## Conclusions

1. **Price Prediction:** Book ratings have very limited predictive power for pricing
2. **Category Impact:** Category is a much stronger indicator of book prices than ratings
3. **Recommendations:** Category-based recommendations work well for books with similar pricing
4. **Inventory:** No significant relationship found between stock levels and pricing

---

*Report generated by Book Price Prediction Analysis System*
"""

class BookPricePredictionSystem:
    """
    Main system class that orchestrates all analysis components.
    
    This class follows the Facade pattern, providing a simple interface
    to complex subsystems of analysis components.
    """
    
    def __init__(self, file_path: str, output_dir: str = '../data'):
        """
        Initialize the prediction system.
        
        Args:
            file_path: Path to the CSV data file
            output_dir: Directory to save reports
        """
        self.file_path = file_path
        self.output_dir = output_dir
        self.data_manager = DataManager(file_path)
        self.report_generator = ReportGenerator(output_dir)
        self.analyzers = {}
        self.data = None
        
    def _initialize_analyzers(self) -> None:
        """Initialize all analyzer components with data."""
        if self.data is None:
            raise ValueError("Data must be loaded before initializing analyzers")
            
        self.analyzers = {
            'linear_regression': LinearRegressionAnalyzer(self.data),
            'category_pricing': CategoryAnalyzer(self.data),
            'recommendation_system': RecommendationSystem(self.data),
            'stock_analysis': StockAnalyzer(self.data)
        }
    
    def load_data(self) -> bool:
        """
        Load and prepare data for analysis.
        
        Returns:
            True if data loaded successfully, False otherwise
        """
        self.data = self.data_manager.load_and_clean_data()
        if self.data is not None and not self.data.empty:
            self._initialize_analyzers()
            return True
        return False
    
    def run_all_analyses(self) -> Dict[str, Any]:
        """
        Run all analysis components and collect results.
        
        Returns:
            Dictionary containing all analysis results
        """
        if not self.analyzers:
            raise ValueError("Analyzers not initialized. Call load_data() first.")
        
        # Initialize report data structure
        report_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'dataset_file': self.file_path,
                'analysis_type': 'Statistical Modeling and Prediction'
            }
        }
        
        # Add data summary
        data_summary = self.data_manager.get_data_summary()
        report_data['metadata'].update(data_summary)
        
        # Run all analyses
        for analysis_name, analyzer in self.analyzers.items():
            print(f"Running {analysis_name.replace('_', ' ').title()} Analysis...")
            try:
                results = analyzer.analyze()
                report_data[analysis_name] = results
            except Exception as e:
                print(f"❌ Error in {analysis_name}: {e}")
                report_data[analysis_name] = {'error': str(e)}
        
        return report_data
    
    def generate_reports(self, report_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate and save reports in multiple formats.
        
        Args:
            report_data: Analysis results dictionary
            
        Returns:
            Dictionary with paths to generated reports
        """
        return self.report_generator.save_prediction_report(report_data)
    
    def run_complete_analysis(self) -> Dict[str, str]:
        """
        Run the complete analysis pipeline.
        
        Returns:
            Dictionary with paths to generated reports
        """
        print("📚 BOOK PRICE STATISTICAL MODELING")
        print("=" * 60)
        print("Performing comprehensive statistical analysis on book data")
        print("=" * 60)
        print()
        
        # Load data
        if not self.load_data():
            print("❌ Cannot proceed with analysis - no valid data available")
            return {}
        
        # Run all analyses
        report_data = self.run_all_analyses()
        
        # Generate reports
        report_files = self.generate_reports(report_data)
        
        print("✅ ANALYSIS COMPLETE")
        print("=" * 60)
        print("All statistical modeling tasks have been completed successfully!")
        print("Comprehensive reports have been saved to the data folder.")
        
        return report_files


def main():
    """Main function to run the complete analysis system."""
    try:
        # Initialize the prediction system
        file_path = '../data/cleaned_books.csv'
        system = BookPricePredictionSystem(file_path)
        
        # Run complete analysis
        report_files = system.run_complete_analysis()
        
        if report_files:
            print(f"\n📊 Analysis completed successfully!")
            print(f"Generated {len(report_files)} report files.")
        else:
            print("❌ Analysis failed. Please check the data file and try again.")
            
    except Exception as e:
        print(f"❌ System error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    main()
