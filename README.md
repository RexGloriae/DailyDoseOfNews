# 🗞️ DailyDoseOfNews 🗞️

A Python Web-Scraper for automated collection of news from well-known sources, storing them in a database and presenting them trough a REST API

---

## 📜 Description

**DailyDoseOfNews** is a modular scrapper which:

✅ Collects articles from various news sources 
✅ Stores articles in a SQLite Database  
✅ Generates descriptions of each article using AI Studio
✅ Uses a REST API to provide the articles

The project has been designed to be easily extended and to run periodically, either manually or timed.

## 🏁 Fast setup
1. Install all the requirements using `pip install requirements.txt`.
2. Generate an API Key from AI Studio.
3. Run the following command in the project directory: `mkdir src/hidden && touch src/hidden/key.py`
4. In `key.py` write the following line `API_KEY = "" # your key goes here` then save.

### 1️⃣ Clonează proiectul

```bash
git clone https://github.com/USERNAME/DailyDoseOfNews.git
cd DailyDoseOfNews
```