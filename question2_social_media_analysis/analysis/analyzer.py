"""
Book Data Analyzer Module

This module provides a simplified, comprehensive statistical analysis for book data,
including descriptive statistics, outlier detection, correlation, frequency distribution,
and hypothesis testing.

Author: GitHub Copilot
Date: September 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json
from datetime import datetime
from typing import Dict, Any
from scipy.stats import ttest_ind

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BookDataAnalyzer:
    """
    A simplified book data analyzer that performs key statistical analyses and
    generates a comprehensive report.
    """
    
    def __init__(self, data_path: str):
        """
        Initialize the analyzer and load data.
        
        Args:
            data_path: Path to the cleaned CSV data file.
        """
        self.data_path = data_path
        self.df = self._load_data()
        
    def _load_data(self) -> pd.DataFrame:
        """Loads data from the specified CSV file."""
        try:
            df = pd.read_csv(self.data_path)
            logger.info(f"Successfully loaded {len(df)} records from {self.data_path}")
            
            if 'rating' not in df.columns and 'rating_num' in df.columns:
                df['rating'] = df['rating_num']
                
            return df
        except FileNotFoundError:
            logger.error(f"Data file not found: {self.data_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """
        Generates a single, comprehensive analysis report with key insights.
        
        Returns:
            A dictionary containing the full analysis report.
        """
        if self.df is None or self.df.empty:
            logger.warning("DataFrame is empty. Cannot generate report.")
            return {}

        logger.info("Generating comprehensive analysis report...")
        
        report = {
            'metadata': {
                'report_generated_at': datetime.now().isoformat(),
                'source_file': self.data_path,
                'total_records': len(self.df),
            },
            'descriptive_stats': {},
            'price_distribution_by_category': {},
            'rating_patterns': {},
            'correlation_analysis': {},
            'category_popularity': {},
            'comparative_analysis': {},
            'outlier_analysis': {},
            'hypothesis_testing': {}
        }

        # 1. Descriptive Statistics (Mean, Median, Mode, Std Dev)
        for col in ['price', 'rating']:
            if col in self.df.columns:
                series = self.df[col]
                stats = {
                    'mean': series.mean(),
                    'median': series.median(),
                    'mode': series.mode().iloc[0] if not series.mode().empty else 'N/A',
                    'std_dev': series.std(),
                    'min': series.min(),
                    'max': series.max()
                }
                report['descriptive_stats'][col] = {k: round(v, 2) if isinstance(v, (int, float)) else v for k, v in stats.items()}

        # 2. Price Distribution Analysis Across Categories
        if 'category' in self.df.columns and 'price' in self.df.columns:
            category_price_stats = {}
            for category, group in self.df.groupby('category'):
                price_series = group['price']
                category_price_stats[category] = {
                    'count': len(price_series),
                    'mean_price': round(price_series.mean(), 2),
                    'median_price': round(price_series.median(), 2),
                    'std_dev': round(price_series.std(), 2),
                    'min_price': round(price_series.min(), 2),
                    'max_price': round(price_series.max(), 2),
                    'price_range': round(price_series.max() - price_series.min(), 2)
                }
            report['price_distribution_by_category'] = category_price_stats

        # 3. Rating Patterns and Statistical Summaries
        if 'rating' in self.df.columns:
            rating_series = self.df['rating']
            rating_freq = rating_series.value_counts().sort_index()
            
            report['rating_patterns'] = {
                'rating_distribution': rating_freq.to_dict(),
                'most_common_rating': rating_freq.index[0],
                'rating_variability': round(rating_series.std(), 2),
                'rating_skewness': round(rating_series.skew(), 2),
                'rating_percentiles': {
                    '25th': round(rating_series.quantile(0.25), 2),
                    '50th': round(rating_series.quantile(0.50), 2),
                    '75th': round(rating_series.quantile(0.75), 2),
                    '90th': round(rating_series.quantile(0.90), 2)
                }
            }

        # 4. Correlation Analysis (Price, Rating, and Availability if available)
        numerical_cols = []
        if 'price' in self.df.columns:
            numerical_cols.append('price')
        if 'rating' in self.df.columns:
            numerical_cols.append('rating')
        if 'availability' in self.df.columns:
            # Convert availability to numeric if it's categorical
            if self.df['availability'].dtype == 'object':
                # Try to extract numeric values from availability strings
                self.df['availability_numeric'] = self.df['availability'].str.extract(r'(\d+)').astype(float)
                numerical_cols.append('availability_numeric')
            else:
                numerical_cols.append('availability')
        
        if len(numerical_cols) > 1:
            corr_matrix = self.df[numerical_cols].corr()
            correlations = {}
            for i in range(len(numerical_cols)):
                for j in range(i + 1, len(numerical_cols)):
                    col1, col2 = numerical_cols[i], numerical_cols[j]
                    corr_value = corr_matrix.loc[col1, col2]
                    correlations[f"{col1}_vs_{col2}"] = round(corr_value, 3) if pd.notna(corr_value) else 'N/A'
            
            report['correlation_analysis'] = {
                'correlation_matrix': corr_matrix.round(3).to_dict(),
                'significant_correlations': correlations
            }

        # 5. Category Popularity Analysis (Frequency Distributions)
        if 'category' in self.df.columns:
            category_freq = self.df['category'].value_counts()
            category_percent = (category_freq / len(self.df) * 100).round(2)
            
            report['category_popularity'] = {
                'frequency_distribution': category_freq.to_dict(),
                'percentage_distribution': category_percent.to_dict(),
                'total_categories': len(category_freq),
                'most_popular_category': category_freq.index[0],
                'least_popular_category': category_freq.index[-1],
                'category_concentration': {
                    'top_3_categories_percentage': category_percent.head(3).sum(),
                    'bottom_categories_count': len(category_freq[category_freq <= 1])
                }
            }

        # 6. Comparative Analysis Between Different Data Sources
        # Since we only have one data source, we'll compare different segments
        if 'category' in self.df.columns:
            # Compare fiction vs non-fiction
            fiction_mask = self.df['category'].str.contains('Fiction', case=False, na=False)
            fiction_data = self.df[fiction_mask]
            nonfiction_data = self.df[~fiction_mask]
            
            comparative_stats = {}
            
            if not fiction_data.empty and not nonfiction_data.empty:
                for col in ['price', 'rating']:
                    if col in fiction_data.columns and col in nonfiction_data.columns:
                        comparative_stats[f'{col}_comparison'] = {
                            'fiction': {
                                'count': len(fiction_data),
                                'mean': round(fiction_data[col].mean(), 2),
                                'std': round(fiction_data[col].std(), 2)
                            },
                            'non_fiction': {
                                'count': len(nonfiction_data),
                                'mean': round(nonfiction_data[col].mean(), 2),
                                'std': round(nonfiction_data[col].std(), 2)
                            },
                            'difference': round(fiction_data[col].mean() - nonfiction_data[col].mean(), 2)
                        }
            
            # Compare by price ranges
            if 'price' in self.df.columns:
                price_quartiles = self.df['price'].quantile([0.25, 0.5, 0.75])
                cheap_books = self.df[self.df['price'] <= price_quartiles[0.25]]
                expensive_books = self.df[self.df['price'] >= price_quartiles[0.75]]
                
                comparative_stats['price_range_comparison'] = {
                    'cheap_books': {
                        'count': len(cheap_books),
                        'avg_rating': round(cheap_books['rating'].mean(), 2) if 'rating' in cheap_books.columns else 'N/A',
                        'price_threshold': round(price_quartiles[0.25], 2)
                    },
                    'expensive_books': {
                        'count': len(expensive_books),
                        'avg_rating': round(expensive_books['rating'].mean(), 2) if 'rating' in expensive_books.columns else 'N/A',
                        'price_threshold': round(price_quartiles[0.75], 2)
                    }
                }
            
            report['comparative_analysis'] = comparative_stats

        # 7. Outlier Detection (using IQR method)
        for col in ['price', 'rating']:
            if col in self.df.columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                report['outlier_analysis'][col] = {
                    'count': len(outliers),
                    'percentage': round((len(outliers) / len(self.df)) * 100, 2),
                    'values': outliers[col].head(5).tolist() # Show up to 5 sample outliers
                }

        # 8. Hypothesis Testing (Fiction vs. Non-Fiction prices)
        if 'category' in self.df.columns:
            fiction_prices = self.df[self.df['category'].str.contains('Fiction', case=False, na=False)]['price']
            non_fiction_prices = self.df[~self.df['category'].str.contains('Fiction', case=False, na=False)]['price']
            
            if not fiction_prices.empty and not non_fiction_prices.empty:
                stat, p_value = ttest_ind(fiction_prices, non_fiction_prices, equal_var=False, nan_policy='omit')
                report['hypothesis_testing']['fiction_vs_nonfiction_price'] = {
                    't_statistic': round(stat, 3),
                    'p_value': round(p_value, 3),
                    'is_significant_at_0.05': p_value < 0.05,
                    'fiction_mean_price': round(fiction_prices.mean(), 2),
                    'non_fiction_mean_price': round(non_fiction_prices.mean(), 2)
                }

        logger.info("Comprehensive report generated successfully.")
        return report

    def save_report(self, report: Dict[str, Any], output_path: str, format: str = 'json') -> str:
        """
        Saves the analysis report to a file (JSON or Markdown).
        """
        output_path = Path(output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == 'json':
            # Custom JSON encoder to handle NumPy data types
            class NpEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, np.integer):
                        return int(obj)
                    if isinstance(obj, np.floating):
                        return float(obj)
                    if isinstance(obj, np.ndarray):
                        return obj.tolist()
                    if isinstance(obj, np.bool_):
                        return bool(obj)
                    return super(NpEncoder, self).default(obj)
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=4, cls=NpEncoder)
        elif format == 'markdown':
            with open(output_path, 'w') as f:
                f.write(self._format_report_to_markdown(report))
        else:
            raise ValueError("Unsupported format. Choose 'json' or 'markdown'.")
            
        logger.info(f"{format.upper()} report saved to: {output_path}")
        return str(output_path)

    def _format_report_to_markdown(self, report: Dict[str, Any]) -> str:
        """Converts the report dictionary to a Markdown string."""
        lines = [f"# Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]

        # Metadata
        meta = report.get('metadata', {})
        lines.append("## 1. Overview\n")
        lines.append(f"- **Source File**: `{meta.get('source_file', 'N/A')}`")
        lines.append(f"- **Total Records**: {meta.get('total_records', 'N/A')}\n")

        # Descriptive Stats
        stats = report.get('descriptive_stats', {})
        if stats:
            lines.append("## 2. Descriptive Statistics\n")
            for col, data in stats.items():
                lines.append(f"### {col.title()} Statistics\n")
                lines.append("| Metric | Value |")
                lines.append("|--------|-------|")
                for metric, value in data.items():
                    lines.append(f"| {metric.replace('_', ' ').title()} | {value} |")
                lines.append("")

        # Outlier Analysis
        outliers = report.get('outlier_analysis', {})
        if outliers:
            lines.append("## 3. Outlier Analysis (IQR Method)\n")
            for col, data in outliers.items():
                lines.append(f"- **{col.title()} Outliers**: {data.get('count')} ({data.get('percentage')}%)")
            lines.append("")

        # Category Analysis
        cat_analysis = report.get('category_analysis', {})
        if cat_analysis:
            lines.append("## 4. Category Frequency Distribution\n")
            lines.append(f"- **Total Unique Categories**: {cat_analysis.get('total_categories', 'N/A')}")
            lines.append(f"- **Most Popular**: {cat_analysis.get('most_popular_category', 'N/A')}\n")
            lines.append("### Top 5 Categories\n")
            lines.append("| Category | Count |")
            lines.append("|----------|-------|")
            for cat, count in cat_analysis.get('top_5_categories', {}).items():
                lines.append(f"| {cat} | {count} |")
            lines.append("")

        # Correlation Analysis
        corr = report.get('correlation_analysis', {})
        if corr:
            lines.append("## 5. Correlation Analysis\n")
            lines.append(f"- **Price vs. Rating Correlation**: {corr.get('price_vs_rating_correlation', 'N/A')}\n")

        # Hypothesis Testing
        hypo = report.get('hypothesis_testing', {})
        if hypo.get('fiction_vs_nonfiction_price'):
            test_results = hypo['fiction_vs_nonfiction_price']
            lines.append("## 6. Hypothesis Testing: Fiction vs. Non-Fiction Prices\n")
            lines.append(f"- **T-statistic**: {test_results['t_statistic']}")
            lines.append(f"- **P-value**: {test_results['p_value']}")
            lines.append(f"- **Result**: {'Significant difference' if test_results['is_significant_at_0.05'] else 'No significant difference'} found at the 0.05 level.")
            lines.append(f"- **Mean Price (Fiction)**: £{test_results['fiction_mean_price']}")
            lines.append(f"- **Mean Price (Non-Fiction)**: £{test_results['non_fiction_mean_price']}\n")

        return "\n".join(lines)


def main():
    """
    Main function to demonstrate the BookDataAnalyzer.
    """
    print("--- Book Data Analyzer Demonstration ---")
    
    script_dir = Path(__file__).parent
    data_file = script_dir.parent / 'data' / 'cleaned_books.csv'
    output_dir = script_dir.parent / 'data'
    
    if not data_file.exists():
        print(f"Error: Cleaned data file not found at {data_file}")
        return

    try:
        print(f"Loading data from: {data_file}")
        analyzer = BookDataAnalyzer(str(data_file))

        print("Generating comprehensive analysis report...")
        report_data = analyzer.generate_comprehensive_report()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = output_dir / f"simplified_report_{timestamp}.json"
        md_path = output_dir / f"simplified_report_{timestamp}.md"

        analyzer.save_report(report_data, str(json_path), 'json')
        analyzer.save_report(report_data, str(md_path), 'markdown')

        print("\n--- Analysis Complete ---")
        print(f"Reports saved in: {output_dir.resolve()}")
        
        print("\n--- Report Summary ---")
        
        # Custom JSON encoder for printing
        class NpEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                if isinstance(obj, np.floating):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                if isinstance(obj, np.bool_):
                    return bool(obj)
                return super(NpEncoder, self).default(obj)
        
        print(json.dumps(report_data, indent=2, cls=NpEncoder))

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        logger.error(f"Analyzer demonstration failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()
