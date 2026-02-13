import streamlit as st
import pandas as pd
import csv
import os
import webbrowser

st.set_page_config(page_title="Job Opportunity Portal", page_icon="💼", layout="wide")

# ================= LOAD COLLEGES CSV =================
# Make sure you have all_colleges_india.csv in same folder
df = pd.read_csv("all_colleges_india.csv")

# ================= DEGREE LIST (150+) =================
degree_list = [
"BTech","BE","MTech","ME","Diploma Engineering","Polytechnic",
"Mechanical Engineering","Civil Engineering","Electrical Engineering",
"Electronics Engineering","Electronics & Communication Engineering",
"Computer Science Engineering","Information Technology",
"Artificial Intelligence","Machine Learning","Data Science",
"Cyber Security","Cloud Computing","Robotics Engineering",
"Automobile Engineering","Aeronautical Engineering","Aerospace Engineering",
"Marine Engineering","Petroleum Engineering","Chemical Engineering",
"Biotechnology Engineering","Biomedical Engineering",
"Environmental Engineering","Instrumentation Engineering",
"Production Engineering","Industrial Engineering",
"Mining Engineering","Mechatronics","Structural Engineering",
"Power Engineering","Renewable Energy Engineering","Nanotechnology",
"BCA","MCA","BSc Computer Science","MSc Computer Science",
"Software Engineering","Information Systems","Game Development",
"Full Stack Development","Blockchain Technology",
"BSc","MSc","Physics","Chemistry","Mathematics","Statistics",
"Microbiology","Biotechnology","Forensic Science",
"Environmental Science","Geology","Zoology","Botany",
"Astrophysics","Oceanography","Material Science",
"BCom","MCom","BBA","MBA","Finance","Accounting",
"Banking & Insurance","International Business",
"Business Analytics","Human Resource Management",
"Marketing Management","Operations Management",
"Supply Chain Management","Retail Management",
"Entrepreneurship","Hospital Administration",
"BA","MA","English Literature","Tamil Literature","Hindi Literature",
"History","Political Science","Economics","Sociology",
"Psychology","Philosophy","Public Administration",
"Journalism","Mass Communication","Social Work",
"Fine Arts","Performing Arts","Linguistics",
"Archaeology","Anthropology",
"MBBS","MD","MS","BDS","MDS","BSc Nursing","GNM Nursing",
"Pharmacy","BPharm","MPharm","PharmD",
"Physiotherapy","BPT","MPT","Radiology",
"Medical Laboratory Technology","Optometry",
"Occupational Therapy","Speech Therapy",
"Cardiac Technology","Dialysis Technology",
"Anesthesia Technology","Emergency Medical Technology",
"BAMS","BHMS","BUMS","BSMS","BNYS",
"LLB","LLM","Corporate Law","Criminal Law",
"BEd","MEd","Special Education",
"Agriculture","Agricultural Engineering","Horticulture",
"Forestry","Dairy Technology","Veterinary Science",
"Fisheries Science","Food Technology",
"Hotel Management","Hospitality Management",
"Tourism Management","Aviation Management",
"Animation","Graphic Designing","Fashion Designing",
"Interior Designing","Film Making","Photography",
"Defense Studies","Criminology","Public Policy",
"BArch","MArch","Urban Planning",
"CA","CS","CMA","Actuarial Science",
"Nautical Science","Logistics Management",
"Sports Science","Yoga Science",
"Library Science","Information Science"
]

