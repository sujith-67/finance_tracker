import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💰 Personal Finance Analysis Dashboard")
st.write("App is running ✅")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("./data.csv")

st.subheader("📄 Dataset Preview")
st.write(df)

# ---------------- BASIC STATS ----------------
st.subheader("📊 Overview")

avg_income = df['monthly_income_usd'].mean()
avg_expense = df['monthly_expenses_usd'].mean()
avg_savings = df['savings_usd'].mean()

st.write(f"Average Income: ${round(avg_income,2)}")
st.write(f"Average Expense: ${round(avg_expense,2)}")
st.write(f"Average Savings: ${round(avg_savings,2)}")

# ---------------- BAR CHART ----------------
st.subheader("📊 Income vs Expenses")

sample = df.head(10)

fig, ax = plt.subplots()
ax.bar(sample['user_id'], sample['monthly_income_usd'], label="Income")
ax.bar(sample['user_id'], sample['monthly_expenses_usd'], label="Expense")

ax.legend()
st.pyplot(fig)

# ---------------- SAVINGS DISTRIBUTION ----------------
st.subheader("💰 Savings Distribution")

fig2, ax2 = plt.subplots()
ax2.hist(df['savings_usd'], bins=10)

st.pyplot(fig2)

# ---------------- LOAN ANALYSIS ----------------
st.subheader("🏦 Loan Analysis")

loan_counts = df['has_loan'].value_counts()

st.write(loan_counts)

fig3, ax3 = plt.subplots()
ax3.pie(loan_counts, labels=loan_counts.index, autopct='%1.1f%%')

st.pyplot(fig3)
