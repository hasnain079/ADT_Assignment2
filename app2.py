import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 University Course Analytics – Full Report (Queries a–k)")

uploaded_file = st.file_uploader("Upload merged CSV file", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    # Ensure date column is correctly parsed
    data['visit_date'] = pd.to_datetime(data['visit_date'])

    st.success("CSV Loaded Successfully!")
    st.dataframe(data.head())

    # ---------------------------
    # a. Total visits per course
    # ---------------------------
    st.header("a. Total number of times each course was visited")
    q_a = data.groupby(["courseCode", "title"])["visits_on_that_day"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(q_a["courseCode"], q_a["visits_on_that_day"])
    ax.set_title("Total Visits per Course")
    ax.set_xlabel("Course Code")
    ax.set_ylabel("Total Visits")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ---------------------------
    # b. Total visits per program per course
    # ---------------------------
    st.header("b. Total visits per course by program")
    q_b = data.groupby(["Program", "courseCode", "title"])["visits_on_that_day"].sum().reset_index()
    st.dataframe(q_b)

    # ---------------------------
    # c. Total number of users enrolled per program
    # ---------------------------
    st.header("c. Total number of students in each program")
    q_c = data.groupby("Program")["userName"].nunique().reset_index(name="total_users")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(q_c["Program"], q_c["total_users"])
    ax.set_title("Total Users per Program")
    st.pyplot(fig)

    # ---------------------------
    # d. Unique visitors per department by program
    # ---------------------------
    st.header("d. Unique visitors per department by program")
    q_d = data.groupby(["deptName", "Program"])["userName"].nunique().reset_index(name="unique_visitors")
    st.dataframe(q_d)

    # ---------------------------
    # e. Most recent visit date per user per course
    # ---------------------------
    st.header("e. Most recent visit date per user per course")
    q_e = data.groupby(["userName", "courseCode"])["visit_date"].max().reset_index()
    q_e = q_e.sort_values("visit_date", ascending=False)
    st.dataframe(q_e)

    # ---------------------------
    # f. Number of times each user visited each course
    # ---------------------------
    st.header("f. Visit count per user per course")
    q_f = data.groupby(["userName", "courseCode"])["visits_on_that_day"].sum().reset_index(name="visit_count")
    st.dataframe(q_f)

    # ---------------------------
    # g. User who visited each course the most
    # ---------------------------
    st.header("g. Top user for each course")
    q_g = q_f.sort_values(["courseCode", "visit_count"], ascending=[True, False]).groupby("courseCode").head(1)
    st.dataframe(q_g)

    # ---------------------------
    # h. User with highest visits in a single day per course
    # ---------------------------
    st.header("h. User with most visits in a single day (per course)")
    q_h = data.groupby(["courseCode", "userName", "visit_date"])["visits_on_that_day"].sum().reset_index(name="daily_visits")
    q_h = q_h.sort_values(["courseCode", "daily_visits"], ascending=[True, False]).groupby("courseCode").head(1)
    st.dataframe(q_h)

    # ---------------------------
    # i. Longest visit streak per user per course
    # ---------------------------
    st.header("i. Longest consecutive-day streak per user per course")

    streak_results = []
    for (user, course), group in data.groupby(["userName", "courseCode"]):
        days = sorted(group["visit_date"].unique())
        streak = longest = 1

        for i in range(1, len(days)):
            if (days[i] - days[i-1]).days == 1:
                streak += 1
                longest = max(longest, streak)
            else:
                streak = 1
        streak_results.append([user, course, longest])

    q_i = pd.DataFrame(streak_results, columns=["userName", "courseCode", "streak_length"])\
            .sort_values("streak_length", ascending=False)

    st.dataframe(q_i)

    # ---------------------------
    # j. Longest gap between visits per user per course
    # ---------------------------
    st.header("j. Longest gap between visits per user per course")

    gap_results = []
    for (user, course), group in data.groupby(["userName", "courseCode"]):
        dates = sorted(group["visit_date"].unique())
        gaps = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
        longest_gap = max(gaps) if gaps else 0
        gap_results.append([user, course, longest_gap])

    q_j = pd.DataFrame(gap_results, columns=["userName", "courseCode", "longest_gap_days"])\
            .sort_values("longest_gap_days", ascending=False)

    st.dataframe(q_j)

    # ---------------------------
    # k. User visiting most unique courses in 3 days
    # ---------------------------
    st.header("k. User who visited the most courses within 3 days")

    short_window_results = []
    for user, group in data.groupby("userName"):
        min_date, max_date = group["visit_date"].min(), group["visit_date"].max()
        if (max_date - min_date).days <= 3:
            unique_courses = group["courseCode"].nunique()
            short_window_results.append([user, unique_courses, min_date, max_date])

    q_k = pd.DataFrame(short_window_results,
                       columns=["userName", "unique_courses", "start_date", "end_date"])\
                       .sort_values("unique_courses", ascending=False)

    st.dataframe(q_k)
