import streamlit as st
from ocr_utils import extract_text
from parser import parse_text
from db import init_db, insert_receipt, fetch_all
from logic import aggregate, sort_by, search, range_search, get_monthly_trend
import matplotlib.pyplot as plt
import pandas as pd
import pytesseract
from parser import map_category


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

CATEGORIES = [
    "All", "Shopping", "Groceries", "Food & Delivery", "Electricity",
    "Internet & Mobile", "Transportation", "Entertainment", "Hotels & Travel",
    "Healthcare & Medical", "Education", "Finance & Payments", "Fuel", "Misc"
]

CURRENCIES = ["INR", "USD", "EUR", "GBP", "Unknown"]

init_db()

st.title(" BillInsight: Spend Analyzer")

file = st.file_uploader("Upload receipt (.jpg/.png/.pdf/.txt)", type=["jpg", "png", "pdf", "txt"])
if file:
    text = extract_text(file, file.name)
    receipt = parse_text(text)
    st.write("📝 Edit Parsed Fields (if needed):")

    vendor = st.text_input("Vendor", receipt.vendor)
    date = st.text_input("Date", receipt.date)
    amount = st.number_input("Amount", value=receipt.amount)
    category = st.selectbox("Category", CATEGORIES, index=CATEGORIES.index(receipt.category) if receipt.category in CATEGORIES else len(CATEGORIES)-1)
    currency = st.selectbox("Currency", CURRENCIES, index=CURRENCIES.index(receipt.currency) if receipt.currency in CURRENCIES else len(CURRENCIES)-1)
   
    receipt.vendor = vendor
    receipt.date = date
    receipt.amount = amount
    receipt.category = category
    receipt.currency = currency

    st.json(receipt.dict())

    if st.button("Save to Database"):
        insert_receipt(receipt)
        st.success("Saved!")

st.subheader("📊 Records")
if st.checkbox("Show All"):
    data = fetch_all()
    df = pd.DataFrame(data, columns=["ID", "Vendor", "Date", "Amount", "Category"," Currency"])
    st.dataframe(df, use_container_width=True)

if st.checkbox("Enable Export"):
    df = pd.DataFrame(fetch_all(), columns=["ID", "Vendor", "Date", "Amount", "Category", "Currency"])

    export_format = st.selectbox("Select export format", ["CSV", "JSON"])
    if export_format == "CSV":
        st.download_button("Download CSV", df.to_csv(index=False), file_name="receipts.csv", mime="text/csv")
    else:
        st.download_button("Download JSON", df.to_json(orient="records", indent=2), file_name="receipts.json", mime="application/json")


st.subheader("🔎 Search & Filter")
q = st.text_input("Vendor search")
if q:
    result = search(q)
    st.dataframe(pd.DataFrame(result, columns=["ID", "Vendor", "Date", "Amount", "Category"," Currency"]))

min_amt = st.number_input("Min Amount", 0.0)
max_amt = st.number_input("Max Amount", 10000.0)
if st.button("Range Search"):
    result = range_search(min_amt, max_amt)
    st.dataframe(pd.DataFrame(result, columns=["ID", "Vendor", "Date", "Amount", "Category", "Currency"]))

st.subheader("🧠 Insights")
agg = aggregate()
st.write(agg)

st.subheader("📈 Vendor Frequency")
vendors = agg["vendor_freq"]
fig, ax = plt.subplots()
ax.bar(vendors.keys(), vendors.values())
ax.set_title("Vendor Frequency")
st.pyplot(fig)

st.subheader("📅 Monthly Spend Trend")
trend = get_monthly_trend()
if not trend.empty:
    fig, ax = plt.subplots()
    ax.plot(trend['month'], trend['amount'], label='Monthly Total', marker='o')
    ax.plot(trend['month'], trend['moving_avg'], label='3-Month Moving Avg', linestyle='--')
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.set_title("Monthly Spend Trend")
    ax.legend()
    st.pyplot(fig)
else:
    st.info("Not enough data for trend visualization.")

from logic import get_monthly_summary

st.subheader("Download Monthly Summary")
monthly_summary = get_monthly_summary()
if not monthly_summary.empty:
    st.dataframe(monthly_summary)
    st.download_button("Download Monthly Summary as CSV", 
                       monthly_summary.to_csv(index=False), 
                       file_name="monthly_summary.csv", 
                       mime="text/csv")
else:
    st.info("Not enough data for monthly summary.")


st.subheader("🥧 Category-wise Spend Distribution")

category_spend = agg.get("category_totals", {})
if category_spend:
    fig2, ax2 = plt.subplots()
    ax2.pie(category_spend.values(), labels=category_spend.keys(), autopct="%1.1f%%", startangle=140)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig2)
else:
    st.info("No data available for category-wise distribution.")
