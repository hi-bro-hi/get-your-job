import streamlit as st
from datetime import date
import csv
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Job Opportunity Portal",
    page_icon="💼",
    layout="wide"
)

# ---------------- COLLEGES ----------------
colleges_by_state = {
    "Tamil Nadu": [
        "Anna University", "IIT Madras", "NIT Trichy", "VIT Vellore",
        "SRM IST", "PSG College of Technology", "SSN College of Engineering",
        "Thiagarajar College of Engineering", "SASTRA University",
        "Amrita Vishwa Vidyapeetham"
    ],
    "Karnataka": [
        "IISc Bangalore", "NIT Surathkal", "RV College of Engineering",
        "BMS College of Engineering", "MS Ramaiah Institute of Technology",
        "PES University", "Christ University", "Jain University"
    ],
    "Kerala": [
        "IIT Palakkad", "NIT Calicut", "CUSAT",
        "College of Engineering Trivandrum",
        "Government Engineering College Thrissur",
        "TKM College of Engineering", "MEC Kochi"
    ]
}

# ---------------- JOB DATABASE ----------------
jobs = [
    ["Infosys", "Software Trainee", ["BTech", "BE", "BCA", "MCA"], 60, 18, 28],
    ["TCS", "Assistant System Engineer", ["BTech", "BE"], 60, 18, 28],
    ["Wipro", "Project Engineer", ["BTech", "BE", "Diploma"], 60, 18, 27],
    ["Accenture", "Associate Software Engineer", ["BTech", "BE", "MSc IT"], 65, 21, 28],
    ["ISRO", "Scientist/Engineer", ["BTech", "BE", "MTech"], 65, 21, 28],
    ["Infosys", "Data Science Trainee", ["BSc", "BTech"], 70, 21, 28],
    ["Cognizant", "Operations Executive", ["BSc", "BCom", "BA"], 55, 18, 25],
    ["Deloitte", "Audit Executive", ["BCom", "MCom"], 60, 21, 30],
    ["HDFC Bank", "Relationship Officer", ["BBA", "MBA"], 55, 21, 30],
    ["L&T", "Junior Technician", ["Diploma", "ITI"], 55, 18, 30],
    ["SSC", "CGL Officer", ["Any"], 55, 18, 32],
    ["RRB", "NTPC Graduate", ["Any"], 55, 18, 33]
]

# ---------------- SAVE APPLICATION ----------------
def save_application(name, age, degree, company, role):
    file_exists = os.path.isfile("applications.csv")

    with open("applications.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Age", "Degree", "Company", "Role"])
        writer.writerow([name, age, degree, company, role])

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "form"

# ============================================================
# 📝 FORM PAGE
# ============================================================
if st.session_state.page == "form":

    st.title("💼 Job Opportunity Portal")
    st.subheader("Fill your details to discover jobs you qualify for")

    today = date.today()

    with st.form("job_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *")
            dob = st.date_input("Date of Birth *")
            state = st.selectbox("State *", list(colleges_by_state.keys()))
            college = st.selectbox("College *", colleges_by_state[state])

        with col2:
            degree = st.selectbox(
                "Degree *",
                [
                    "BTech", "BE", "BCA", "MCA", "BSc", "BCom", "BBA", "BA",
                    "MBA", "MTech", "Diploma", "ITI", "MBBS", "BDS", "BPT",
                    "BSc Nursing", "PharmD", "LLB", "BArch", "BEd",
                    "Hotel Management", "Animation", "Journalism"
                ]
            )
            tenth = st.number_input("10th Percentage *", 0.0, 100.0)
            twelfth = st.number_input("12th Percentage *", 0.0, 100.0)
            photo = st.file_uploader("Upload Photo *", type=["jpg", "png"])
            certificate = st.file_uploader(
                "Upload Degree Certificate *",
                type=["jpg", "png", "pdf"]
            )

        submit = st.form_submit_button("🔍 Find Eligible Jobs")

    if submit:
        errors = []
        age = today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )

        if age < 18:
            errors.append("You must be at least 18 years old")
        if not name.strip():
            errors.append("Full Name is required")
        if tenth == 0 or twelfth == 0:
            errors.append("10th and 12th percentages are required")
        if photo is None:
            errors.append("Photo upload is required")
        if certificate is None:
            errors.append("Degree certificate upload is required")

        if errors:
            for e in errors:
                st.error(e)
        else:
            avg_percent = (tenth + twelfth) / 2
            eligible = []

            for company, role, deg_list, min_per, min_age, max_age in jobs:
                if (
                    (degree in deg_list or "Any" in deg_list)
                    and avg_percent >= min_per
                    and min_age <= age <= max_age
                ):
                    eligible.append([company, role])

            st.session_state.name = name
            st.session_state.age = age
            st.session_state.degree = degree
            st.session_state.eligible_jobs = eligible
            st.session_state.page = "result"
            st.rerun()

# ============================================================
# 📊 RESULTS PAGE
# ============================================================
if st.session_state.page == "result":

    st.success(
        f"Welcome {st.session_state.name}! Age: {st.session_state.age}"
    )

    if st.session_state.eligible_jobs:
        st.subheader("🎯 Jobs You Are Eligible For")

        for company, role in st.session_state.eligible_jobs:
            col1, col2 = st.columns([3, 1])
            col1.write(f"**{company}** — {role}")

            if col2.button("Apply Now", key=f"{company}_{role}"):
                save_application(
                    st.session_state.name,
                    st.session_state.age,
                    st.session_state.degree,
                    company,
                    role
                )
                st.success(f"Applied to {company} for {role}!")

    else:
        st.warning("No jobs matched your profile.")

    if st.button("🔙 Go Back"):
        st.session_state.page = "form"
        st.rerun()
