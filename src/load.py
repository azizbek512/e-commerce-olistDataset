import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")

def load_all_tables():
    tables = {
        "orders": pd.read_csv(RAW_DIR / "olist_orders_dataset.csv"),
        "order_items": pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv"),
        "payments": pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv"),
        "reviews": pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv"),
        "customers": pd.read_csv(RAW_DIR / "olist_customers_dataset.csv"),
        "sellers": pd.read_csv(RAW_DIR / "olist_sellers_dataset.csv"),
        "products": pd.read_csv(RAW_DIR / "olist_products_dataset.csv"),
        "category_translation": pd.read_csv(RAW_DIR / "product_category_name_translation.csv"),
    }
    return tables

if __name__ == "__main__":
    tables = load_all_tables()
    for name, df in tables.items():
        print(f"\n=== {name} ===")
        print("Shakli: ", df.shape)
        print(df.dtypes)
        print("\nBo'sh qiymatlar:\n", df.isnull().sum()[df.isnull().sum() > 0])