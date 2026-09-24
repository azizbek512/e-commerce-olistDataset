import pandas as pd
from src.load import load_all_tables
from src.clean import clean_tables
from src.merge import build_master_table
from src.features import add_features

# oylik daromad o'zgarishi
def monthly_revenue(df:pd.DataFrame) -> pd.Series:
    return df.groupby("order_month")["item_total"].sum()

# qaysi kategoriyalar eng ko'p foyda keltiradi
def top_categories(df: pd.DataFrame, n=10) -> pd.Series:
    return (
        df.groupby("product_category_name_english")["item_total"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )

# kechikishning mijoz bahosiga ta'siri
def delay_vs_review(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("is_late")["review_score"].mean()

# sotuv kuchli va past hududlar
def sales_by_state(df: pd.DataFrame) -> pd.Series:
    return (
        df.groupby("customer_state")["item_total"]
        .sum()
        .sort_values(ascending=False)
    )

# mijozlarning qanchasi 2-marta sotib oladi
def repeat_customer_rate(df: pd.DataFrame) -> float:
    orders_per_customer = df.groupby("customer_unique_id")["order_id"].nunique()
    return (orders_per_customer > 1).mean() * 100

# sotuvchi reytinggi
def seller_performance(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("seller_id").agg(
        total_revenue = ("item_total", "sum"),
        avg_review = ("review_score", "mean"),
        num_orders = ("order_id", "nunique"),
    ).sort_values("total_revenue", ascending=False)

if __name__ == "__main__":
    raw = load_all_tables()
    cleaned = clean_tables(raw)
    master = build_master_table(cleaned)
    master = add_features(master)

    print("\n=== 1. Monthly income ===")
    print(monthly_revenue(master))
    
    print("\n=== 2. Top 10 categories ===")
    print(top_categories(master))
    
    print("\n=== 3. Delay & review ===")
    print(delay_vs_review(master))
    
    print("\n=== 4. Sales by states ===")
    print(sales_by_state(master).head(10))
    
    print("\n=== 5. Repurchase rate ===")
    print(f"{repeat_customer_rate(master):.2f}%")

    print("\n=== 6. Top 5 seller ===")
    print(seller_performance(master).head(5))

