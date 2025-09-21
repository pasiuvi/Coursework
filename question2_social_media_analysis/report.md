E-commerce Book Data Analysis Report
Executive Summary
This report details the analysis of book data scraped from the e-commerce site 

books.toscrape.com. The primary objective was to uncover patterns in product pricing, ratings, and category popularity. Through a process of data collection, cleaning, statistical analysis, and visualization, we have identified key business insights.


The analysis reveals that book prices are heavily skewed towards the lower end and vary significantly between categories, with genres like "nonfiction" and "science" having higher average prices. We found no significant linear relationship between a book's price and its star rating, indicating that customers are not necessarily paying more for higher-rated books. Finally, categories such as "default," "fiction," and "mystery" were identified as the most popular based on the number of titles available.

Methodology
The analysis was conducted in a three-stage process:


Data Collection: Book data, including titles, prices, ratings, stock availability, and categories, was scraped from all pages of the target website using a Python script with the requests and BeautifulSoup libraries.


Data Cleaning and Preprocessing: The raw data was loaded into a pandas DataFrame. We performed several cleaning operations: removing duplicate entries based on book titles, handling missing numerical values by filling them with zeros, and normalizing text data by converting it to lowercase and removing special characters.


Analysis and Visualization: The cleaned dataset was used for statistical analysis to identify trends and relationships. We calculated descriptive statistics, identified outliers, performed correlation analysis, and used a T-test for hypothesis testing. The findings were visualized using libraries like Seaborn and Plotly to create histograms, box plots, scatter plots, and bar charts.



Analysis and Findings
This section presents the detailed findings and directly addresses the key business questions.

How does price vary across categories?
The analysis shows that book prices are not uniform and exhibit significant variation across different categories. Most books are priced under £20, but certain categories command a premium.

Finding 1: Prices are skewed towards the lower end.
The histogram below shows that the vast majority of books are priced between £10 and £25, with a long tail of more expensive books.

Finding 2: Certain categories are consistently more expensive.
The box plot reveals the price ranges for the 10 most popular categories. Genres related to non-fiction and science tend to have higher median prices and a wider price range compared to fiction genres. Statistical analysis confirms that categories like nonfiction, science, and history have the highest average prices.

Are there any significant relationships between ratings and prices?
Our analysis indicates there is no meaningful linear relationship between a book's star rating and its price.

Finding 1: Correlation is negligible.
The scatter plot of price versus rating shows points widely dispersed with no clear upward or downward trend. The red regression line is nearly flat, visually confirming the lack of a strong linear relationship.

Finding 2: Rating is a poor predictor of price.
A simple linear regression model was built to predict price based on rating. The model yielded an 

R-squared value near 0.0, which means that the variation in star ratings explains almost none of the variation in price. This statistically confirms that customers do not pay a premium for higher-rated books.

Which categories are most popular based on your data?
The popularity of categories, measured by the number of unique titles available, is highly concentrated in a few key genres.

Finding 1: "Default," "Fiction," and "Mystery" are the most stocked categories.
The bar chart below clearly illustrates the top 10 most popular categories in the dataset. The "default" category, which appears to be a general classification on the site, has the most titles, followed closely by traditional genres like fiction and mystery.

Finding 2: Popularity does not always mean highest-rated.
Interestingly, while some popular categories like "fiction" and "mystery" have high average ratings, other popular ones do not necessarily lead in quality. This suggests an opportunity to promote high-quality books in less popular but well-regarded categories.

Conclusion
This analysis provides valuable insights into the e-commerce book market. The key takeaway is that pricing strategies appear to be driven more by category and genre than by customer ratings. The most popular categories represent clear opportunities for targeted marketing and inventory management. Based on these findings, we recommend focusing promotional efforts on curated lists within popular genres and exploring dynamic pricing strategies for high-demand categories.