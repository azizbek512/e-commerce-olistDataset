import pandas as pd
from src.load import load_all_tables
from src.clean import clean_tables
from src.merge import build_master_table

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1. yetkazib berish kuni
    df["delivery_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days

    # 2. kechikish: musbat -> kechikkan, manfiy -> oldin yetib borgan
    df["delivery_delay_days"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.days

    # 3. buyurtma berilgan sana
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M")
    df["order_weekday"] = df["order_purchase_timestamp"].dt.day_name()

    # 4. buyurtma summasi
    df["item_total"] = df["price"] + df["freight_value"]

    # 5. kechikkanmi
    df["is_late"] = df["delivery_delay_days"] > 0

    return df

if __name__ == "__main__":
    raw = load_all_tables()
    cleaned = clean_tables(raw)
    master = build_master_table(cleaned)
    master = add_features(master)

    print(master[["delivery_days", "delivery_delay_days", "order_month", "order_weekday", "item_total", "is_late"]].head(10))
    print("\nAverage delivery day:", master["delivery_days"].mean())
    print("Percentage of late orders:", master["is_late"].mean() * 100)