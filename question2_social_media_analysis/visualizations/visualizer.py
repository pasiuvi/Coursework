"""
Book Data Visualizer Module

Simplified visualizer that creates essential plots for book data analysis.

Author: GitHub Copilot
Date: September 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path
from typing import Dict, Any
import logging

# Configure plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BookDataVisualizer:
    """
    Simplified visualizer for book data with essential plots.
    """

    def __init__(self, data_path: str, output_dir: str = "output_visualizations") -> None:
        """
        Initialize the visualizer.

        Args:
            data_path: Path to the cleaned books CSV file
            output_dir: Directory to save visualizations
        """
        self.data_path = Path(data_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.data = None
        self._load_data()

    def _load_data(self) -> None:
        """Load and prepare data."""
        try:
            self.data = pd.read_csv(self.data_path)
            self.data['price'] = pd.to_numeric(self.data['price'], errors='coerce')
            self.data['rating'] = pd.to_numeric(self.data['rating'], errors='coerce')
            self.data['category'] = self.data['category'].fillna('Unknown')

            logger.info(f"Loaded {len(self.data)} records")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def create_price_distribution_plots(self) -> Dict[str, Any]:
        """
        Create price distribution visualizations.

        Returns:
            Dict containing plot statistics
        """
        logger.info("Creating price distribution plots...")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('Price Distribution Analysis')

        # Price histogram
        ax1.hist(self.data['price'].dropna(), bins=20, alpha=0.7, edgecolor='black')
        ax1.set_title('Price Distribution')
        ax1.set_xlabel('Price ($)')
        ax1.set_ylabel('Frequency')
        ax1.axvline(self.data['price'].mean(), color='red', linestyle='--',
                   label=f'Mean: ${self.data["price"].mean():.2f}')
        ax1.legend()

        # Price by category (top 5)
        top_categories = self.data['category'].value_counts().head(5).index
        filtered_data = self.data[self.data['category'].isin(top_categories)]
        sns.boxplot(data=filtered_data, x='category', y='price', ax=ax2)
        ax2.set_title('Price by Category (Top 5)')
        ax2.set_xlabel('Category')
        ax2.set_ylabel('Price ($)')
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plot_path = self.output_dir / 'price_distribution_analysis.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Price distribution analysis saved to: {plot_path}")

        return {
            'mean_price': self.data['price'].mean(),
            'median_price': self.data['price'].median()
        }

    def create_rating_analysis_plots(self) -> Dict[str, Any]:
        """
        Create rating analysis visualizations.

        Returns:
            Dict containing plot statistics
        """
        logger.info("Creating rating analysis plots...")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('Rating Analysis')

        # Rating distribution
        ax1.hist(self.data['rating'].dropna(), bins=5, range=(1, 5), alpha=0.7, edgecolor='black')
        ax1.set_title('Rating Distribution')
        ax1.set_xlabel('Rating')
        ax1.set_ylabel('Frequency')
        ax1.set_xticks(range(1, 6))

        # Rating vs price scatter
        valid_data = self.data.dropna(subset=['rating', 'price'])
        ax2.scatter(valid_data['rating'], valid_data['price'], alpha=0.6)
        ax2.set_title('Rating vs Price')
        ax2.set_xlabel('Rating')
        ax2.set_ylabel('Price ($)')

        # Add trend line
        slope, intercept = np.polyfit(valid_data['rating'], valid_data['price'], 1)
        x_trend = np.linspace(valid_data['rating'].min(), valid_data['rating'].max(), 100)
        y_trend = slope * x_trend + intercept
        ax2.plot(x_trend, y_trend, color='red', linewidth=2, label='Trend Line')
        ax2.legend()

        # Add correlation
        correlation = valid_data['rating'].corr(valid_data['price'])
        ax2.text(0.05, 0.95, f'Correlation: {correlation:.3f}',
                transform=ax2.transAxes, fontsize=10,
                bbox=dict(boxstyle="round", facecolor='white', alpha=0.8))

        plt.tight_layout()
        plot_path = self.output_dir / 'rating_analysis.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Rating analysis saved to: {plot_path}")

        return {
            'mean_rating': self.data['rating'].mean(),
            'correlation_rating_price': correlation
        }

    def create_category_analysis_plots(self) -> Dict[str, Any]:
        """
        Create category analysis visualizations.

        Returns:
            Dict containing plot statistics
        """
        logger.info("Creating category analysis plots...")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('Category Analysis')

        # Category popularity (top 10)
        category_counts = self.data['category'].value_counts().head(10)
        ax1.bar(range(len(category_counts)), category_counts.values, alpha=0.7)
        ax1.set_title('Category Popularity (Top 10)')
        ax1.set_xlabel('Category')
        ax1.set_ylabel('Number of Books')
        ax1.set_xticks(range(len(category_counts)))
        ax1.set_xticklabels(category_counts.index, rotation=45, ha='right')

        # Average price by category (top 10)
        top_categories = category_counts.index
        category_prices = self.data[self.data['category'].isin(top_categories)].groupby('category')['price'].mean()
        ax2.bar(range(len(category_prices)), category_prices.values, alpha=0.7, color='orange')
        ax2.set_title('Average Price by Category')
        ax2.set_xlabel('Category')
        ax2.set_ylabel('Average Price ($)')
        ax2.set_xticks(range(len(category_prices)))
        ax2.set_xticklabels(category_prices.index, rotation=45, ha='right')

        plt.tight_layout()
        plot_path = self.output_dir / 'category_analysis.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Category analysis saved to: {plot_path}")

        return {
            'total_categories': len(self.data['category'].unique()),
            'most_popular_category': category_counts.index[0],
            'category_counts': category_counts.to_dict()
        }

    def create_interactive_plotly_dashboard(self) -> str:
        """
        Create comprehensive interactive dashboard with all plots.

        Returns:
            str: Path to the saved HTML file
        """
        logger.info("Creating comprehensive interactive dashboard...")

        # Create subplots with 4x2 grid
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go

        fig = make_subplots(
            rows=4, cols=2,
            subplot_titles=[
                'Price Distribution', 'Rating Distribution',
                'Price vs Rating Scatter', 'Category Popularity',
                'Price by Category Box Plot', 'Average Rating by Category',
                'Correlation Matrix', 'Fiction vs Non-Fiction Comparison'
            ],
            specs=[
                [{"type": "histogram"}, {"type": "histogram"}],
                [{"type": "scatter"}, {"type": "bar"}],
                [{"type": "box"}, {"type": "bar"}],
                [{"type": "heatmap"}, {"type": "box"}]
            ]
        )

        # 1. Price Distribution Histogram
        fig.add_trace(
            go.Histogram(
                x=self.data['price'].dropna(),
                nbinsx=20,
                name='Price Distribution',
                marker_color='lightblue',
                showlegend=False
            ),
            row=1, col=1
        )

        # 2. Rating Distribution Histogram
        fig.add_trace(
            go.Histogram(
                x=self.data['rating'].dropna(),
                nbinsx=5,
                name='Rating Distribution',
                marker_color='lightcoral',
                showlegend=False
            ),
            row=1, col=2
        )

        # 3. Price vs Rating Scatter Plot
        valid_data = self.data.dropna(subset=['price', 'rating'])
        fig.add_trace(
            go.Scatter(
                x=valid_data['rating'],
                y=valid_data['price'],
                mode='markers',
                name='Price vs Rating',
                text=valid_data['category'],
                marker=dict(
                    color=valid_data['price'],
                    colorscale='Viridis',
                    size=8,
                    showscale=True,
                    colorbar=dict(title="Price ($)", x=0.45, y=0.5, len=0.4)
                ),
                hovertemplate='<b>%{text}</b><br>Rating: %{x}<br>Price: $%{y:.2f}<extra></extra>',
                showlegend=False
            ),
            row=2, col=1
        )

        # Add trend line to scatter
        slope, intercept = np.polyfit(valid_data['rating'], valid_data['price'], 1)
        x_trend = np.linspace(valid_data['rating'].min(), valid_data['rating'].max(), 100)
        y_trend = slope * x_trend + intercept
        fig.add_trace(
            go.Scatter(
                x=x_trend,
                y=y_trend,
                mode='lines',
                name='Trend Line',
                line=dict(color='red', width=2),
                showlegend=False
            ),
            row=2, col=1
        )

        # 4. Category Popularity Bar Chart
        category_counts = self.data['category'].value_counts().head(10)
        fig.add_trace(
            go.Bar(
                x=category_counts.index,
                y=category_counts.values,
                name='Category Popularity',
                marker_color='lightgreen',
                showlegend=False
            ),
            row=2, col=2
        )

        # 5. Price by Category Box Plot
        top_categories = self.data['category'].value_counts().head(5).index
        box_data = self.data[self.data['category'].isin(top_categories)]
        for cat in top_categories:
            cat_data = box_data[box_data['category'] == cat]['price'].dropna()
            fig.add_trace(
                go.Box(
                    y=cat_data,
                    name=cat,
                    showlegend=False
                ),
                row=3, col=1
            )

        # 6. Average Rating by Category Bar Chart
        category_avg_rating = self.data.groupby('category')['rating'].mean().sort_values(ascending=False).head(10)
        fig.add_trace(
            go.Bar(
                x=category_avg_rating.index,
                y=category_avg_rating.values,
                name='Average Rating',
                marker_color='orange',
                showlegend=False
            ),
            row=3, col=2
        )

        # 7. Correlation Matrix Heatmap
        numerical_cols = ['price', 'rating']
        if 'availability' in self.data.columns:
            numerical_cols.append('availability')

        corr_matrix = self.data[numerical_cols].corr().round(3)
        fig.add_trace(
            go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values,
                texttemplate='%{text:.3f}',
                textfont={"size": 10},
                hoverongaps=False,
                showlegend=False
            ),
            row=4, col=1
        )

        # 8. Fiction vs Non-Fiction Box Plot
        fiction_categories = ['fiction', 'historical fiction', 'mystery', 'young adult']
        self.data['book_type'] = self.data['category'].apply(
            lambda x: 'Fiction' if str(x).lower() in fiction_categories else 'Non-Fiction'
        )

        fiction_ratings = self.data[self.data['book_type'] == 'Fiction']['rating'].dropna()
        nonfiction_ratings = self.data[self.data['book_type'] == 'Non-Fiction']['rating'].dropna()

        fig.add_trace(
            go.Box(
                y=fiction_ratings,
                name='Fiction',
                marker_color='skyblue',
                showlegend=False
            ),
            row=4, col=2
        )

        fig.add_trace(
            go.Box(
                y=nonfiction_ratings,
                name='Non-Fiction',
                marker_color='salmon',
                showlegend=False
            ),
            row=4, col=2
        )

        # Update layout
        fig.update_layout(
            height=1600,
            width=1000,
            title_text="Comprehensive Book Data Analysis Dashboard",
            title_x=0.5,
            showlegend=False
        )

        # Update axis labels
        fig.update_xaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Frequency", row=1, col=1)

        fig.update_xaxes(title_text="Rating", row=1, col=2)
        fig.update_yaxes(title_text="Frequency", row=1, col=2)

        fig.update_xaxes(title_text="Rating", row=2, col=1)
        fig.update_yaxes(title_text="Price ($)", row=2, col=1)

        fig.update_xaxes(title_text="Category", row=2, col=2)
        fig.update_yaxes(title_text="Number of Books", row=2, col=2)

        fig.update_xaxes(title_text="Category", row=3, col=1)
        fig.update_yaxes(title_text="Price ($)", row=3, col=1)

        fig.update_xaxes(title_text="Category", row=3, col=2)
        fig.update_yaxes(title_text="Average Rating", row=3, col=2)

        fig.update_xaxes(title_text="Variables", row=4, col=1)
        fig.update_yaxes(title_text="Variables", row=4, col=1)

        fig.update_xaxes(title_text="Book Type", row=4, col=2)
        fig.update_yaxes(title_text="Rating", row=4, col=2)

        # Save as HTML
        dashboard_path = self.output_dir / 'comprehensive_interactive_dashboard.html'
        fig.write_html(str(dashboard_path))

        logger.info(f"Comprehensive interactive dashboard saved to: {dashboard_path}")
        return str(dashboard_path)

    def create_advanced_correlation_plots(self) -> Dict[str, Any]:
        """
        Create correlation analysis plots.

        Returns:
            Dict containing correlation statistics
        """
        logger.info("Creating correlation plots...")

        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        fig.suptitle('Correlation Analysis')

        # Correlation heatmap
        numerical_cols = ['price', 'rating']
        if 'availability' in self.data.columns:
            numerical_cols.append('availability')

        correlation_data = self.data[numerical_cols].corr()
        sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0, ax=ax)
        ax.set_title('Correlation Matrix')

        plt.tight_layout()
        plot_path = self.output_dir / 'correlation_analysis.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Correlation analysis saved to: {plot_path}")

        return {
            'correlation_matrix': correlation_data.to_dict(),
            'price_rating_correlation': self.data['price'].corr(self.data['rating'])
        }

    def create_comparative_analysis_plots(self) -> Dict[str, Any]:
        """
        Create comparative analysis plots.

        Returns:
            Dict containing comparative statistics
        """
        logger.info("Creating comparative analysis plots...")

        # Define fiction vs non-fiction
        fiction_categories = ['fiction', 'historical fiction', 'mystery', 'young adult']
        self.data['book_type'] = self.data['category'].apply(
            lambda x: 'Fiction' if str(x).lower() in fiction_categories else 'Non-Fiction'
        )

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('Fiction vs Non-Fiction Comparison')

        # Price comparison
        fiction_prices = self.data[self.data['book_type'] == 'Fiction']['price'].dropna()
        nonfiction_prices = self.data[self.data['book_type'] == 'Non-Fiction']['price'].dropna()

        ax1.hist(fiction_prices, bins=10, alpha=0.7, label='Fiction', color='skyblue')
        ax1.hist(nonfiction_prices, bins=10, alpha=0.7, label='Non-Fiction', color='salmon')
        ax1.set_xlabel('Price ($)')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Price Distribution')
        ax1.legend()

        # Rating comparison
        fiction_ratings = self.data[self.data['book_type'] == 'Fiction']['rating'].dropna()
        nonfiction_ratings = self.data[self.data['book_type'] == 'Non-Fiction']['rating'].dropna()

        ax2.boxplot([fiction_ratings, nonfiction_ratings], labels=['Fiction', 'Non-Fiction'])
        ax2.set_ylabel('Rating')
        ax2.set_title('Rating Distribution')

        plt.tight_layout()
        plot_path = self.output_dir / 'comparative_analysis.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Comparative analysis saved to: {plot_path}")

        return {
            'fiction_count': len(fiction_prices),
            'nonfiction_count': len(nonfiction_prices),
            'fiction_avg_price': fiction_prices.mean(),
            'nonfiction_avg_price': nonfiction_prices.mean()
        }

    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive visualization report.

        Returns:
            Dict containing all visualization results and statistics
        """
        logger.info("Generating comprehensive visualization report...")

        try:
            report = {
                'dataset_summary': {
                    'total_books': len(self.data),
                    'unique_categories': len(self.data['category'].unique()),
                    'price_range': [self.data['price'].min(), self.data['price'].max()],
                    'rating_range': [self.data['rating'].min(), self.data['rating'].max()]
                }
            }

            # Generate all visualizations
            report['price_analysis'] = self.create_price_distribution_plots()
            report['rating_analysis'] = self.create_rating_analysis_plots()
            report['category_analysis'] = self.create_category_analysis_plots()
            report['correlation_analysis'] = self.create_advanced_correlation_plots()
            report['comparative_analysis'] = self.create_comparative_analysis_plots()

            # Create interactive dashboard
            dashboard_path = self.create_interactive_plotly_dashboard()
            report['interactive_dashboard'] = dashboard_path

            logger.info(f"Comprehensive report generated successfully")
            logger.info(f"All visualizations saved in: {self.output_dir}")

            return report

        except Exception as e:
            logger.error(f"Error generating comprehensive report: {e}")
            raise


