# E-commerce Analytics Pipeline

A complete pandas-based data pipeline for loading, cleaning, merging, and analyzing real-world e-commerce data.

## About the Project

This project works with the **Olist Brazilian E-Commerce** dataset (free on Kaggle). The dataset consists of 9 linked tables covering orders, order items, payments, reviews, customers, sellers, products, category translations, and geolocation.

The raw data arrives messy: missing values, inconsistent data types, and duplicates. This makes it a strong practice ground for building a real, end-to-end pandas pipeline rather than working with a toy dataset.

## Goal

Turn raw, multi-table e-commerce data into a clean, merged dataset and answer real business questions from it — covering revenue trends, product performance, delivery impact, regional sales, customer segmentation, and retention.

## What This Project Covers

- Loading and inspecting multiple CSV files (`read_csv`, `dtypes`, missing-value profiling)
- Converting text columns to proper `datetime` types
- Merging multiple related tables (`merge`)
- Handling missing values and duplicates
- Grouping and aggregation (`groupby`, `agg`)
- Feature engineering (delivery time, delay, order month/weekday, order totals)
- Business analysis with `groupby`/`agg`
- RFM (Recency, Frequency, Monetary) customer segmentation
- Cohort retention analysis (`pivot`, `transform`)
- Data visualization with `matplotlib`
- Simple baseline forecasting (`rolling`, `pct_change`)

## Pipeline Stages

1. **Load** (`src/load.py`) — reads all raw CSV files into DataFrames.
2. **Clean** (`src/clean.py`) — converts date columns to `datetime`, removes duplicates, translates category names.
3. **Merge** (`src/merge.py`) — joins orders, order items, customers, products, sellers, payments, and reviews into a single master table.
4. **Features** (`src/features.py`) — adds calculated columns: delivery duration, delivery delay, order month/weekday, item totals.
5. **Analysis** (`src/analysis.py`) — answers core business questions (see below).
6. **Segmentation** (`src/segmentation.py`) — RFM customer segments and monthly cohort retention.
7. **Report** (`src/report.py`) — generates charts and a text summary report.
8. **Forecast** (`src/forecast.py`) — simple moving-average and growth-rate revenue forecasts.

## Business Questions Answered

- How has monthly revenue and order volume changed over time?
- Which product categories generate the most revenue?
- How much does delivery delay affect customer review scores?
- Which regions have the strongest and weakest sales?
- What percentage of customers make a repeat purchase?
- Which sellers perform best and worst?
- How does customer retention change month over month after first purchase?

## Key Findings

- Revenue grew steadily from late 2016 through 2018, peaking around November 2017, before flattening and slightly declining in mid-to-late 2018.
- Delivery delay has a strong negative effect on customer satisfaction: on-time orders average a **4.15** review score versus **2.26** for delayed orders.
- Customer retention is very low — only about **3%** of customers make a second purchase, and month-over-month cohort retention drops below 1% almost immediately after the first purchase.
- São Paulo (SP) is the clear leader in sales volume, generating roughly 3x the revenue of the next-highest state.
- `health_beauty`, `watches_gifts`, and `bed_bath_table` are the top-performing product categories by revenue.

## Project Structure

```
ecommerce-analytics/
├── data/
│   ├── raw/              # downloaded CSVs (not committed to git)
│   └── processed/        # cleaned/merged data
├── notebooks/
│   └── 01_eda.ipynb
├── src/
│   ├── load.py
│   ├── clean.py
│   ├── merge.py
│   ├── features.py
│   ├── analysis.py
│   ├── segmentation.py
│   ├── report.py
│   └── forecast.py
├── reports/
│   ├── figures/           # generated charts (.png)
│   └── summary.txt        # generated text report
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ecommerce-analytics-pandas.git
cd ecommerce-analytics-pandas

# 2. Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download the dataset
# Get "Brazilian E-Commerce Public Dataset by Olist" from Kaggle
# and place the CSV files in data/raw/

# 5. Run each stage
python3 -m src.load
python3 -m src.clean
python3 -m src.merge
python3 -m src.features
python3 -m src.analysis
python3 -m src.segmentation
python3 -m src.report
python3 -m src.forecast
```

## Technologies

Python 3, pandas, matplotlib, Jupyter.

## Notes

This project was built as a hands-on, project-based way to learn pandas — starting from raw multi-table CSV data and working through cleaning, merging, feature engineering, business analysis, customer segmentation, visualization, and basic forecasting.
