import requests
from datetime import datetime, timedelta
import re

def download_site(URL):
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return response.text

def conv_relative_date(text):
    now = datetime.now()
    text = text.strip().lower()
    if "minute" in text:
        minutes = int(re.search(r"(\d+)", text).group(1))
        return now - timedelta(minutes=minutes)
    elif "ora" in text or "ore" in text:
        hours = int(re.search(r"(\d+)", text).group(1))
        return now - timedelta(hours=hours)
    else:
        return "expired"
