# Bill Management System

The **Bill Management System** is a full-stack application built with Python, Streamlit, SQLite, and OCR. It allows users to upload receipts in various formats, extracts key information using rule-based logic and optical character recognition, and provides smart insights through visual dashboards and analytics.

---

## Features

### Receipt Upload & Extraction
- Upload receipts in `.jpg`, `.png`, `.pdf`, `.txt` formats
- Extract structured data using OCR (Tesseract) and regex:
  - Vendor / Biller
  - Date of Transaction
  - Amount
  - Category (auto-mapped)
  - Currency (detected from symbols)

### Editing & Storage
- Manually edit extracted data in the UI
- Store data in SQLite (ACID-compliant)
- Automatically categorize vendors (e.g., Food, Shopping, Utilities)

### Search, Filter, and Analysis
- Search by vendor keyword
- Filter by:
  - Category (dropdown)
  - Amount range
- Sort by amount, date, or vendor
- Aggregated statistics:
  - Total, Mean, Median, Mode
- Currency display per receipt

### Visualizations & Exports
- Bar chart for vendor frequency
- Line chart for monthly spending trends
- Export all data as `.csv` or `.json`
- Download monthly summaries

---

## Tech Stack

| Component        | Technology       |
|------------------|------------------|
| UI               | Streamlit        |
| Backend Logic    | Python           |
| OCR              | Tesseract via `pytesseract` |
| Data Validation  | Pydantic         |
| Storage          | SQLite           |
| Visualization    | Matplotlib, Pandas |

---



