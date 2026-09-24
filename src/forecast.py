import pandas as pd
from src.load import load_all_tables
from src.clean import clean_tables
from src.merge import build_master_table
from src.features import add_features
from src.analysis import monthly_revenue

# oxirgi oyga asoslanib keyingi oylarni bashorat qilish
def simple_moving_average_forecast(revenue: pd.Series, window: int=3, periods_ahead: int=3) -> pd.Series:
    rolling_avg = revenue.rolling(window=window).mean()

    last_avg =  rolling_avg.iloc[-1]
    last_period = revenue.index[-1]
    future_periods = pd.period_range(
        start=last_period + 1, periods=periods_ahead, freq="M"
    )

    forecast = pd.Series([last_avg] * periods_ahead, index=future_periods)

    return forecast

# o'sish suratiga asoslangan bashorat -> oxirgi oylarning o'sish foizini kelajakka qo'llaydi.
def seasonal_growth_forecast(revenue: pd.Series, periods_ahead: int=3) -> pd.Series:
    growth_rates = revenue.pct_change()
    avg_growth = growth_rates.tail(6).mean()

    last_value = revenue.iloc[-1]
    last_period = revenue.index[-1]
    future_periods = pd.period_range(
        start=last_period + 1, periods=periods_ahead, freq="M"
    )

    forecast_value = []
    current_value = last_value
    for _ in range(periods_ahead):
        current_value = current_value * (1 + avg_growth)
        forecast_value.append(current_value)

    forecast = pd.Series(forecast_value, index=future_periods)
    return forecast


if __name__ == "__main__":
    raw = load_all_tables()
    cleaned = clean_tables(raw)
    master = build_master_table(cleaned)
    master = add_features(master)

    revenue = monthly_revenue(master)

    revenue_stable = revenue["2017-01":"2018-08"]

    print("=== Last 6 month ===")
    print(revenue_stable.tail(6))

    print("\n=== Forecast: Moving average method")
    sma_forecast = simple_moving_average_forecast(revenue_stable, window=3, periods_ahead=3)
    print(sma_forecast)

    print("\n=== Forecast: growth rate method ===")
    growth_forecast = seasonal_growth_forecast(revenue_stable, periods_ahead=3)
    print(growth_forecast)