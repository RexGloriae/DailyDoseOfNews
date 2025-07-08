<img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white"/><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>

# 🗞️ DailyDoseOfNews 🗞️

A Python Web-Scraper for automated collection of news from well-known sources, storing them in a database and presenting them on a Web based client.

---

## 📜 Description

**DailyDoseOfNews** is a modular scrapper which:

<ul>✅ Collects articles from various news sources</ul>
<ul>✅ Stores articles in a SQLite Database</ul>
<ul>✅ Generates descriptions of each article using AI Studio</ul>
<ul>✅ Uses a REST API to provide the articles</ul>
<ul>✅ Provides a web based client for the user</ul>
<ul>✅ Provides different statistics for articles</ul>
<ul>✅ Provides search functions for finding articles with ease</ul>
<ul>✅ Filters articles by source</ul>
<ul>✅ Articles can be marked as read and/or as favorite</ul>
<ul>✅ Favorite articles are shown in their own tab</ul>

The project has been designed to be easily extended.

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
You need to use your own API Key for AI Studio.

## ⚡️ How to run
Enter the virtual environment by running
```bash
source venv/bin/activate
```
Execute
```bash
python3 src/api.py
```
in order to start the API which will provide you the data.
Then execute
```bash
python3 src/gui.py
```
and you can open the application on web at `http://localhost:8080/articles`.

## 👨‍💻 Author
Codreanu Andrei-Daniel