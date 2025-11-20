import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("University Course Analytics Dashboard")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    # Load CSV
    data = pd.read_csv(uploaded_file)

    # Fix truncated visits column
    data = data.rename(columns={"visits_on_that_d": "visits_on_that_day"})
    data["visit_date"] = pd.to_datetime(data["visit_date"])

    st.subheader("Data Preview")
    st.write(data.head())

    # ========== A. Total Visits per Course ==========
    st.header("A. Total Visits per Course")
    q_a = data.groupby(["courseCode", "CourseTitle"])["visits_on_that_day"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(q_a["courseCode"], q_a["visits_on_that_day"])
    ax.set_title("Total Course Visits")
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Total Visits")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.write(q_a)

    # ========== B. Total Visits per Course by Program ==========
    st.header("B. Total Visits per Course by Program")
    q_b = data.groupby(["Program", "courseCode"])["visits_on_that_day"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10,4))
    for program in q_b["Program"].unique():
        subset = q_b[q_b["Program"] == program]
        ax.bar(subset["courseCode"], subset["visits_on_that_day"], label=program)
    ax.set_title("Visits per Course by Program")
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Total Visits")
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)
    st.write(q_b)

    # ========== C. Total Users per Program ==========
    st.header("C. Total Users per Program")
    q_c = data.groupby("Program")["userName"].nunique().reset_index(name="total_users")

    fig, ax = plt.subplots(figsize=(7,4))
    ax.bar(q_c["Program"], q_c["total_users"])
    ax.set_title("Users per Program")
    ax.set_xlabel("Program")
    ax.set_ylabel("Total Users")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.write(q_c)

    # ========== D. Unique Visitors per Department by Program ==========
    st.header("D. Unique Visitors per Department by Program")
    q_d = data.groupby(["Department", "Program"])["userName"].nunique().reset_index(name="unique_visitors")
    st.write(q_d)

    # Visual
    fig, ax = plt.subplots(figsize=(10,5))
    for dept in q_d["Department"].unique():
        subset = q_d[q_d["Department"] == dept]
        ax.bar(subset["Program"], subset["unique_visitors"], label=dept)
    ax.set_title("Unique Visitors per Department by Program")
    ax.set_xlabel("Program")
    ax.set_ylabel("Unique Visitors")
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

    # ========== E. Most Recent Visit ==========
    st.header("E. Most Recent Visit per User per Course")
    q_e = data.groupby(["userName", "courseCode"])["visit_date"].max().reset_index(name="last_visit_date")
    st.write(q_e)

    # ========== F. Visit Count per User per Course ==========
    st.header("F. Visit Count per User per Course")
    q_f = data.groupby(["userName", "courseCode"])["visits_on_that_day"].sum().reset_index(name="visit_count")
    st.write(q_f)

    # Visual
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(q_f["courseCode"], q_f["visit_count"])
    ax.set_title("Visits per User per Course (Aggregated)")
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Visit Count")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ========== G. Top Visitor Per Course ==========
    st.header("G. User Who Visited Each Course the Most")
    q_g = q_f.sort_values(["courseCode", "visit_count"], ascending=[True, False])
    top_g = q_g.groupby("courseCode").head(1)
    st.write(top_g)

    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(top_g["courseCode"], top_g["visit_count"])
    ax.set_title("Top Visitor Count per Course")
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Max Visits")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ========== H. User with Most Visits in a Single Day ==========
    st.header("H. Most Visits in a Single Day per Course")
    q_h = data.groupby(["courseCode", "userName", "visit_date"])["visits_on_that_day"].sum().reset_index(name="daily_visits")
    top_h = q_h.sort_values(["courseCode", "daily_visits"], ascending=[True, False]).groupby("courseCode").head(1)
    st.write(top_h)

    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(top_h["courseCode"], top_h["daily_visits"])
    ax.set_title("Highest Daily Visits per Course")
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Daily Visit Count")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ========== I. Longest Streak ==========
    st.header("I. Longest Visit Streak per User per Course")

    data_sorted = data.sort_values(["userName", "courseCode", "visit_date"])
    data_sorted["day_diff"] = data_sorted.groupby(["userName", "courseCode"])["visit_date"].diff().dt.days
    data_sorted["streak_group"] = data_sorted["day_diff"].ne(1).cumsum()
    streaks = data_sorted.groupby(["userName", "courseCode", "streak_group"]).size().reset_index(name="streak_length")
    top_streaks = streaks.sort_values("streak_length", ascending=False).groupby(["userName", "courseCode"]).head(1)
    st.write(top_streaks)

    # Visual
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(top_streaks["courseCode"], top_streaks["streak_length"])
    ax.set_title("Longest Visit Streak per Course")
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Streak Length")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ========== J. Longest Gap ==========
    st.header("J. Longest Gap Between Visits per User per Course")
    data_sorted["prev_date"] = data_sorted.groupby(["userName", "courseCode"])["visit_date"].shift()
    data_sorted["gap_days"] = (data_sorted["visit_date"] - data_sorted["prev_date"]).dt.days
    q_j = data_sorted.groupby(["userName", "courseCode"])["gap_days"].max().reset_index(name="longest_gap_days")
    st.write(q_j)

    # Graph: longest gaps
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(q_j["courseCode"], q_j["longest_gap_days"])
    ax.set_title("Longest Gap Between Visits per Course")
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Gap (Days)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ========== K. Most Unique Courses in 3 Days ==========
    st.header("K. Users Visiting Most Unique Courses within 3 Days")

    q_k = data.groupby("userName").agg(
        unique_courses=("courseCode", "nunique"),
        start_date=("visit_date", "min"),
        end_date=("visit_date", "max")
    ).reset_index()

    q_k["duration_days"] = (q_k["end_date"] - q_k["start_date"]).dt.days
    top_k = q_k[q_k["duration_days"] <= 3].sort_values("unique_courses", ascending=False)

    st.write(top_k)

    # Graph
    fig, ax = plt.subplots(figsize=(10,4))
    ax.bar(top_k["userName"], top_k["unique_courses"])
    ax.set_title("Unique Courses Visited Within 3 Days")
    ax.set_xlabel("User")
    ax.set_ylabel("Unique Courses")
    plt.xticks(rotation=60)
    st.pyplot(fig)