def main() -> None:
    """Main function to demonstrate the visualizer capabilities."""
    try:
        # Initialize visualizer
        data_path = "../data/cleaned_books.csv"
        visualizer = BookDataVisualizer(data_path)

        # Generate comprehensive visualization report
        report = visualizer.generate_comprehensive_report()

        print("=== BOOK DATA VISUALIZATION REPORT ===\n")
        print(f"Dataset: {report['dataset_summary']['total_books']} books analyzed")
        print(f"Categories: {report['dataset_summary']['unique_categories']} unique categories")
        print(f"Price range: ${report['dataset_summary']['price_range'][0]:.2f} - ${report['dataset_summary']['price_range'][1]:.2f}")
        print(f"Rating range: {report['dataset_summary']['rating_range'][0]} - {report['dataset_summary']['rating_range'][1]}")

        print("\n=== KEY FINDINGS ===")
        print(f"Average price: ${report['price_analysis']['mean_price']:.2f}")
        print(f"Average rating: {report['rating_analysis']['mean_rating']:.2f}")
        print(f"Most popular category: {report['category_analysis']['most_popular_category']}")

        print(f"\n=== CORRELATIONS ===")
        print(f"Price-Rating correlation: {report['correlation_analysis']['price_rating_correlation']:.3f}")

        print(f"\n=== COMPARATIVE ANALYSIS ===")
        comp = report['comparative_analysis']
        print(f"Fiction books: {comp['fiction_count']}")
        print(f"Non-fiction books: {comp['nonfiction_count']}")

        print(f"\n=== OUTPUT FILES ===")
        print(f"Interactive dashboard: {report['interactive_dashboard']}")
        print(f"All visualizations saved in: output_visualizations/")

    except Exception as e:
        logger.error(f"Visualization failed: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
