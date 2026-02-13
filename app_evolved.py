import streamlit as st
import pandas as pd
import csv
import os
import webbrowser

st.set_page_config(page_title="Job Opportunity Portal", page_icon="💼", layout="wide")

# ================= LOAD COLLEGES CSV =================
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

# ================= JOB DATABASE (80+) =================
jobs = [
["Infosys","Software Engineer",["BTech","BE","MCA","BCA"],60,18,28,"https://www.infosys.com/careers"],
["TCS","System Engineer",["BTech","BE"],60,18,28,"https://www.tcs.com/careers"],
["Wipro","Project Engineer",["BTech","BE"],60,18,27,"https://careers.wipro.com"],
["HCL","Graduate Engineer Trainee",["BTech","BE"],60,18,28,"https://www.hcltech.com/careers"],
["Tech Mahindra","Software Developer",["BTech","BE","MCA"],60,18,28,"https://careers.techmahindra.com"],
["Capgemini","Analyst Programmer",["BTech","BE","MCA"],60,18,28,"https://www.capgemini.com/careers"],
["Accenture","Associate Software Engineer",["BTech","BE"],65,18,28,"https://www.accenture.com/in-en/careers"],
["IBM","Application Developer",["BTech","BE"],65,18,28,"https://www.ibm.com/careers"],
["Cognizant","Programmer Analyst",["BTech","BE"],60,18,28,"https://careers.cognizant.com"],
["Oracle","Cloud Associate",["BTech","BE"],65,18,28,"https://www.oracle.com/careers"],
["Google","Associate Engineer",["BTech","BE"],75,21,30,"https://careers.google.com"],
["Microsoft","Software Engineer",["BTech","BE"],75,21,30,"https://careers.microsoft.com"],

["L&T","Site Engineer",["Civil Engineering"],60,18,30,"https://www.larsentoubro.com/careers"],
["Tata Motors","Design Engineer",["Mechanical Engineering"],60,18,30,"https://careers.tatamotors.com"],
["Siemens","Electrical Engineer",["Electrical Engineering"],65,18,30,"https://new.siemens.com/in/en/company/jobs.html"],
["BHEL","Engineer Trainee",["BTech","BE"],60,18,28,"https://www.bhel.com/careers"],
["NTPC","Executive Trainee",["BTech","BE"],60,18,28,"https://careers.ntpc.co.in"],
["ONGC","Graduate Trainee",["BTech","BE"],60,18,28,"https://www.ongcindia.com/careers"],
["HAL","Aeronautical Engineer",["Aeronautical Engineering"],60,18,28,"https://hal-india.co.in/Careers"],
["ISRO","Scientist",["BTech","BE"],65,18,28,"https://www.isro.gov.in/careers"],

["SSC","CGL Officer",["Any Degree"],55,18,32,"https://ssc.gov.in"],
    ["RRB","NTPC Graduate",["Any Degree"],55,18,33,"https://indianrailways.gov.in"]
]
["UPSC","Civil Services",["Any"],60,21,32,"https://www.upsc.gov.in"],

["HDFC Bank","Probationary Officer",["BCom","MBA"],55,21,30,"https://www.hdfcbank.com/careers"],
["ICICI Bank","Relationship Officer",["BCom","MBA"],55,21,30,"https://www.icicibank.com/careers"],
["Deloitte","Audit Associate",["BCom","CA"],60,21,30,"https://www2.deloitte.com/in/en/careers.html"],
["KPMG","Tax Consultant",["BCom","CA"],60,21,30,"https://home.kpmg/in/en/home/careers.html"],

["Apollo Hospitals","Junior Doctor",["MBBS"],60,23,35,"https://www.apollohospitals.com/careers"],
["AIIMS","Staff Nurse",["BSc Nursing"],60,21,35,"https://www.aiims.edu/en/jobs.html"],
["Cipla","Clinical Research Associate",["Pharmacy"],60,22,35,"https://www.cipla.com/careers"],

["AZB & Partners","Legal Associate",["LLB"],60,23,35,"https://www.azbpartners.com/careers"],
["NABARD","Development Officer",["Agriculture"],60,21,30,"https://www.nabard.org/careers"],
["IndiGo","Ground Staff",["Aviation Management"],55,18,30,"https://careers.goindigo.in"],
["Taj Hotels","Management Trainee",["Hotel Management"],55,21,30,"https://www.tajhotels.com/en-in/about-taj/careers"],
["Times Group","Content Editor",["Journalism"],55,21,30,"https://timesgroup.com/careers"],
["Byju's","Academic Counselor",["BEd"],55,21,30,"https://byjus.com/careers"],
["Hafeez Contractor","Junior Architect",["BArch"],60,22,30,"https://www.hafeezcontractor.com/careers"],
["Titan","Product Designer",["Product Designing"],60,21,30,"https://www.titancompany.in/careers"]
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

# ================= FORM PAGE =================
if st.session_state.page == "form":

    st.title("💼 Job Opportunity Portal")

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

# ================= RESULT PAGE =================
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
