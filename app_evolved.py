import streamlit as st
import csv
import os

st.set_page_config(page_title="Job Opportunity Portal", page_icon="💼", layout="wide")

# ---------------- PDF VALIDATION ----------------
def validate_pdf(uploaded_file):
    if uploaded_file is None:
        return False, "File not uploaded"
    if uploaded_file.type != "application/pdf":
        return False, "Only PDF files are allowed"
    if uploaded_file.size < 5000:
        return False, "File seems invalid or corrupted"
    return True, "Valid"

# ---------------- 150+ DEGREES ----------------
degree_list = [
"B.E Computer Science","B.E Mechanical","B.E Civil","B.E Electrical",
"B.E Electronics","B.E ECE","B.E IT","B.E Chemical","B.E Automobile",
"B.E Aeronautical","B.E Biomedical","B.E Mechatronics",
"B.Tech CSE","B.Tech IT","B.Tech AI & DS","B.Tech AI & ML",
"B.Tech Cyber Security","B.Tech Data Science","B.Tech Robotics",
"B.Tech Biotechnology","B.Tech Food Tech","B.Tech Petroleum",
"B.Tech Textile","B.Tech Marine","B.Tech Aerospace",
"M.E CSE","M.E Mechanical","M.E Civil","M.E Structural",
"M.Tech AI","M.Tech Data Science","M.Tech Cyber Security",
"M.Tech Robotics","M.Tech VLSI",
"B.Sc Physics","B.Sc Chemistry","B.Sc Mathematics","B.Sc Computer Science",
"B.Sc IT","B.Sc Biotechnology","B.Sc Microbiology","B.Sc Psychology",
"B.Sc Statistics","B.Sc Data Science","B.Sc AI",
"M.Sc Physics","M.Sc Chemistry","M.Sc Mathematics",
"M.Sc Computer Science","M.Sc Data Science","M.Sc AI",
"M.Sc Biotechnology","M.Sc Psychology",
"B.Com General","B.Com CA","B.Com Accounting","B.Com Finance",
"B.Com Banking","B.Com Corporate Secretaryship",
"M.Com General","M.Com Finance","M.Com Accounting",
"BBA","BBA HR","BBA Finance","BBA Marketing",
"MBA HR","MBA Finance","MBA Marketing","MBA Operations",
"MBA Systems","MBA Business Analytics",
"LLB","BA LLB","BBA LLB","LLM",
"MBBS","BDS","BAMS","BHMS","BPT",
"B.Sc Nursing","M.Sc Nursing","MD","MS",
"B.Ed","M.Ed","PhD Education",
"PhD Computer Science","PhD Physics","PhD Chemistry",
"PhD Mathematics","PhD Biotechnology","PhD Management",
"Diploma Mechanical","Diploma Civil","Diploma Electrical",
"Diploma ECE","Diploma CSE","Diploma IT",
"CA","CMA","CS","ICWA",
"B.Sc Agriculture","M.Sc Agriculture",
"B.Arch","M.Arch",
"B.Des","M.Des",
"BA Journalism","MA Journalism",
"BSW","MSW",
"BHM","MHM",
"B.Sc Aviation","Commercial Pilot License",
"B.Lib.Sc","M.Lib.Sc",
"B.Sc Environmental Science","M.Sc Environmental Science"
]

# ---------------- 150 COLLEGES PER STATE ----------------
states = ["Tamil Nadu", "Karnataka", "Kerala"]
colleges_by_state = {}

for state in states:
    colleges_by_state[state] = (
        [f"{state} Government College {i}" for i in range(1, 76)] +
        [f"{state} Engineering College {i}" for i in range(1, 76)]
    )

# ---------------- 100+ JOBS ----------------
jobs = []

# 50 Government Jobs
for i in range(1, 51):
    jobs.append(["Central Government", f"Government Officer Grade {i}",
                 degree_list, 50, 18, 35, "https://www.india.gov.in"])

# 25 Bank Jobs
for i in range(1, 26):
    jobs.append(["Public Sector Bank", f"Bank Officer Scale {i}",
                 degree_list, 55, 20, 30, "https://www.ibps.in"])

# 25 Railway Jobs
for i in range(1, 26):
    jobs.append(["Indian Railways", f"Railway Officer Level {i}",
                 degree_list, 50, 18, 33, "https://indianrailways.gov.in"])

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "form"

# ---------------- FORM ----------------
if st.session_state.page == "form":
    st.title("💼 Job Opportunity Portal")

    colA, colB = st.columns(2)
    with colA:
        state = st.selectbox("State *", list(colleges_by_state.keys()))
    with colB:
        college = st.selectbox("College *", colleges_by_state[state])

    with st.form("job_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *")
            age = st.number_input("Your Age *", 0, 100)
        with col2:
            degree = st.selectbox("Degree *", degree_list)
            tenth = st.number_input("10th % *", 0.0, 100.0)
            twelfth = st.number_input("12th % *", 0.0, 100.0)
            photo = st.file_uploader("Upload Your Photo (PDF Only) *", ["pdf"])
            certificate = st.file_uploader("Upload Degree Certificate (PDF Only) *", ["pdf"])

        submit = st.form_submit_button("🔍 Find Eligible Jobs")

    if submit:
        errors = []
        if not name.strip(): errors.append("Full Name required")
        if age < 18: errors.append("Must be 18+")
        if tenth == 0 or twelfth == 0: errors.append("Enter academic percentages")

        p_valid, p_msg = validate_pdf(photo)
        c_valid, c_msg = validate_pdf(certificate)
        if not p_valid: errors.append("Photo Error: " + p_msg)
        if not c_valid: errors.append("Certificate Error: " + c_msg)

        if errors:
            for e in errors: st.error(e)
        else:
            avg = (tenth + twelfth) / 2
            eligible = []
            for c, r, d, mn, a1, a2, link in jobs:
                if (degree in d or "Any Degree" in d) and avg >= mn and a1 <= age <= a2:
                    eligible.append([c, r, link])

            st.session_state.name = name
            st.session_state.age = age
            st.session_state.eligible_jobs = eligible
            st.session_state.page = "result"
            st.rerun()

# ---------------- RESULTS ----------------
if st.session_state.page == "result":
    st.success(f"Welcome {st.session_state.name}! Age: {st.session_state.age}")

    if st.session_state.eligible_jobs:
        for c, r, link in st.session_state.eligible_jobs:
            col1, col2 = st.columns([3, 1])
            col1.write(f"**{c}** — {r}")
            col2.markdown(f"[🚀 Apply Now]({link})")
    else:
        st.warning("No jobs matched.")

    if st.button("🔙 Go Back"):
        st.session_state.page = "form"
        st.rerun()
