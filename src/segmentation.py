import pandas as pd
from src.load import load_all_tables
from src.clean import clean_tables
from src.merge import build_master_table
from src.features import add_features

# Har bir mijoz uchun Recency, Frequency, Monetary
def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    snapshot_date = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("customer_unique_id").agg(
        recency = ("order_purchase_timestamp", lambda x: (snapshot_date - x.max()).days),

        frequency = ("order_id", "nunique"),

        monetary = ("item_total", "sum"),
    )

    rfm["r_score"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1])
    rfm["f_score"] = rfm["frequency"].apply(lambda x: 1 if x == 1 else 4)
    rfm["m_score"] = pd.qcut(rfm["monetary"], 4, labels=[1, 2, 3, 4])

    def segment(row):
        r, f, m = int(row["r_score"]), int(row["f_score"]), int(row["m_score"])

        if r >= 3 and f >= 3 and m >= 3:
            return "Champions"              
        elif r >= 3 and f >= 3 and m < 3:
            return "Loyal, Low Spend"       
        elif r >= 3 and f <= 2:
            return "New/Promising"          
        elif r <= 2 and f >= 3 and m >= 3:
            return "Loyal (At Risk)"        
        elif r <= 2 and f >= 3 and m < 3:
            return "At Risk, Low Value"     
        else:
            return "Lost/Low Value"

    rfm["segment"] = rfm.apply(segment, axis=1)

    return rfm


def cohort_retention(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    df["cohort_month"] = df.groupby("customer_unique_id")["order_purchase_timestamp"].transform("min").dt.to_period("M")

    df["cohort_index"] = (
        (df["order_month"].dt.year - df["cohort_month"].dt.year) * 12
        + (df["order_month"].dt.month - df["cohort_month"].dt.month)
    )

    cohort_data = df.groupby(["cohort_month", "cohort_index"])["customer_unique_id"].nunique()
    cohort_pivot = cohort_data.reset_index().pivot(
        index="cohort_month", columns="cohort_index", values="customer_unique_id"
    )

    cohort_size = cohort_pivot.iloc[:, 0]
    retention = cohort_pivot.divide(cohort_size, axis=0) * 100
    
    return retention


if __name__ == "__main__":
    raw = load_all_tables()
    cleaned = clean_tables(raw)
    master = build_master_table(cleaned)
    master = add_features(master)

    print("\n=== RFM segmentation ===")
    rfm = compute_rfm(master)
    print(rfm["segment"].value_counts())
    print("\nExample (first 5 clients): ")
    print(rfm.head())

    print("\n=== Cohort retention (%) ===")
    retention = cohort_retention(master)
    print(retention.round(1))