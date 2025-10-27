# 💼 LinkedIn Job Trends Dashboard

An interactive **Streamlit dashboard** to visualize LinkedIn job posting trends across India.  
It shows insights on job types, locations, skills, and internships — built using **Python, Pandas, and Seaborn**.

---

## 🚀 Features
- Filter jobs by **keyword**, **location**, or **internship**
- Visualize **job counts by keyword** & **city**
- Compare **internship vs full-time job ratios**
- Explore **top skills by city** with a heatmap
- Browse job listings directly from LinkedIn data

---

## 🧠 Tech Stack
- **Python 3**
- **Streamlit** — Frontend framework
- **Pandas** — Data manipulation
- **Matplotlib & Seaborn** — Data visualization

---

## ▶️ How to Run

1. **Clone this repository**
   ```bash
   git clone https://github.com/arunabhiam/Linkedin-Job-Trend-Analyser.git
   cd Linkedin-Job-Trend-Analyser
2. **Install dependencies**
    ```bash 
    pip install -r requirements.txt
3. **Run the Streamlit app**
    ```bash 
    streamlit run src/app.py
---
## 📊 Dataset
   The app uses a cleaned LinkedIn job dataset (data/cleaned_jobs.csv) containing:
   Title, Company, Location, Keyword, Job Type, is_internship, Skills, Link
---
## App Link
   https://linkedinjobtrends.streamlit.app/
---
## 🧩 Future Scope & Notes

🔍 Add sentiment analysis on job descriptions to identify trending skill demands.

🤖 Integrate NLP models (like BERT) to auto-classify job roles.

🌍 Expand dataset to cover global job markets.

💾 Add database backend (e.g., PostgreSQL) for dynamic updates.

📈 Enable real-time scraping from LinkedIn or other job APIs.

🧠 Deploy on Streamlit Cloud or Render for easy public access.
