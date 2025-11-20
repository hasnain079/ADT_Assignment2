import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Required for Streamlit Cloud
import matplotlib.pyplot as plt

# --- 1. App Title ---
st.title("University Course Analytics Dashboard")

# --- 2. Load CSV Data ---
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(data.head())

    # --- 3. Total Visits per Course ---
    st.header("Total Visits per Course")
    visits_per_course = (
        data.groupby("courseCode")["visits_on_that_day"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    visits_per_course.plot(kind='bar', ax=ax)
    ax.set_title("Total Visits per Course")
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Total Visits")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # --- 4. Total Visits per Program ---
    st.header("Total Visits per Program")
    visits_per_program = data.groupby("Program")["visits_on_that_day"].sum()

    fig, ax = plt.subplots(figsize=(7, 5))
    visits_per_program.plot(kind='bar', ax=ax)
    ax.set_title("Total Visits per Program")
    ax.set_xlabel("Program")
    ax.set_ylabel("Total Visits")
    st.pyplot(fig)

    # --- 5. Unique Visitors per Department ---
    st.header("Unique Visitors per Department")
    unique_visitors = data.groupby("Department")["userName"].nunique()

    fig, ax = plt.subplots(figsize=(7, 5))
    unique_visitors.plot(kind='bar', ax=ax)
    ax.set_title("Unique Visitors per Department")
    ax.set_xlabel("Department")
    ax.set_ylabel("Unique Visitors")
    st.pyplot(fig)

    # --- 6. Visits Trend Over Time ---
    st.header("Visits Trend Over Time")
    data["visit_date"] = pd.to_datetime(data["visit_date"])
    visits_over_time = data.groupby("visit_date")["visits_on_that_day"].sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    visits_over_time.plot(kind='line', marker='o', ax=ax)
    ax.set_title("Visits Trend Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Visits")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("Please upload a CSV file to view the analysis.")
