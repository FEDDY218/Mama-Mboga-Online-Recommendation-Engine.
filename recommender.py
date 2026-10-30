
import csv
from pathlib import Path
from collections import defaultdict


DATA_PATH = Path("data") / "purchases.csv"
OUTPUT_PATH = Path("output") / "recommendations.csv"


def read_purchases(path=DATA_PATH):
    valid_rows = []
    rejected_rows = []
    seen_purchases = set()

    with open(path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Remove extra spaces from text fields
            for key in row:
                if row[key]:
                    row[key] = row[key].strip()

            # Standardise IDs
            if row.get("customer_id"):
                row["customer_id"] = row["customer_id"].upper()

            if row.get("product_id"):
                row["product_id"] = row["product_id"].upper()

            # Reject rows with missing required information
            if not row.get("customer_id") or not row.get("product_id"):
                rejected_rows.append(row)
                continue

            if not row.get("customer_name") or not row.get("product_name"):
                rejected_rows.append(row)
                continue

            if not row.get("purchase_date"):
                rejected_rows.append(row)
                continue

            # Identify duplicate customer-product-date records
            purchase_key = (
                row["customer_id"],
                row["product_id"],
                row["purchase_date"]
            )

            if purchase_key in seen_purchases:
                rejected_rows.append(row)
                continue

            seen_purchases.add(purchase_key)
            valid_rows.append(row)

    return valid_rows, rejected_rows


def jaccard(a: set, b: set) -> float:
    intersection = a & b
    union = a | b

    if not union:
        return 0.0

    return len(intersection) / len(union)


class RecommendationEngine:

    def __init__(self, purchases):
        self.customer_products = defaultdict(set)
        self.customer_names = {}
        self.product_names = {}
        self.product_categories = {}
        self.product_popularity = defaultdict(int)

        for row in purchases:
            customer_id = row["customer_id"]
            product_id = row["product_id"]

            self.customer_products[customer_id].add(product_id)
            self.customer_names[customer_id] = row["customer_name"]
            self.product_names[product_id] = row["product_name"]
            self.product_categories[product_id] = row["category"]
            self.product_popularity[product_id] += 1

    def history(self, customer_id):
        return self.customer_products.get(customer_id, set())

    def similarity(self, customer_a, customer_b):
        return jaccard(
            self.history(customer_a),
            self.history(customer_b)
        )

    def similar_customers(self, customer_id, k=3):
        scores = []

        for other_id in self.customer_products:
            if other_id != customer_id:
                score = self.similarity(customer_id, other_id)
                scores.append((other_id, score))

        scores.sort(key=lambda item: (-item[1], item[0]))
        return scores[:k]

    def candidate_products(self, customer_id, k=3):
        candidates = {}
        customer_history = self.history(customer_id)

        neighbours = self.similar_customers(customer_id, k)

        for neighbour_id, similarity_score in neighbours:
            for product_id in self.history(neighbour_id):

                if product_id not in customer_history:
                    if product_id not in candidates:
                        candidates[product_id] = {
                            "similarity_scores": [],
                            "supporting_customers": []
                        }

                    candidates[product_id]["similarity_scores"].append(
                        similarity_score
                    )
                    candidates[product_id]["supporting_customers"].append(
                        neighbour_id
                    )

        return candidates

    def score(self, product_id, evidence):
        average_similarity = (
            sum(evidence["similarity_scores"])
            / len(evidence["similarity_scores"])
        )

        total_purchases = sum(self.product_popularity.values())

        popularity = (
            self.product_popularity[product_id] / total_purchases
        )

        return (0.7 * average_similarity) + (0.3 * popularity)

    def recommend(self, customer_id, n=3):
        candidates = self.candidate_products(customer_id)
        recommendations = []

        for product_id, evidence in candidates.items():
            recommendations.append({
                "customer_id": customer_id,
                "customer_name": self.customer_names[customer_id],
                "product_id": product_id,
                "product_name": self.product_names[product_id],
                "category": self.product_categories[product_id],
                "score": self.score(product_id, evidence),
                "supporting_customers": ", ".join(
                    evidence["supporting_customers"]
                )
            })

        recommendations.sort(
            key=lambda item: (-item["score"], item["product_id"])
        )

        for rank, item in enumerate(recommendations[:n], start=1):
            item["rank"] = rank

        return recommendations[:n]

    def recommend_all(self, n=3):
        all_recommendations = []

        for customer_id in self.customer_products:
            recommendations = self.recommend(customer_id, n)

            if recommendations:
                all_recommendations.extend(recommendations)
            else:
                all_recommendations.append({
                    "customer_id": customer_id,
                    "customer_name": self.customer_names[customer_id],
                    "rank": "",
                    "product_id": "",
                    "product_name": "",
                    "category": "",
                    "score": "",
                    "supporting_customers": ""
                })

        return all_recommendations

    def export_csv(self, rows, path=OUTPUT_PATH):
        path.parent.mkdir(parents=True, exist_ok=True)

        columns = [
            "customer_id",
            "customer_name",
            "rank",
            "product_id",
            "product_name",
            "category",
            "score",
            "supporting_customers"
        ]

        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
