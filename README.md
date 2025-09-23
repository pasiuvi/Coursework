# Coursework
University Management and Data Analysis Coursework

## Overview

This repository contains three distinct projects, each with different objectives and requirements:

1. **Question 1**: University Management System (Object-Oriented Programming)
2. **Question 2**: Social Media Analysis Pipeline (Data Science & Web Scraping)
3. **Question 3**: Healthcare Ethics Report (Academic Research)

Each project has its own setup requirements and usage instructions detailed below.

---

## Project 1: University Management System

### Description
An object-oriented Python application that demonstrates inheritance, encapsulation, and polymorphism through a university management system with students, faculty, departments, and courses.

### Features
- Person base class with Student and Faculty inheritance
- Department and Course management
- Student enrollment and GPA calculation
- Academic status tracking
- Faculty-course assignment system

### Setup & Installation

#### Prerequisites
- Python 3.7 or higher
- No additional dependencies required (uses only standard library)

#### Running the Project
```bash
cd question1_university_system
python main.py
```

### Project Structure
```
question1_university_system/
├── main.py          # Main demonstration script
├── person.py        # Base Person class
├── student.py       # Student class (inherits from Person)
├── faculty.py       # Faculty class (inherits from Person)
└── department.py    # Department and Course classes
```

### Usage Example
The `main.py` file demonstrates:
- Creating departments and courses
- Adding students and faculty
- Course enrollment and grade management
- GPA calculation and academic status checking

---

## Project 2: Social Media Analysis Pipeline

### Description
A comprehensive data analysis pipeline that scrapes book data from books.toscrape.com, cleans and processes the data, performs statistical analysis, and creates visualizations.

### Features
- Web scraping with rate limiting and error handling
- Data cleaning and preprocessing
- Statistical analysis and correlation studies
- Interactive visualizations and dashboards
- Comprehensive reporting system
- Logging and monitoring

### Setup & Installation

#### Prerequisites
- Python 3.8 or higher
- Required packages (install via requirements.txt)

#### Installation Steps
1. Navigate to the project directory:
   ```bash
   cd question2_social_media_analysis
   ```

2. Install dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

#### Running the Pipeline

##### Option 1: Run Complete Pipeline
```bash
# Basic run (scrapes 1 page by default)
python pipeline.py

# Scrape specific number of pages
python pipeline.py --pages 5

# Scrape all available pages (unlimited)
python pipeline.py --pages 0

# Skip scraping and use existing data
python pipeline.py --skip-scraping

# Combine options
python pipeline.py --pages 10 --skip-scraping
```

##### Option 2: Run Individual Steps
```bash
# Run only the scraper (specify pages)
python pipeline.py --step scraper --pages 3

# Run only the scraper (all pages)
python pipeline.py --step scraper --pages 0

# Run only the data cleaner
python pipeline.py --step cleaner

# Run only the analyzer
python pipeline.py --step analyzer

# Run only the visualizer
python pipeline.py --step visualizer
```

##### Command Line Arguments
The pipeline accepts the following arguments:
- `--pages N`: Number of pages to scrape (default: 1, use 0 for unlimited/all available pages)
- `--skip-scraping`: Skip scraping and use existing data files
- `--step STEP`: Run only a specific step (choices: scraper, cleaner, analyzer, visualizer)

##### Option 3: Run Components Directly (Alternative)
```bash
# Data scraping only
python -c "from data_collection.scraper import BookScraper; scraper = BookScraper(); scraper.scrape_books()"

# Data cleaning only
python -c "from data_processing.cleaner import DataCleaner; cleaner = DataCleaner(); cleaner.clean_data('data/scraped_books.csv')"

# Analysis only
python -c "from analysis.analyzer import BookDataAnalyzer; analyzer = BookDataAnalyzer(); analyzer.analyze_data('data/cleaned_books.csv')"

# Visualization only
python -c "from visualizations.visualizer import BookDataVisualizer; viz = BookDataVisualizer(); viz.create_all_visualizations('data/cleaned_books.csv')"
```

### Project Structure
```
question2_social_media_analysis/
├── pipeline.py              # Main pipeline orchestrator
├── pipeline.log             # Pipeline execution logs
├── scraper.log              # Scraping operation logs
├── data_collection/
│   └── scraper.py           # Web scraping module
├── data_processing/
│   └── cleaner.py           # Data cleaning module
├── analysis/
│   ├── analyzer.py          # Statistical analysis module
│   └── predictor.py         # Predictive modeling module
├── visualizations/
│   ├── visualizer.py        # Data visualization module
│   └── output_visualizations/  # Generated charts and dashboards
└── data/
    ├── scraped_books.csv    # Raw scraped data
    ├── cleaned_books.csv    # Processed data
    └── *.json/*.md          # Analysis reports
```

### Output Files
After running the pipeline, you'll find:
- **Raw data**: `data/scraped_books.csv`
- **Cleaned data**: `data/cleaned_books.csv`
- **Visualizations**: `visualizations/output_visualizations/`
- **Analysis reports**: `data/comprehensive_analysis_report_*.json` and `*.md`
- **Interactive dashboard**: `visualizations/output_visualizations/comprehensive_interactive_dashboard.html`

### Configuration Options
The pipeline can be customized by modifying parameters in `pipeline.py`:
- Number of pages to scrape
- Data cleaning thresholds
- Visualization styles
- Output formats

---

## Project 3: Healthcare Ethics Report

### Description
An academic research report focusing on healthcare ethics, examining key ethical principles and their applications in modern healthcare settings.

### Setup & Requirements
- No installation required
- Markdown viewer or text editor
- For PDF generation: pandoc or similar markdown processor

### Accessing the Report
```bash
cd question3_ethics_report
# View with any markdown viewer or text editor
notepad healthcare_ethics_report.md
```

### Project Structure
```
question3_ethics_report/
└── healthcare_ethics_report.md    # Main ethics report document
```

---

## General Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python Version**: 3.7+ (3.8+ recommended for Project 2)
- **Memory**: 2GB RAM minimum (4GB+ recommended for data analysis)
- **Storage**: 100MB free space for data and outputs

### Global Installation
To install dependencies for all projects:
```bash
# Install requirements for data analysis project
pip install -r requirements.txt

# The other projects use only standard library modules
```

### Development Environment
Recommended development setup:
- **IDE**: Visual Studio Code, PyCharm, or similar
- **Extensions**: Python extension for VS Code
- **Git**: For version control

---

## Troubleshooting

### Common Issues

#### Project 1 - University System
- **ImportError**: Ensure you're running from the `question1_university_system` directory
- **Python version**: Requires Python 3.7+

#### Project 2 - Data Analysis Pipeline
- **Package installation errors**: 
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
- **Scraping errors**: Check internet connection and website availability
- **Memory issues**: Reduce the number of pages to scrape in `pipeline.py`
- **Visualization errors**: Ensure all visualization packages are installed

#### General Issues
- **Path issues**: Use absolute paths or ensure you're in the correct directory
- **Permission errors**: Run with appropriate permissions or use virtual environment

### Getting Help
- Check log files in respective project directories
- Ensure all dependencies are correctly installed
- Verify Python version compatibility

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (if applicable)
5. Submit a pull request

## License

This project is for educational purposes as part of university coursework.
