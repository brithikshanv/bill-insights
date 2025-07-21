import re
from models import Receipt

def map_category(vendor: str) -> str:
    vendor = vendor.lower()

    CATEGORY_MAP = {
        "Shopping": ["amazon", "flipkart", "myntra", "ajio", "shein", "meesho", "nykaa", "snapdeal", "tatacliq", "limeroad", "shopclues", "koovs", "clubfactory", "paytm mall", "jiomart"],
        "Groceries": ["bigbasket", "grofers", "dmart", "more supermarket", "reliance fresh", "spencer", "nature's basket", "easyday", "blinkit", "jio mart", "bbnow", "zepto"],
        "Food & Delivery": ["swiggy", "zomato", "ubereats", "eatsure", "domino", "pizza hut", "kfc", "mcdonald", "faasos", "box8", "behrouz", "freshmenu", "eatclub", "grill", "biriyani", "foodpanda"],
        "Electricity": ["tneb", "bescom", "tata power", "adani electricity", "bills", "electricity", "cesc", "pspcl", "mescom"],
        "Internet & Mobile": ["airtel", "jio", "vi", "vodafone", "bsnl", "act fibernet", "hathway", "den broadband", "excitel"],
        "Transportation": ["uber", "ola", "rapido", "redbus", "abhibus", "irctc", "makemytrip", "blablacar", "shuttl", "train", "bus ticket", "rail ticket", "metro", "bmrtc", "tsrtc", "ksrtc", "tnstc", "msrtc"],
        "Entertainment": ["bookmyshow", "inox", "pvr", "cinepolis", "paytm movies", "ticketnew", "justickets", "wave cinemas"],
        "Hotels & Travel": ["oyo", "goibibo", "makemytrip", "yatra", "airbnb", "booking.com", "tripadvisor", "trivago"],
        "Healthcare & Medical": ["pharmeasy", "netmeds", "1mg", "apollo", "medplus", "tata 1mg", "medlife", "practo", "ayush", "clinic"],
        "Education": ["byjus", "unacademy", "udemy", "coursera", "edx", "upgrad", "greatlearning", "vedantu", "whitehat", "skillshare"],
        "Finance & Payments": ["paytm", "google pay", "phonepe", "cred", "razorpay", "mobikwik", "freecharge", "instamojo"],
        "Fuel": ["bharat petroleum", "indian oil", "hpcl", "hindustan petroleum", "shell", "fuel", "petrol", "diesel"],
        "Misc": []
    }

    for category, keywords in CATEGORY_MAP.items():
        if any(k in vendor for k in keywords):
            return category

    return "Misc"

def detect_currency(text: str) -> str:
    if "₹" in text:
        return "INR"
    elif "$" in text:
        return "USD"
    elif "€" in text:
        return "EUR"
    elif "£" in text:
        return "GBP"
    else:
        return "Unknown"

def parse_text(text: str) -> Receipt:
    vendor = re.search(r"(?i)(from|vendor):?\s*(.+)", text)
    amount = re.search(r"(?i)(total|amount):?\s*₹?\$?([\d,]+\.\d{2})", text)
    date = re.search(r"\d{2}[-/]\d{2}[-/]\d{4}", text)
    currency = detect_currency(text)

    vendor_name = vendor.group(2).strip() if vendor else "Unknown"
    return Receipt(
        vendor=vendor_name,
        date=date.group() if date else "Unknown",
        amount=float(amount.group(2).replace(",", "")) if amount else 0.0,
        category=map_category(vendor_name),
        currency=currency
    )


