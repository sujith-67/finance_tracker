import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Finance Dashboard", layout="wide")

# ---------------- TITLE ----------------
st.title("💰 Personal Finance Dashboard")
st.markdown("### 📊 Analyze income, expenses & savings easily")

# ---------------- LOAD DATA ----------------
try:
    df = pd.read_csv("./data.csv")
except:
    st.error("❌ Error loading data.csv")
    st.stop()

# ---------------- SIDEBAR FILTER ----------------
st.sidebar.title("📌 Filters")

if 'gender' in df.columns:
    selected_gender = st.sidebar.selectbox(
        "Select Gender",
        ["All"] + list(df['gender'].dropna().unique())
    )

    if selected_gender != "All":
        df = df[df['gender'] == selected_gender]

# ---------------- KPI CARDS ----------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

avg_income = df['monthly_income_usd'].mean()
avg_expense = df['monthly_expenses_usd'].mean()
avg_savings = df['savings_usd'].mean()

col1.metric("💰 Avg Income", f"${round(avg_income,2)}")
col2.metric("💸 Avg Expense", f"${round(avg_expense,2)}")
col3.metric("🏦 Avg Savings", f"${round(avg_savings,2)}")

# ---------------- DATA TABLE ----------------
st.subheader("📄 Dataset Preview")
st.write(df)

# ---------------- CHARTS ----------------
st.subheader("📈 Visual Analysis")

col1, col2 = st.columns(2)

# Income vs Expense
with col1:
    st.write("Income vs Expense (Sample)")
    sample = df.head(10)

    fig, ax = plt.subplots()
    ax.bar(sample['user_id'], sample['monthly_income_usd'], label="Income")
    ax.bar(sample['user_id'], sample['monthly_expenses_usd'], label="Expense")
    ax.legend()

    st.pyplot(fig)

# Savings distribution
with col2:
    st.write("Savings Distribution")

    fig2, ax2 = plt.subplots()
    ax2.hist(df['savings_usd'], bins=10)

    st.pyplot(fig2)

# ---------------- LOAN ANALYSIS ----------------
st.subheader("🏦 Loan Analysis")

loan_counts = df['has_loan'].value_counts()

col1, col2 = st.columns(2)

with col1:
    st.write(loan_counts)

with col2:
    fig3, ax3 = plt.subplots()
    ax3.pie(loan_counts, labels=loan_counts.index, autopct='%1.1f%%')
    st.pyplot(fig3)
    # ---------------- AI INSIGHTS ----------------
st.subheader("🤖 AI Insights")

insights = []

# Insight 1: Income vs Expense
if avg_expense > avg_income:
    insights.append("⚠️ People are spending more than they earn.")
else:
    insights.append("✅ Income is generally higher than expenses.")

# Insight 2: Savings health
if avg_savings < 0.2 * avg_income:
    insights.append("💡 Savings are quite low compared to income.")
else:
    insights.append("💰 Savings levels are healthy.")

# Insight 3: Loan impact
if 'has_loan' in df.columns:
    loan_group = df.groupby('has_loan')['savings_usd'].mean()

    if True in loan_group and False in loan_group:
        if loan_group[True] < loan_group[False]:
            insights.append("🏦 People with loans tend to save less.")
        else:
            insights.append("📊 Loan status does not significantly affect savings.")

# Insight 4: Income vs Savings trend
if df['monthly_income_usd'].corr(df['savings_usd']) > 0:
    insights.append("📈 Higher income generally leads to higher savings.")
else:
    insights.append("📉 Income does not strongly impact savings.")

# Show insights
for i in insights:
    st.write(i)
  # ---------------- ML PREDICTION ----------------
from sklearn.linear_model import LinearRegression
import numpy as np

st.subheader("🔮 ML Prediction: Future Savings")

# Prepare data
X = df[['monthly_income_usd', 'monthly_expenses_usd']]
y = df['savings_usd']

# Train model
model = LinearRegression()
model.fit(X, y)

# User input
input_income = st.number_input("Monthly Income", value=5000)
input_expense = st.number_input("Monthly Expense", value=2000)

# Predict button
if st.button("Predict Savings"):

    prediction = model.predict([[input_income, input_expense]])

    # Make realistic
    prediction_value = max(0, min(prediction[0], input_income))

    st.success(f"Predicted Monthly Savings: ${round(prediction_value,2)}")