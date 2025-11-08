import streamlit as st
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import google.generativeai as genai
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ================================
# Load Environment & Configure Gemini
# ================================
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ================================
# Streamlit App Setup
# ================================
st.set_page_config(page_title="Smart Data Cleaner", layout="wide")
st.title("Smart Data Cleaner – AI-Powered Data Cleaning & Quality Analyzer")
st.caption("Upload → Clean → Analyze → Download ")

# ================================
# File Upload
# ================================
uploaded_file = st.file_uploader("📂 Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

    st.subheader("📊 Original Data Preview")
    st.dataframe(df.head())

    # ===================================
    # Data Quality BEFORE Cleaning
    # ===================================
    total_cells = df.size
    missing_cells = df.isnull().sum().sum()
    before_quality = 100 * (1 - missing_cells / total_cells)
    st.metric("🧮 Data Quality (Before Cleaning)", f"{before_quality:.2f}%")

    # ===================================
    # AI Analysis Before Cleaning
    # ===================================
    buffer = []
    buffer.append(f"Shape: {df.shape}")
    buffer.append(f"Columns: {list(df.columns)}")
    buffer.append("Missing Values:\n" + str(df.isnull().sum()))
    buffer.append("Data Types:\n" + str(df.dtypes))
    summary_text = "\n\n".join(buffer)

    with st.spinner("🤖 Analyzing dataset with Gemini AI..."):
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"""
        You are a data cleaning assistant.
        Dataset Summary:
        {summary_text}

        Identify issues (missing values, duplicates, wrong types, etc.)
        and suggest how to fix them clearly and shortly.
        """
        ai_analysis = model.generate_content(prompt).text

    st.subheader("🧠 Gemini AI Analysis & Suggestions")
    st.write(ai_analysis)
    st.divider()

    # ===================================
    # SMART DATA CLEANING
    # ===================================
    st.subheader("🩺 Cleaning Data...")

    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()
    df = df.replace(r"^\s*$", np.nan, regex=True)

    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass
        if df[col].dtype in ["int64", "float64"]:
            df[col].fillna(df[col].median(), inplace=True)
        else:
            df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown", inplace=True)

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    for col in numeric_cols:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        df[col] = np.where((df[col] < lower) | (df[col] > upper), df[col].median(), df[col])

    df = df.convert_dtypes()
    df = df.dropna(axis=1, how="all")
    df = df.loc[:, (df != "").any(axis=0)]

    st.success("✅ Data Cleaned Successfully!")
    st.subheader("🧼 Cleaned Data Preview")
    st.dataframe(df.head())
    st.divider()

    # ===================================
    # Data Quality AFTER Cleaning
    # ===================================
    total_cells_after = df.size
    missing_cells_after = df.isnull().sum().sum()
    after_quality = 100 * (1 - missing_cells_after / total_cells_after)

    improvement = after_quality - before_quality

    col1, col2, col3 = st.columns(3)
    col1.metric("🧮 Before Cleaning", f"{before_quality:.2f}%")
    col2.metric("🧼 After Cleaning", f"{after_quality:.2f}%")
    col3.metric("📈 Improvement", f"{improvement:.2f}%")

    st.divider()

    # ===================================
    # AI Cleaning Summary
    # ===================================
    with st.spinner("🧠 Generating AI Cleaning Summary..."):
        post_prompt = f"""
        The dataset has been cleaned successfully.
        Original Quality: {before_quality:.2f}%
        Improved Quality: {after_quality:.2f}%
        Columns: {list(df.columns)}

        Summarize the cleaning improvements in human-readable language.
        """
        ai_report = model.generate_content(post_prompt).text

    st.subheader("📈 Gemini AI Cleaning Summary Report")
    st.write(ai_report)

    # ===================================
    # Generate PDF Report
    # ===================================
    st.subheader("📄 Download AI Cleaning Report (PDF)")

    def generate_pdf_report(ai_report, before_quality, after_quality, improvement, df):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(180, height - 60, "AI Data Cleaning Summary Report")

        c.setFont("Helvetica", 11)
        c.drawString(40, height - 100, f"Total Rows: {df.shape[0]}")
        c.drawString(200, height - 100, f"Total Columns: {df.shape[1]}")

        c.drawString(40, height - 130, f"Data Quality Before: {before_quality:.2f}%")
        c.drawString(250, height - 130, f"Data Quality After: {after_quality:.2f}%")
        c.drawString(450, height - 130, f"Improvement: {improvement:.2f}%")

        text_obj = c.beginText(40, height - 180)
        text_obj.setFont("Helvetica", 10)
        for line in ai_report.split("\n"):
            text_obj.textLine(line)
        c.drawText(text_obj)
        c.save()
        buffer.seek(0)
        return buffer

    pdf_report = generate_pdf_report(ai_report, before_quality, after_quality, improvement, df)

    st.download_button(
        label="⬇️ Download PDF Report",
        data=pdf_report,
        file_name="AI_Data_Cleaning_Report.pdf",
        mime="application/pdf"
    )

    # ===================================
    # Download Cleaned Data
    # ===================================
    cleaned_csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Cleaned CSV",
        data=cleaned_csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

else:
    st.info("📥 Please upload a CSV or Excel file to start cleaning your dataset.")
