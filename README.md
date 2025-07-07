<img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white"/><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/><img src="https://www.flaticon.com/free-icons/online-scraper"/>

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
### 1️⃣ Clone the project

```bash
git clone https://github.com/USERNAME/DailyDoseOfNews.git
cd DailyDoseOfNews
```

### 2️⃣ Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Add AI Studio API Key
Create the file:
```bash
src/secret/key.py
```
and add the following line:
```python
API_KEY = "your_key"
```

## ⚡️ How to run
```bash
python3 main.py
```

## 👨‍💻 Author
Codreanu Andrei-Daniel