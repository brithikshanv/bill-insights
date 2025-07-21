import streamlit as st
from ocr_utils import extract_text
from parser import parse_text
from db import init_db, insert_receipt, fetch_all
from logic import aggregate, sort_by, search, range_search, get_monthly_trend
import matplotlib.pyplot as plt
import pandas as pd

init_db()
st.title("📁 BillInsight: Spend Analyzer")

file = st.file_uploader("Upload receipt (.jpg/.png/.pdf/.txt)", type=["jpg", "png", "pdf", "txt"])
if file:
    text = extract_text(file, file.name)
    receipt = parse_text(text)
    st.write("📝 Edit Parsed Fields (if needed):")

    vendor = st.text_input("Vendor", receipt.vendor)
    date = st.text_input("Date", receipt.date)
    amount = st.number_input("Amount", value=receipt.amount)
    category = st.text_input("Category", receipt.category)

    receipt.vendor = vendor
    receipt.date = date
    receipt.amount = amount
    receipt.category = category

    st.json(receipt.dict())

    if st.button("Save to Database"):
        insert_receipt(receipt)
        st.success("Saved!")

st.subheader("📊 Records")
if st.checkbox("Show All"):
    data = fetch_all()
    df = pd.DataFrame(data, columns=["ID", "Vendor", "Date", "Amount", "Category"])
    st.dataframe(df, use_container_width=True)

st.subheader("🔎 Search & Filter")
q = st.text_input("Vendor search")
if q:
    result = search(q)
    st.dataframe(pd.DataFrame(result, columns=["ID", "Vendor", "Date", "Amount", "Category"]))

min_amt = st.number_input("Min Amount", 0.0)
max_amt = st.number_input("Max Amount", 10000.0)
if st.button("Range Search"):
    result = range_search(min_amt, max_amt)
    st.dataframe(pd.DataFrame(result, columns=["ID", "Vendor", "Date", "Amount", "Category"]))

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
