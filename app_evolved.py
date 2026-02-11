import streamlit as st
from datetime import date
import pandas as pd

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Job Opportunity Portal",
    page_icon="💼",
    layout="wide"
)

# ---------------- Colleges by State ----------------
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

# ---------------- Jobs (UNCHANGED) ----------------
jobs = [
    ["Infosys", "Software Trainee", ["BTech", "BE"], 60, 18, 28],
    ["TCS", "Assistant System Engineer", ["BTech", "BE"], 60, 18, 28],
    ["Wipro", "Project Engineer", ["BTech", "BE"], 60, 18, 27],
    ["Accenture", "Associate Software Engineer", ["BTech", "BE"], 65, 21, 28],
    ["ISRO", "Scientist/Engineer", ["BTech", "BE"], 65, 21, 28],
    ["TCS", "Data Analyst Intern", ["BSc", "BTech"], 65, 21, 26],
    ["Infosys", "Data Science Trainee", ["BSc", "BTech"], 70, 21, 28],
    ["Infosys", "Junior Developer", ["BCA", "MCA"], 60, 18, 28],
    ["Wipro", "System Support Engineer", ["BCA", "MCA"], 55, 18, 27],
    ["Cognizant", "Operations Executive", ["BSc"], 55, 18, 25],
    ["Infosys", "BSc IT Trainee", ["BSc"], 60, 18, 26],
    ["Deloitte", "Audit Executive", ["BCom"], 60, 21, 30],
    ["KPMG", "Accounts Associate", ["BCom"], 58, 21, 30],
    ["HDFC Bank", "Relationship Officer", ["BBA", "MBA"], 55, 21, 30],
    ["ICICI Bank", "Management Trainee", ["MBA"], 60, 21, 30],
    ["Digital Marketing Firm", "Content Analyst", ["BA"], 55, 18, 28],
    ["Media House", "Junior Editor", ["BA"], 55, 21, 30],
    ["L&T", "Junior Technician", ["Diploma"], 55, 18, 30],
    ["TVS Motors", "Service Technician", ["Diploma"], 55, 18, 28],
    ["Banking Exam", "Clerk", ["Any"], 55, 20, 30],
    ["Banking Exam", "Probationary Officer", ["Any"], 60, 21, 30],
    ["SSC", "CGL Officer", ["Any"], 55, 18, 32],
    ["RRB", "NTPC Graduate", ["Any"], 55, 18, 33],
    ["Apollo Hospitals", "Junior Doctor", ["MBBS"], 60, 23, 35],
    ["Fortis Hospitals", "Resident Doctor", ["MBBS", "MDS"], 65, 25, 40],
    ["Dental Clinic", "Dental Intern", ["BDS"], 60, 22, 35],
    ["Dental Clinic", "Dental Surgeon", ["MDS"], 65, 25, 40],
    ["Physiotherapy Center", "Physiotherapist", ["BPT"], 60, 22, 35],
    ["Pharmacy Corp", "Pharmacist", ["PharmD"], 60, 22, 35],
    ["Hospital Nursing", "Staff Nurse", ["BSc Nursing"], 60, 20, 35],
    ["Medical Research Lab", "Research Assistant", ["MBBS", "BSc Nursing", "BPT", "PharmD"], 65, 22, 35]
]

# ---------------- Session State ----------------
if "page" not in st.session_state:
    st.session_state.page = "form"

# ---------------- Page 1: Form (UNCHANGED) ----------------
if st.session_state.page == "form":

    st.title("Job Opportunity Portal")
    st.subheader("Enter your details to find eligible jobs")

    today = date.today()
    max_dob = date(today.year - 18, today.month, today.day)

    with st.form("job_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *")
            dob = st.date_input("Date of Birth *", max_value=max_dob)
            state = st.selectbox("State *", list(colleges_by_state.keys()))
            college = st.selectbox("College *", colleges_by_state[state])

        with col2:
            degree = st.selectbox(
                "Degree *",
                [
                    "BTech", "BE", "B.E. (Civil)", "B.E. (Mechanical)", "B.Tech (CS)",
                    "BSc", "BSc (Physics)", "BSc (Chemistry)", "BSc (Maths)",
                    "BCA", "BCom", "BCom (Hons)", "BCom (Finance)", "BBA",
                    "BA", "BA (English)", "BA (Economics)", "BA (History)",
                    "MBA", "MCA", "MCom",
                    "MBBS", "BDS", "MDS", "BPT", "BSc Nursing", "PharmD",
                    "Diploma", "LLB", "BArch"
                ]
            )
            tenth = st.number_input("10th Percentage *", 0.0, 100.0)
            twelfth = st.number_input("12th Percentage *", 0.0, 100.0)
            photo = st.file_uploader("Upload Photo *", type=["jpg", "png"])
            certificate = st.file_uploader("Upload Degree Certificate *", type=["jpg", "png", "pdf"])

        submit = st.form_submit_button("Find Eligible Jobs")

    if submit:
        errors = []
        if not name.strip(): errors.append("Full Name is required")
        if tenth == 0 or twelfth == 0: errors.append("10th and 12th percentages are required")
        if photo is None: errors.append("Photo upload is required")
        if certificate is None: errors.append("Degree certificate upload is required")

        if errors:
            for e in errors: st.error(e)
        else:
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            avg_percent = (tenth + twelfth) / 2
            eligible = []

            for job in jobs:
                company, role, deg_list, min_per, min_age, max_age = job
                if degree in deg_list and avg_percent >= min_per and min_age <= age <= max_age:
                    eligible.append([company, role, min_per, f"{min_age}-{max_age}"])

            if eligible:
                for job in jobs:
                    company, role, deg_list, min_per, min_age, max_age = job
                    if "Any" in deg_list and avg_percent >= min_per and min_age <= age <= max_age:
                        row = [company, role, min_per, f"{min_age}-{max_age}"]
                        if row not in eligible:
                            eligible.append(row)

            st.session_state.name = name
            st.session_state.age = age
            st.session_state.eligible_jobs = eligible
            st.session_state.page = "result"
            st.rerun()

# ---------------- Page 2: Results ----------------
elif st.session_state.page == "result":

    st.title("Eligible Job Results")
    st.success(f"Hello {st.session_state.name}, Age: {st.session_state.age}")

    if st.session_state.eligible_jobs:
        df = pd.DataFrame(st.session_state.eligible_jobs,
                          columns=["Company", "Role", "Min % Required", "Age Limit"])
        st.dataframe(df, use_container_width=True)
        st.info(f"Total eligible jobs found: {len(st.session_state.eligible_jobs)}")
    else:
        st.warning("No jobs found matching your eligibility")

    # ---------------- Live Interview Updates (Streamlit-safe) ----------------
    st.subheader("🔴 Live Interview Updates")

    @st.cache_data(show_spinner=False)
    def load_interview_data():
        return pd.read_csv("interviews.csv")

    try:
        interviews = load_interview_data()
        st.dataframe(interviews, use_container_width=True)
        st.caption("Click button to check for latest interview updates")

        if st.button("🔄 Check for Interview Updates"):
            load_interview_data.clear()
            st.rerun()

    except FileNotFoundError:
        st.error("Interview data file not found")

    if st.button("Go Back"):
        st.session_state.page = "form"
        st.rerun()
