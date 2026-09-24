import pandas as pd
from src.load import load_all_tables


#yangi sana qoshilganda, faqat shu dict ga bitta col qoshiladi
DATE_COLS = {
    "orders": [
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ],
    "reviews": ["review_creation_date", "review_answer_timestamp"],
    "order_items": ["shipping_limit_date"],
}

def clean_tables(tables: dict) -> dict:
    tables = {name: df.copy() for name, df in tables.items()}

    # 1. Sana ustunlarini datetime turiga o'tkazish
    for table_name, cols in DATE_COLS.items():
        for col in cols:
            tables[table_name][col] = pd.to_datetime(
                tables[table_name][col], errors="coerce"
            )

    # 2. Dublikatlarni olib tashlash
    for name, df in tables.items():
        before = len(df)
        tables[name] = df.drop_duplicates()
        after = len(tables[name])
        if before != after:
            print(f"{name}: {before - after} dublicats deleted")

    # 3. reviews'dagi bo'sh izohlarni "izoh yo'q" deb belgilash (o'chirmaymiz!)
    tables["reviews"]["review_comment_message"] = (
        tables["reviews"]["review_comment_message"].fillna("no comment")
    )
    tables["reviews"]["review_comment_title"] = (
        tables["reviews"]["review_comment_title"].fillna("no comment")
    )

    # 4. Kategoriya nomini inglizchaga tarjima qilish
    cat_map = tables["category_translation"].set_index(
        "product_category_name"
    )["product_category_name_english"]
    tables["products"]["product_category_name_english"] = (
        tables["products"]["product_category_name"].map(cat_map)
    )

    return tables

if __name__ == "__main__":
    raw = load_all_tables()
    cleaned = clean_tables(raw)
    print(cleaned["orders"].dtypes)
    print(cleaned["products"][["product_category_name", "product_category_name_english"]].head())