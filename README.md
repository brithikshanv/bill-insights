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

## File Structure

bill-management-system/
├── app.py # Streamlit application
├── db.py # SQLite database setup and access
├── models.py # Pydantic models for validation
├── logic.py # Search, sort, aggregate, monthly summary
├── parser.py # Rule-based text and date parsing
├── ocr_utils.py # OCR logic for image/pdf
├── requirements.txt
└── README.md

---

## Setup Instructions

### 1. Clone the repository

git clone: https://github.com/your-username/bill-management-system.git

cd bill-management-system

### 2. Set up a virtual environment (optional)

python -m venv env

source env/bin/activate  

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the app

streamlit run main.py


## Conclusion

The Bill Management System is designed to be a practical and efficient tool for managing, categorizing, and analyzing bills and receipts in one place. It brings together OCR, data parsing, validation, and interactive visualizations into a streamlined, user-friendly application.

Whether you're managing personal expenses, analyzing vendor trends, or preparing financial summaries, this system can serve as a solid foundation. Contributions and enhancements are welcome to help improve and extend its capabilities.

For any issues or feature requests, feel free to open an issue or submit a pull request.

