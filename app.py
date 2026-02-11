import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Command Centre", layout="wide")

st.title("🎓 Student Command Centre")

st.header("📘 Academic Marks")

subjects = ["Maths", "English","Python", "HTML", "OS"]

attendance = {}
marks = {}

for sub in subjects:
    col1, col2 = st.columns(2)
    with col1:
        attendance[sub] = st.number_input(
            f"{sub} Attendance (%)",
            min_value=0,
            max_value=100,
            value=50,
            key=f"att_{sub}"
        )
    with col2:
        marks[sub] = st.number_input(
            f"{sub} Internal Marks",
            min_value=0,
            max_value=50,
            value=0,
            key=f"mark_{sub}"
        )

df = pd.DataFrame({
    "Subject": subjects,
    "Attendance (%)": [attendance[s] for s in subjects],
    "Internal Marks": [marks[s] for s in subjects]
})

st.subheader("📊 Academic Data")
st.dataframe(df)

import os

st.header("📝 Task Manager")

TASK_FILE = "data/tasks.csv"

# Load tasks
if os.path.exists(TASK_FILE):
    task_df = pd.read_csv(TASK_FILE, parse_dates=["Deadline"])
else:
    task_df = pd.DataFrame(columns=["Task", "Deadline", "Status"])

# Input
task_name = st.text_input("Task Name")
task_deadline = st.date_input("Deadline")

if st.button("Add Task"):
    new_task = pd.DataFrame([{
        "Task": task_name,
        "Deadline": task_deadline,
        "Status": "Pending"
    }])
    task_df = pd.concat([task_df, new_task], ignore_index=True)
    task_df.to_csv(TASK_FILE, index=False)

# Convert & sort
if not task_df.empty:
    task_df["Deadline"] = pd.to_datetime(task_df["Deadline"])
    task_df["Days Left"] = (task_df["Deadline"] - pd.Timestamp.today()).dt.days
    task_df = task_df.sort_values("Days Left")

# Mark complete
st.subheader("📌 Pending Tasks")
pending = task_df[task_df["Status"] == "Pending"]

for i, row in pending.iterrows():
    if st.checkbox(f"{row['Task']} (Due in {row['Days Left']} days)", key=f"task_{i}"):
        task_df.at[i, "Status"] = "Completed"
        task_df.to_csv(TASK_FILE, index=False)

# View completed
if st.button("View Completed Tasks"):
    st.subheader("✅ Completed Tasks")
    st.dataframe(task_df[task_df["Status"] == "Completed"])

COURSE_FILE = "data/courses.csv"

# Load courses
if os.path.exists(COURSE_FILE):
    course_df = pd.read_csv(COURSE_FILE)
else:
    course_df = pd.DataFrame(columns=["Course", "Platform", "Progress", "Status"])

st.header("📚 Self-Paced Courses Tracker")

course_name = st.text_input("Course Name")

platform_choice = st.selectbox("Platform", ["NPTEL", "Coursera", "Udemy", "Other"])
platform = st.text_input("Website Name") if platform_choice == "Other" else platform_choice

progress = st.slider("Completion (%)", 0, 100, 0)

if st.button("Add Course"):
    status = "Completed" if progress == 100 else "In Progress"
    new_course = pd.DataFrame([{
        "Course": course_name,
        "Platform": platform,
        "Progress": progress,
        "Status": status
    }])
    course_df = pd.concat([course_df, new_course], ignore_index=True)
    course_df.to_csv(COURSE_FILE, index=False)

# Show active courses
st.subheader("📈 Ongoing Courses")
st.dataframe(course_df[course_df["Status"] != "Completed"])

# View completed
if st.button("View Completed Courses"):
    st.subheader("🎓 Completed Courses")
    st.dataframe(course_df[course_df["Status"] == "Completed"])
st.header("⚠️ Data Privacy")

if st.button("Delete All Personal Information"):
    if os.path.exists(TASK_FILE):
        os.remove(TASK_FILE)
    if os.path.exists(COURSE_FILE):
        os.remove(COURSE_FILE)

    st.success("All personal data has been deleted. Restart the app.")
