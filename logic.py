import statistics
from db import fetch_all
import pandas as pd

def search(keyword):
    return [r for r in fetch_all() if keyword.lower() in r[1].lower()]

def range_search(min_amount, max_amount):
    return [r for r in fetch_all() if min_amount <= r[3] <= max_amount]

def sort_by(field="amount"):
    records = fetch_all()
    idx = {"vendor": 1, "date": 2, "amount": 3}[field]
    return sorted(records, key=lambda x: x[idx])

def aggregate():
    records = fetch_all()
    amounts = [r[3] for r in records]
    vendors = [r[1] for r in records]
    categories = [r[4] for r in records]  # r[4] = category

    # Vendor frequency
    vendor_freq = {v: vendors.count(v) for v in set(vendors)}

    # Category-wise spend totals
    category_totals = {}
    for i, category in enumerate(categories):
        category_totals[category] = category_totals.get(category, 0) + amounts[i]

    return {
        "total": sum(amounts),
        "mean": statistics.mean(amounts) if amounts else 0,
        "median": statistics.median(amounts) if amounts else 0,
        "mode": statistics.mode(amounts) if amounts else 0,
        "vendor_freq": vendor_freq,
        "category_totals": category_totals  # 👈 new field
    }


def get_monthly_trend():
    rows = fetch_all()
    df = pd.DataFrame(rows, columns=["id", "vendor", "date", "amount", "category"])
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna()
    df['month'] = df['date'].dt.to_period('M').astype(str)
    trend = df.groupby('month')['amount'].sum().reset_index()
    trend['moving_avg'] = trend['amount'].rolling(window=3).mean()
    return trend
