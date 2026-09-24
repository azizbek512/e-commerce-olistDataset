import pandas as pd
from src.load import load_all_tables
from src.clean import clean_tables

def build_master_table(tables: dict) -> pd.DataFrame:
    orders = tables["orders"]
    order_items = tables["order_items"]
    payments = tables["payments"]
    reviews = tables["reviews"]
    customers = tables["customers"]
    sellers = tables["sellers"]
    products = tables["products"]

    # 1. 1ta buyurtma va bir nechta mahsulot
    df = order_items.merge(orders, on="order_id", how="left")

    # 2. bitta buyurtma -> bitta mijoz
    df = df.merge(customers, on="customer_id", how="left")

    # 3. mahsulot malumoti
    df = df.merge(products, on="product_id", how="left")

    # 4. sotuvchi
    df = df.merge(sellers, on="seller_id", how="left")

    # 5. bitta buyurtma uchun bir nechta to'lov
    payments_agg = payments.groupby("order_id", as_index=False)["payment_value"].sum()
    df = df.merge(payments_agg, on="order_id", how="left")

    # 6. bitta buyurtma uchun bitta baho
    reviews_slim = reviews[["order_id", "review_score"]].drop_duplicates(subset="order_id")
    df = df.merge(reviews_slim, on="order_id", how="left")

    return df


if __name__ == "__main__":
    raw = load_all_tables()
    cleaned = clean_tables(raw)
    master = build_master_table(cleaned)
    print("Shape of master schedule: ", master.shape)
    print(master.columns.tolist())
    print(master.isnull().sum()[master.isnull().sum() > 0])