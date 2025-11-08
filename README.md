# Smart Data Cleaner App 

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Gemini](https://img.shields.io/badge/Gemini%20API-AI%20Powered-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

> 🚀 **An AI-powered Streamlit app that cleans, analyzes, and improves your datasets — instantly!**

---

## ✨ Overview

**Smart Data Cleaner** automatically detects and fixes issues in messy datasets using **Streamlit**, **Pandas**, and **Google Gemini AI**.  
It removes duplicates, fills missing values intelligently, handles outliers, drops empty columns, and generates a **Data Quality Score** and **AI Cleaning Report (PDF)**.

---

## 🧠 Key Features

✅ Automatic data cleaning (duplicates, missing values, data types)  
✅ Outlier detection using IQR method  
✅ Drops completely empty or blank columns  
✅ Gemini AI pre- & post-cleaning reports  
✅ Data Quality Score before and after cleaning  
✅ Download cleaned CSV and PDF report  
✅ User-friendly Streamlit UI  

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend / UI** | Streamlit |
| **Backend** | Python |
| **AI Engine** | Google Gemini API |
| **Data Processing** | Pandas, NumPy |
| **PDF Report** | ReportLab |

---

## 🗂️ Folder Structure
 smart-data-cleaner
├── app.py
├── requirements.txt
├── .env # Your Gemini API key (Do NOT push this to GitHub)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone this repository
```bash
git clone https://github.com/your-username/smart-data-cleaner.git
cd smart-data-cleaner
