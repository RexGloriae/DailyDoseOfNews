<img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white"/><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>

# 🗞️ DailyDoseOfNews 🗞️

A Python Web-Scraper for automated collection of news from well-known sources, storing them in a database and presenting them on a Web based client.

---

## 📜 Description

**DailyDoseOfNews** is a modular scrapper which:

- ✅ Collects articles from various news sources
- ✅ Stores articles in a SQLite Database
- ✅ Generates descriptions of each article using AI Studio
- ✅ Uses a REST API to provide the articles
- ✅ Provides a web based client for the user
- ✅ Provides different statistics for articles
- ✅ Provides search functions for finding articles with ease
- ✅ Filters articles by source
- ✅ Articles can be marked as read and/or as favorite
- ✅ Favorite articles are shown in their own tab

The project has been designed to be easily extended.

## 🏁 Fast setup
### 1️⃣ Clone the project

```bash
git clone https://github.com/USERNAME/DailyDoseOfNews.git
cd DailyDoseOfNews
```

### 2️⃣ Give execution rights to the setup
```bash
chmod +x setup.sh
```

### 3️⃣ Run the setup script
```bash
./setup.sh
```
#### NOTE: Python3 needs to be installed manually by the user prior to running the setup.

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

Run
```bash
python3 src/api.py
```
in order to start the API which will provide you the data.

Run
```bash
python3 src/gui.py
```
and you can open the application on web at `http://localhost:8080/articles`.

## 👨‍💻 Author
Codreanu Andrei-Daniel