
import csv
from pathlib import Path
from collections import defaultdict



from recommender import read_purchases, RecommendationEngine
from recommender import DATA_PATH, OUTPUT_PATH


def main():
    # Load and clean purchase data
    valid_rows, rejected_rows = read_purchases(DATA_PATH)

    # Create the recommendation engine
    engine = RecommendationEngine(valid_rows)

    # Generate recommendations for all customers
    recommendations = engine.recommend_all(n=3)

    # Export recommendations to CSV
    engine.export_csv(recommendations, OUTPUT_PATH)

    # Display recommendations for one customer
    customer_id = next(iter(engine.customer_products))

    print("\nMAMA MBOGA RECOMMENDATION ENGINE")
    print("Customer:", engine.customer_names[customer_id])

    for item in engine.recommend(customer_id, n=3):
        print(
            item["rank"],
            item["product_name"],
            "- Score:",
            round(item["score"], 3)
        )

    # Display project summary
    print("\nPROJECT SUMMARY")
    print("Purchases read:", len(valid_rows) + len(rejected_rows))
    print("Purchases used:", len(valid_rows))
    print("Purchases rejected:", len(rejected_rows))
    print("Customers:", len(engine.customer_products))
    print("Products:", len(engine.product_names))
    print("Recommendations written:", len(recommendations))
    print("Output file:", OUTPUT_PATH)


# Run the program
if __name__ == "__main__":
    main()
