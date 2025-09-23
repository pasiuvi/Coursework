"""
Social Media Analysis Pipeline

This script orchestrates the complete data analysis pipeline:
1. Web scraping (scraper.py)
2. Data cleaning (cleaner.py)
3. Statistical analysis (analyzer.py)
4. Data visualization (visualizer.py)

Author: GitHub Copilot
Date: September 2025
"""

import os
import sys
import time
import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from colorama import init, Fore, Back, Style

# Add subdirectories to path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir / 'data_collection'))
sys.path.append(str(current_dir / 'data_processing'))
sys.path.append(str(current_dir / 'analysis'))
sys.path.append(str(current_dir / 'visualizations'))

# Import pipeline components
from scraper import BookScraper
from cleaner import DataCleaner
from analyzer import BookDataAnalyzer
from visualizer import BookDataVisualizer


class AnalysisPipeline:
    """
    Complete analysis pipeline that orchestrates data collection, cleaning, analysis, and visualization.
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize the analysis pipeline.
        
        Args:
            base_dir: Base directory for the pipeline (defaults to current directory)
        """
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.data_dir = self.base_dir / 'data'
        self.data_dir.mkdir(exist_ok=True)
        
        # File paths
        self.scraped_file = self.data_dir / 'scraped_books.csv'
        self.cleaned_file = self.data_dir / 'cleaned_books.csv'
        self.analysis_report = self.data_dir / f'comprehensive_analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        self.visualization_dir = self.base_dir / 'visualizations' / 'output_visualizations'
        
        # Setup logging
        self._setup_logging()
        
        # Pipeline statistics
        self.pipeline_stats = {
            'start_time': None,
            'end_time': None,
            'duration': None,
            'steps_completed': [],
            'errors': []
        }
    
    def _setup_logging(self) -> None:
        """Set up logging for the pipeline."""
        # Initialize colorama
        init(autoreset=True)
        
        log_file = self.base_dir / 'pipeline.log'
        
        # Custom formatter with colors
        class ColoredFormatter(logging.Formatter):
            def format(self, record):
                if record.levelno == logging.INFO:
                    record.msg = Fore.GREEN + record.msg + Style.RESET_ALL
                elif record.levelno == logging.WARNING:
                    record.msg = Fore.YELLOW + record.msg + Style.RESET_ALL
                elif record.levelno == logging.ERROR:
                    record.msg = Fore.RED + record.msg + Style.RESET_ALL
                elif record.levelno == logging.DEBUG:
                    record.msg = Fore.BLUE + record.msg + Style.RESET_ALL
                return super().format(record)
        
        # Create logger
        self.logger = logging.getLogger('AnalysisPipeline')
        self.logger.setLevel(logging.INFO)
        
        # Remove any existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # File handler (no colors)
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        # Console handler (with colors)
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _clear_data_folders(self) -> None:
        """Clear all data in data folder and output_visualizations folder."""
        # Clear data folder
        if self.data_dir.exists():
            shutil.rmtree(self.data_dir)
            self.data_dir.mkdir()
            self.logger.info(f"Cleared data folder: {self.data_dir}")
        
        # Clear output visualizations folder
        if self.visualization_dir.exists():
            shutil.rmtree(self.visualization_dir)
            self.visualization_dir.mkdir(parents=True)
            self.logger.info(f"Cleared visualizations folder: {self.visualization_dir}")
    
    def run_scraper(self, num_pages: int = 1) -> bool:
        """
        Step 1: Run the web scraper to collect book data.
        
        Args:
            num_pages: Number of pages to scrape
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("\n" + "=" * 60)
            self.logger.info("STEP 1: RUNNING WEB SCRAPER")
            self.logger.info("=" * 60 + "\n")
            
            # Initialize scraper with relative path from scraper's perspective
            scraper = BookScraper(output_file=str(self.scraped_file), max_pages=num_pages, logger=self.logger)
            
            # Run scraping
            scraper.scrape_books()
            
            # Check if scraping was successful by checking if file exists and has content
            if self.scraped_file.exists():
                import pandas as pd
                try:
                    df = pd.read_csv(self.scraped_file)
                    books_count = len(df)
                    if books_count > 0:
                        self.logger.info(f"Successfully scraped {books_count} books")
                        self.logger.info(f"Data saved to: {self.scraped_file}\n")
                        self.pipeline_stats['steps_completed'].append('scraping')
                        return True
                    else:
                        self.logger.error("Scraped file is empty\n")
                        return False
                except Exception as e:
                    self.logger.error(f"Error reading scraped file: {e}\n")
                    return False
            else:
                self.logger.error("Scraped file was not created\n")
                return False
                
        except Exception as e:
            error_msg = f"Error in scraping step: {str(e)}"
            self.logger.error(error_msg + "\n")
            self.pipeline_stats['errors'].append(error_msg)
            return False
    
    def run_cleaner(self) -> bool:
        """
        Step 2: Clean the scraped data.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("\n" + "=" * 60)
            self.logger.info("STEP 2: RUNNING DATA CLEANER")
            self.logger.info("=" * 60 + "\n")
            
            # Check if scraped data exists
            if not self.scraped_file.exists():
                raise FileNotFoundError(f"Scraped data file not found: {self.scraped_file}")
            
            # Initialize cleaner
            cleaner = DataCleaner(
                numerical_fill_value=0.0,
                categorical_fill_value='Unknown',
                required_columns=['title', 'price']
            )
            
            # Process data
            cleaned_df = cleaner.process_pipeline(
                input_path=str(self.scraped_file),
                output_path=str(self.cleaned_file),
                text_columns=['title', 'category'],
                datetime_columns=[]
            )
            
            # Log statistics
            stats = cleaner.processing_stats
            self.logger.info(f"Cleaning completed. Final dataset: {len(cleaned_df)} rows")
            self.logger.info(f"Processing statistics: {stats}\n")
            
            self.pipeline_stats['steps_completed'].append('cleaning')
            return True
            
        except Exception as e:
            error_msg = f"Error in cleaning step: {str(e)}"
            self.logger.error(error_msg + "\n")
            self.pipeline_stats['errors'].append(error_msg)
            return False
    
    def run_analyzer(self) -> bool:
        """
        Step 3: Run statistical analysis on cleaned data.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("\n" + "=" * 60)
            self.logger.info("STEP 3: RUNNING STATISTICAL ANALYSIS")
            self.logger.info("=" * 60 + "\n")
            
            # Check if cleaned data exists
            if not self.cleaned_file.exists():
                raise FileNotFoundError(f"Cleaned data file not found: {self.cleaned_file}")
            
            # Initialize analyzer
            analyzer = BookDataAnalyzer(str(self.cleaned_file))
            
            # Generate comprehensive analysis
            analysis_results = analyzer.generate_comprehensive_report()
            
            # Save analysis results
            json_path = analyzer.save_report(
                analysis_results, 
                str(self.analysis_report),
                format='json'
            )
            
            # Also save as markdown
            md_report = self.analysis_report.with_suffix('.md')
            analyzer.save_report(
                analysis_results, 
                str(md_report),
                format='markdown'
            )
            
            self.logger.info(f"Analysis completed and saved to:")
            self.logger.info(f"  - JSON: {json_path}")
            self.logger.info(f"  - Markdown: {md_report}\n")
            
            self.pipeline_stats['steps_completed'].append('analysis')
            return True
            
        except Exception as e:
            error_msg = f"Error in analysis step: {str(e)}"
            self.logger.error(error_msg + "\n")
            self.pipeline_stats['errors'].append(error_msg)
            return False
    
    def run_visualizer(self) -> bool:
        """
        Step 4: Generate data visualizations.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("\n" + "=" * 60)
            self.logger.info("STEP 4: GENERATING VISUALIZATIONS")
            self.logger.info("=" * 60 + "\n")
            
            # Check if cleaned data exists
            if not self.cleaned_file.exists():
                raise FileNotFoundError(f"Cleaned data file not found: {self.cleaned_file}")
            
            # Initialize visualizer
            visualizer = BookDataVisualizer(
                data_path=str(self.cleaned_file),
                output_dir=str(self.visualization_dir)
            )
            
            # Generate all visualizations
            self.logger.info("Generating price distribution plots...")
            visualizer.create_price_distribution_plots()
            
            self.logger.info("Generating rating analysis plots...")
            visualizer.create_rating_analysis_plots()
            
            self.logger.info("Generating category analysis plots...")
            visualizer.create_category_analysis_plots()
            
            self.logger.info("Generating correlation analysis...")
            visualizer.create_advanced_correlation_plots()
            
            self.logger.info("Generating comprehensive dashboard...")
            visualizer.create_interactive_plotly_dashboard()
            
            self.logger.info(f"All visualizations saved to: {self.visualization_dir}\n")
            
            self.pipeline_stats['steps_completed'].append('visualization')
            return True
            
        except Exception as e:
            error_msg = f"Error in visualization step: {str(e)}"
            self.logger.error(error_msg + "\n")
            self.pipeline_stats['errors'].append(error_msg)
            return False
    
    def run_full_pipeline(self, num_pages: int = 1, skip_scraping: bool = False) -> Dict[str, Any]:
        """
        Run the complete analysis pipeline.
        
        Args:
            num_pages: Number of pages to scrape
            skip_scraping: If True, skip scraping and use existing data
            
        Returns:
            Dictionary with pipeline results and statistics
        """
        self.pipeline_stats['start_time'] = datetime.now()
        
        # Clear existing data and visualizations
        self.logger.info("Clearing existing data and visualizations...")
        self._clear_data_folders()
        
        self.logger.info("*" * 80)
        self.logger.info("STARTING SOCIAL MEDIA ANALYSIS PIPELINE")
        self.logger.info("*" * 80)
        
        success = True
        
        # Step 1: Scraping (optional)
        if not skip_scraping:
            if not self.run_scraper(num_pages):
                success = False
        else:
            self.logger.info("Skipping scraping step - using existing data")
            if self.scraped_file.exists():
                self.pipeline_stats['steps_completed'].append('scraping (skipped)')
            else:
                self.logger.error("Cannot skip scraping - no existing data found")
                success = False
        
        # Step 2: Cleaning
        if success and not self.run_cleaner():
            success = False
        
        # Step 3: Analysis
        if success and not self.run_analyzer():
            success = False
        
        # Step 4: Visualization
        if success and not self.run_visualizer():
            success = False
        
        # Finalize pipeline
        self.pipeline_stats['end_time'] = datetime.now()
        self.pipeline_stats['duration'] = (
            self.pipeline_stats['end_time'] - self.pipeline_stats['start_time']
        ).total_seconds()
        
        # Log final results
        self.logger.info("*" * 80)
        if success:
            self.logger.info("PIPELINE COMPLETED SUCCESSFULLY!")
        else:
            self.logger.error("PIPELINE COMPLETED WITH ERRORS!")
        
        self.logger.info(f"Duration: {self.pipeline_stats['duration']:.2f} seconds")
        self.logger.info(f"Steps completed: {', '.join(self.pipeline_stats['steps_completed'])}")
        
        if self.pipeline_stats['errors']:
            self.logger.error(f"Errors encountered: {len(self.pipeline_stats['errors'])}")
            for error in self.pipeline_stats['errors']:
                self.logger.error(f"  - {error}")
        
        self.logger.info("*" * 80)
        
        return {
            'success': success,
            'statistics': self.pipeline_stats,
            'output_files': {
                'scraped_data': str(self.scraped_file),
                'cleaned_data': str(self.cleaned_file),
                'analysis_report_json': str(self.analysis_report),
                'analysis_report_md': str(self.analysis_report.with_suffix('.md')),
                'visualizations': str(self.visualization_dir)
            }
        }


def main():
    """Main function to run the pipeline with command line options."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Social Media Analysis Pipeline')
    parser.add_argument('--pages', type=int, default=1, help='Number of pages to scrape (default: 5)')
    parser.add_argument('--skip-scraping', action='store_true', help='Skip scraping and use existing data')
    parser.add_argument('--step', choices=['scraper', 'cleaner', 'analyzer', 'visualizer'], 
                       help='Run only a specific step')
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = AnalysisPipeline()
    
    if args.step:
        # Run specific step
        if args.step == 'scraper':
            result = pipeline.run_scraper(args.pages)
        elif args.step == 'cleaner':
            result = pipeline.run_cleaner()
        elif args.step == 'analyzer':
            result = pipeline.run_analyzer()
        elif args.step == 'visualizer':
            result = pipeline.run_visualizer()
        
        if result:
            print(f"Step '{args.step}' completed successfully!")
        else:
            print(f"Step '{args.step}' failed!")
            sys.exit(1)
    else:
        # Run full pipeline
        results = pipeline.run_full_pipeline(
            num_pages=args.pages, 
            skip_scraping=args.skip_scraping
        )
        
        if not results['success']:
            sys.exit(1)


if __name__ == "__main__":
    main()
