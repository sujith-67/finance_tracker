import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- DEBUG ----------------
st.title("💰 Smart Finance Tracker")
st.write("App is running ✅")

# ---------------- LOAD DATA SAFELY ----------------
# ---------------- LOAD DATA SAFELY ----------------
try:
    df = pd.read_csv("./data.csv")

    # Convert column names to lowercase
    df.columns = df.columns.str.lower()

    # Rename columns to match our app
    df = df.rename(columns={
        "date": "date",
        "amount": "amount",
        "category": "category",
        "type": "type",
        "description": "tag"
    })

    # Convert date
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Create month column
    df['month'] = df['date'].dt.month

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()
# ---------------- ADD ENTRY ----------------
st.header("➕ Add New Entry")

date = st.date_input("Date")
amount = st.number_input("Amount")
category = st.selectbox("Category", ["Food","Transport","Shopping","Bills","Salary"])
type_ = st.selectbox("Type", ["Expense","Income"])
tag = st.text_input("Tag")

if st.button("Add Entry"):
    new_row = pd.DataFrame({
        "date":[date],
        "amount":[amount],
        "category":[category],
        "type":[type_],
        "tag":[tag]
    })
    
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("data.csv", index=False)
    st.success("Entry Added! Refresh to see changes.")

# ---------------- FILTER ----------------
st.sidebar.header("🔍 Filter")

selected_category = st.sidebar.selectbox(
    "Select Category", 
    ["All"] + list(df['category'].unique())
)

if selected_category != "All":
    filtered_df = df[df['category'] == selected_category]
else:
    filtered_df = df

st.subheader("📊 Filtered Data")
st.write(filtered_df)

# ---------------- MONTHLY ANALYSIS ----------------
st.subheader("📅 Monthly Analysis")

monthly = filtered_df.groupby("month")["amount"].sum()

if not monthly.empty:
    st.bar_chart(monthly)
else:
    st.warning("No data for selected filter")

# ---------------- PIE CHART ----------------
st.subheader("🥧 Category-wise Spending")

expense_df = filtered_df[filtered_df['type'] == "Expense"]
category_data = expense_df.groupby("category")["amount"].sum()

if not category_data.empty:
    fig, ax = plt.subplots()
    ax.pie(category_data, labels=category_data.index, autopct='%1.1f%%')
    st.pyplot(fig)
else:
    st.warning("No expense data")

# ---------------- INSIGHTS ----------------
st.subheader("🧠 Insights")

if not category_data.empty:
    max_category = category_data.idxmax()
    max_value = category_data.max()
    st.write(f"You spend the most on **{max_category}**: ₹{max_value}")
else:
    st.write("No insights available")

# ---------------- SAVINGS ----------------
st.subheader("💰 Savings")

income = filtered_df[filtered_df['type']=="Income"]["amount"].sum()
expense = filtered_df[filtered_df['type']=="Expense"]["amount"].sum()

st.write(f"Income: ₹{income}")
st.write(f"Expense: ₹{expense}")
st.write(f"Savings: ₹{income - expense}")

# ---------------- PREDICTION ----------------
st.subheader("🔮 Prediction")

if not expense_df.empty:
    avg_spend = expense_df["amount"].mean()
    st.write(f"Estimated next expense: ₹{round(avg_spend,2)}")
else:
    st.write("Not enough data for prediction")