# ================= JOB DATABASE (25+) =================
jobs = [
["Infosys","Software Trainee",["BTech","BE","BCA","MCA"],60,18,28,"https://www.infosys.com/careers"],
["TCS","Assistant System Engineer",["BTech","BE"],60,18,28,"https://www.tcs.com/careers"],
["Wipro","Project Engineer",["BTech","BE","Diploma Engineering"],60,18,27,"https://careers.wipro.com"],
["HCL","Graduate Engineer Trainee",["BTech","BE"],60,18,28,"https://www.hcltech.com/careers"],
["Tech Mahindra","Software Developer",["BTech","BE","MCA"],60,18,28,"https://careers.techmahindra.com"],
["Capgemini","Analyst",["BTech","BE","MCA"],60,18,28,"https://www.capgemini.com/careers"],
["Accenture","Associate Software Engineer",["BTech","BE"],65,18,28,"https://www.accenture.com/in-en/careers"],
["IBM","Associate Developer",["BTech","BE"],65,18,28,"https://www.ibm.com/careers"],
["Cognizant","Programmer Analyst",["BTech","BE"],60,18,28,"https://careers.cognizant.com"],
["L&T","Graduate Engineer",["BTech","BE"],60,18,28,"https://www.larsentoubro.com/careers"],
["Flipkart","Operations Executive",["Any"],55,18,30,"https://www.flipkartcareers.com"],
["Amazon","Virtual Customer Support",["Any"],50,18,35,"https://www.amazon.jobs"],
["HDFC Bank","PO",["Any"],55,21,30,"https://www.hdfcbank.com/careers"],
["ICICI Bank","Relationship Officer",["Any"],55,21,30,"https://www.icicibank.com/careers"],
["Axis Bank","Sales Officer",["Any"],50,21,30,"https://www.axisbank.com/careers"],
["SSC","CGL Officer",["Any"],55,18,32,"https://ssc.nic.in"],
["RRB","NTPC Graduate",["Any"],55,18,33,"https://www.rrbcdg.gov.in"],
["Indian Army","Technical Entry",["BTech","BE"],60,18,27,"https://joinindianarmy.nic.in"],
["Indian Navy","Executive Officer",["BTech","BE"],60,19,27,"https://www.joinindiannavy.gov.in"],
["ISRO","Scientist",["BTech","BE"],65,18,28,"https://www.isro.gov.in/careers"],
["DRDO","Junior Research Fellow",["BTech","BE","MTech"],65,18,28,"https://www.drdo.gov.in/careers"],
["HAL","Engineer",["BTech","BE"],60,18,28,"https://hal-india.co.in/Careers"],
["BHEL","Engineer Trainee",["BTech","BE"],60,18,28,"https://www.bhel.com/careers"],
["ONGC","Graduate Trainee",["BTech","BE"],60,18,28,"https://www.ongcindia.com/careers"],
["NTPC","Executive Trainee",["BTech","BE"],60,18,28,"https://careers.ntpc.co.in"]
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

# ============================================================
# FORM PAGE
# ============================================================
if st.session_state.page == "form":

    st.title("💼 Job Opportunity Portal")

    # STATE & COLLEGE (dynamic refresh)
    state = st.selectbox("State *", sorted(df["State"].unique()))
    colleges = df[df["State"] == state]["College"].unique()
    college = st.selectbox("College *", sorted(colleges))

    with st.form("job_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *")
            age = st.number_input("Your Age *", 0, 100)

        with col2:
            degree = st.selectbox("Degree *", degree_list)
            tenth = st.number_input("10th % *", 0.0, 100.0)
            twelfth = st.number_input("12th % *", 0.0, 100.0)
            photo = st.file_uploader("Upload Photo (PDF Only) *", ["pdf"])
            certificate = st.file_uploader("Upload Degree Certificate (PDF Only) *", ["pdf"])

        submit = st.form_submit_button("🔍 Find Eligible Jobs")

    if submit:
        errors = []
        if age < 18:
            errors.append("You must be at least 18 years old")
        if photo is None:
            errors.append("Photo must be uploaded in PDF format")
        if certificate is None:
            errors.append("Certificate must be uploaded in PDF format")

        if errors:
            for e in errors:
                st.error(e)
        else:
            avg = (tenth + twelfth) / 2
            eligible = []

            for company, role, deg_list, min_per, min_age, max_age, link in jobs:
                if ((degree in deg_list or "Any" in deg_list)
                    and avg >= min_per
                    and min_age <= age <= max_age):
                    eligible.append([company, role, link])

            st.session_state.name = name
            st.session_state.age = age
            st.session_state.degree = degree
            st.session_state.eligible_jobs = eligible
            st.session_state.page = "result"
            st.rerun()

# ============================================================
# RESULT PAGE
# ============================================================
if st.session_state.page == "result":

    st.success(f"Welcome {st.session_state.name}! Age: {st.session_state.age}")

    if st.session_state.eligible_jobs:
        st.subheader("🎯 Jobs You Are Eligible For")

        for company, role, link in st.session_state.eligible_jobs:
            col1, col2 = st.columns([3,1])
            col1.write(f"**{company}** — {role}")

            if col2.button("Apply Now", key=f"{company}_{role}"):
                save_application(
                    st.session_state.name,
                    st.session_state.age,
                    st.session_state.degree,
                    company, role
                )
                webbrowser.open_new_tab(link)

    else:
        st.warning("No jobs matched your profile.")

    if st.button("🔙 Go Back"):
        st.session_state.page = "form"
        st.rerun()
