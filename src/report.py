import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from src.load import load_all_tables
from src.clean import clean_tables
from src.merge import build_master_table
from src.features import add_features
from src.analysis import monthly_revenue, top_categories, delay_vs_review, sales_by_state
from src.segmentation import compute_rfm, cohort_retention

FIGURES_DIR = Path("reports/figures")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# oylik daromad
def plot_monthly_revenue(df: pd.DataFrame):
    revenue = monthly_revenue(df)
    fig, ax = plt.subplots(figsize=(10, 5))
    revenue.plot(ax=ax, marker="o")

    ax.set_title("Monthly income (2016-2018)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Income (BRL)")
    fig.tight_layout()

    fig.savefig(FIGURES_DIR / "monthly_revenue.png")
    plt.close(fig)


# top 10 kategoriya daromadi
def plot_top_categories(df: pd.DataFrame):
    categories = top_categories(df, n=20)

    fig, ax = plt.subplots(figsize=(10, 6))
    categories.plot(kind="barh", ax=ax)

    ax.set_title("Top 10 categories (By income)")
    ax.set_xlabel("Income (BRL)")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "top_categories.png")
    plt.close(fig)

# kechikish va o'rtacha baho
def plot_delay_vs_review(df):
    result = delay_vs_review(df)
    result.index = ["On time", "Delayed"]

    fig, ax = plt.subplots(figsize=(6, 5))
    result.plot(kind="bar", ax=ax, color=["green", "red"])

    ax.set_title("Delivery status and average rating")
    ax.set_ylabel("Average rating (1-5)")
    ax.set_xticklabels(result.index, rotation=0)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "delay_vs_review.png")
    plt.close(fig)

# top 10 state boyicha
def plot_sales_by_state(df: pd.DataFrame):
    states = sales_by_state(df).head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    states.plot(kind="bar", ax=ax)

    ax.set_title("Top 10 state (By sale)")
    ax.set_ylabel("Income (BRL)")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "sales_by_state.png")
    plt.close(fig)

# rfm segmentlari boyicha
def plot_rfm_segments(rfm: pd.DataFrame):
    counts = rfm["segment"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    counts.plot(kind="bar", ax=ax, color="steelblue")

    ax.set_title("Distribution of customers by RFM segments")
    ax.set_ylabel("Client number")
    ax.set_xticklabels(counts.index, rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "rfm_segments.png")
    plt.close(fig)

# cohort retention heatmap
def plot_cohort_heatmap(retention: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(14, 8))
    im = ax.imshow(retention.values, cmap="YlOrRd", aspect="auto")

    ax.set_yticks(range(len(retention.index)))
    ax.set_yticklabels(retention.index.astype(str))

    ax.set_xticks(range(len(retention.columns)))
    ax.set_xticklabels(retention.columns)

    ax.set_title("Customer retention - cohort analysis")
    ax.set_xlabel("How many months have passed since the first purchase")
    ax.set_ylabel("Cohort (First purchase month)")

    fig.colorbar(im, ax=ax, label="Retention rate (%)")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "cohort_retention.png")
    plt.close(fig)

# barcha natijalarni report qilish
def write_summary_report(df: pd.DataFrame, rfm: pd.DataFrame):
    total_revenue = df["item_total"].sum()
    total_orders = df["order_id"].nunique()
    avg_review = df["review_score"].mean()
    repeat_rate = (rfm["frequency"] > 1).mean() * 100
    late_rate = df["is_late"].mean() * 100

    report_text = f"""
E-COMMERCE ANALYSIS REPORT
============================

General indicators:
- Total revenue: {total_revenue:,.2f} BRL
- Total orders: {total_orders:,}
- Average cost: {avg_review:.2f} / 5
- Repurchase rate: {repeat_rate:.2f}%
- Delayed orders: {late_rate:.2f}%

Key Takeaways:
1. Revenue grew steadily throughout 2016–2018, peaking in November 2017.
2. Delivery delays have a strong negative impact on customer ratings 
   (an average rating difference of over 2 points).
3. Customer retention is very low — only {repeat_rate:.2f}% 
   of customers make repeat purchases.
4. The state of São Paulo is the clear leader in sales.

Recommendations:
1. Focus should be placed on improving delivery times.
2. Launching email/discount campaigns to retain one-time 
   buyers is recommended.
"""
    report_path = Path("reports")
    report_path.mkdir(exist_ok=True)
    with open(report_path / "summary.txt", "w", encoding="utf-8") as f:
        f.write(report_text)

    print(report_text)

if __name__=="__main__":
    raw = load_all_tables()
    cleaned = clean_tables(raw)
    master = build_master_table(cleaned)
    master = add_features(master)
    rfm = compute_rfm(master)
    retention = cohort_retention(master)

    plot_monthly_revenue(master)
    plot_top_categories(master)
    plot_delay_vs_review(master)
    plot_sales_by_state(master)
    plot_rfm_segments(rfm)
    plot_cohort_heatmap(retention)

    write_summary_report(master, rfm)

    print(f"\nAll graphics are saved: {FIGURES_DIR}/")
    print("Report saved: reports/summary.txt")