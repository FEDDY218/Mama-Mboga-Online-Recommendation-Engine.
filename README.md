# Mama Mboga Online Recommendation Engine

## Project Overview

The Mama Mboga Online Recommendation Engine is a Python-based grocery recommendation system that suggests products to customers based on their previous purchase histories.

The system uses customer purchase patterns, Jaccard similarity, and product popularity to identify relevant products that customers may be interested in purchasing.

## Project Objectives

- Clean and validate customer purchase records.
- Calculate customer similarity using the Jaccard coefficient.
- Identify customers with similar purchasing behaviour.
- Generate product recommendations based on similar customers.
- Rank recommendations using similarity and product popularity.
- Export recommendations for all customers into a CSV file.

## Technologies Used

- Python
- CSV module
- Collections module
- Pandas (for exploratory analysis and similarity matrix checks in the notebook)
- Jupyter Notebook

## Recommendation Methodology

### 1. Data Cleaning
Purchase records are cleaned by removing unnecessary spaces, standardising customer and product IDs, and rejecting invalid or duplicate records.

### 2. Jaccard Similarity
Jaccard similarity measures how similar two customers are based on the products they have purchased.

### 3. Similar Customer Identification
The engine identifies the three most similar customers based on their purchase histories.

### 4. Candidate Product Generation
Products purchased by similar customers but not yet purchased by the target customer are selected as recommendation candidates.

### 5. Recommendation Scoring

Recommendations are ranked using a weighted score:

**Score = (0.7 × Average Similarity) + (0.3 × Product Popularity)**

This combines customer similarity with product popularity.

## Project Structure

```text
Mama-Mboga-Online-Recommendation-Engine/
│
├── data/
│   └── purchases.csv
│
├── output/
│   └── recommendations.csv
│
├── tests/
│
├── recommender.py
├── main.py
├── main.ipynb
├── README.md
└── requirements.txt
```

## How to Run the Project

1. Clone or download the repository.
2. Open the project folder in VS Code.
3. Ensure Python is installed.
4. Open the terminal in the project directory.
5. Run:

```bash
python main.py
```

The program processes the purchase data, generates recommendations, displays a project summary, and exports the results to:

`output/recommendations.csv`

## Output

The exported CSV contains:

- customer_id
- customer_name
- rank
- product_id
- product_name
- category
- score
- supporting_customers

Customers without recommendations are also included in the output.

## Key Learning Outcomes

- Python functions and classes
- Dictionaries, sets, and tuples
- Data cleaning and validation
- Set operations
- Similarity calculations
- Sorting and ranking
- CSV file handling
- Object-oriented programming

## Author

**Feddy Mwanjumwa**

Data Science, AI & Analytics Portfolio Project