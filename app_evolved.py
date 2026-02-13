import streamlit as st
import csv
import os
import pandas as pd

st.set_page_config(page_title="Job Opportunity Portal", page_icon="💼", layout="wide")

# ================= LOAD COLLEGES FROM CSV =================
df_colleges = pd.read_csv("all_colleges_india.csv")

# ================= DEGREE LIST (50+) =================
degree_list = [
    "BTech","BE","BCA","MCA","Diploma","ITI","BSc","MSc","BCom","MCom",
    "BBA","MBA","BA","MA","MBBS","BDS","LLB","LLM","BEd","MEd",
    "Hotel Management","Aviation","Animation","Pharmacy","BPharm","MPharm",
    "BPT","MPT","BArch","MArch","BHM","BTTM","Biotechnology",
    "Microbiology","Data Science","Artificial Intelligence","Cyber Security",
    "Cloud Computing","Mechanical Engineering","Civil Engineering",
    "Electrical Engineering","Electronics Engineering","Chemical Engineering",
    "Aeronautical Engineering","Marine Engineering","Agriculture",
    "Forensic Science","Psychology","Sociology","Political Science",
    "Economics","Statistics","Mathematics","Physics","Chemistry",
    "Journalism","Mass Communication","Fine Arts","Fashion Designing"
]

# ================= JOB DATABASE (25+) =================
jobs = [
    ["Infosys","Software Trainee",["BTech","BE","BCA","MCA"],60,18,28,"https://www.infosys.com/careers"],
    ["TCS","Assistant System Engineer",["BTech","BE"],60,18,28,"https://www.tcs.com/careers"],
    ["Wipro","Project Engineer",["BTech","BE","Diploma"],60,18,27,"https://careers.wipro.com"],
    ["HCL","Graduate Engineer",["BTech","BE"],60,18,28,"https://www.hcltech.com/careers"],
    ["Accenture","Associate Software Engineer",["BTech","BE"],60,18,28,"https://www.accenture.com/careers"],
    ["Capgemini","Software Analyst",["BTech","BE","MCA"],60,18,28,"https://www.capgemini.com/careers"],
    ["Tech Mahindra","Software Engineer",["BTech","BE"],60,18,28,"https://careers.techmahindra.com"],
    ["Cognizant","Programmer Analyst",["BTech","BE","MCA"],60,18,28,"https://careers.cognizant.com"],
    ["IBM","Associate Developer",["BTech","BE"],65,18,28,"https://www.ibm.com/careers"],
    ["Amazon","Cloud Support Associate",["BTech","BE"],65,18,30,"https://www.amazon.jobs"],
    ["Google","Technical Associate",["BTech","BE"],70,18,30,"https://careers.google.com"],
    ["Flipkart","Software Developer",["BTech","BE"],60,18,28,"https://www.flipkartcareers.com"],
    ["SSC","CGL Officer",["Any"],55,18,32,"https://ssc.nic.in"],
    ["RRB","NTPC Graduate",["Any"],55,18,33,"https://www.rrbcdg.gov.in"],
    ["ISRO","Scientist Assistant",["BTech","BE"],65,21,30,"https://www.isro.gov.in/careers"],
    ["DRDO","Junior Research Fellow",["BTech","BE","MSc"],65,21,30,"https://www.drdo.gov.in/careers"],
    ["BEL","Trainee Engineer",["BTech","BE"],60,18,28,"https://bel-india.in"],
    ["HAL","Graduate Apprentice",["BTech","BE"],60,18,28,"https://hal-india.co.in"],
    ["L&T","Site Engineer",["BTech","BE"],60,18,30,"https://www.larsentoubro.com/careers"],
    ["Reliance","Graduate Engineer Trainee",["BTech","BE"],60,18,28,"https://careers.ril.com"],
    ["Adani Group","Engineer",["BTech","BE"],60,18,28,"https://careers.adani.com"],
    ["Tata Power","Engineer Trainee",["BTech","BE"],60,18,28,"https://www.tatapower.com/careers"],
    ["Mahindra","Graduate Engineer",["BTech","BE"],60,18,28,"https://www.mahindra.com/careers"],
    ["Bosch","Associate Engineer",["BTech","BE"],60,18,28,"https://www.bosch.in/careers"],
    ["Siemens","Technical Engineer",["BTech","BE"],60,18,28,"https://new.siemens.com/careers"]
]

# ================= SAVE APPLICATION =================
def save_application(name, age, degree, company, role):
    file_exists = os.path.isfile("applications.csv")
    with open("applications.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name","Age","Degree","Company","Role"])
        writer.writerow([name,age,degree,company,role])

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "form"

# ====================================================
# FORM PAGE
# ====================================================
if st.session_state.page == "form":

    st.title("💼 Job Opportunity Portal")

    with st.form("job_form"):

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *")
            age = st.number_input("Your Age *", min_value=0, max_value=100, step=1)

            state = st.selectbox("State *", sorted(df_colleges["State"].unique()))
            filtered_colleges = df_colleges[df_colleges["State"] == state]["College Name"].unique()
            college = st.selectbox("College *", sorted(filtered_colleges))

        with col2:
            degree = st.selectbox("Degree *", degree_list)
            tenth = st.number_input("10th Percentage *", 0.0, 100.0)
            twelfth = st.number_input("12th Percentage *", 0.0, 100.0)

            photo = st.file_uploader("Upload Photo (PDF only) *", type=["pdf"])
            certificate = st.file_uploader("Upload Degree Certificate (PDF only) *", type=["pdf"])

        submit = st.form_submit_button("🔍 Find Eligible Jobs")

    if submit:
        errors = []

        if not name.strip():
            errors.append("Full Name is required")
        if age < 18:
            errors.append("You must be at least 18 years old")
        if tenth == 0 or twelfth == 0:
            errors.append("10th and 12th percentages required")
        if photo is None:
            errors.append("Photo upload required (PDF only)")
        if certificate is None:
            errors.append("Degree certificate upload required (PDF only)")

        if errors:
            for e in errors:
                st.error(e)
        else:
            avg_percent = (tenth + twelfth) / 2
            eligible = []

            for company, role, deg_list, min_per, min_age, max_age, website in jobs:
                if (
                    (degree in deg_list or "Any" in deg_list)
                    and avg_percent >= min_per
                    and min_age <= age <= max_age
                ):
                    eligible.append([company, role, website])

            st.session_state.name = name
            st.session_state.age = age
            st.session_state.degree = degree
            st.session_state.eligible_jobs = eligible
            st.session_state.page = "result"
            st.rerun()

# ====================================================
# RESULT PAGE
# ====================================================
if st.session_state.page == "result":

    st.success(f"Welcome {st.session_state.name}! Age: {st.session_state.age}")

    if st.session_state.eligible_jobs:
        st.subheader("🎯 Jobs You Are Eligible For")

        for company, role, website in st.session_state.eligible_jobs:
            col1, col2 = st.columns([3,1])
            col1.write(f"**{company}** — {role}")
            col2.link_button("Apply Now", website)

    else:
        st.warning("No jobs matched your profile.")

    if st.button("🔙 Go Back"):
        st.session_state.page = "form"
        st.rerun()
