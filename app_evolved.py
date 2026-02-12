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

# ---------------- COLLEGES (30+ EACH) ----------------
colleges_by_state = {
    "Tamil Nadu": [
        "Anna University","IIT Madras","NIT Trichy","VIT Vellore","SRM University",
        "SASTRA University","PSG Tech","CIT Coimbatore","Loyola College",
        "Madras Christian College","Thiagarajar College","Kumaraguru College",
        "Kongu Engineering","Hindustan University","Vel Tech","Bharath University",
        "Saveetha University","Rajalakshmi Engineering","Panimalar Engineering",
        "Easwari Engineering","Sri Krishna College","Amrita University",
        "Karunya University","Dhanalakshmi College","Apollo Engineering",
        "Jeppiaar Engineering","Tagore Engineering","Prince Engineering",
        "Agni College","Jerusalem Engineering","Sathyabama University"
    ],
    "Karnataka": [
        "IISc Bangalore","NIT Surathkal","RV College","PES University","BMS College",
        "MS Ramaiah","Christ University","Jain University","Dayananda Sagar",
        "New Horizon","CMR Institute","Reva University","Presidency University",
        "Acharya Institute","Garden City","East West Institute","Global Academy",
        "SJBIT","Oxford Engineering","AMC Engineering","MVJ College",
        "Sir MVIT","BNM Institute","T John College","Kristu Jayanti",
        "Mount Carmel","St Joseph’s College","KLE Tech","SDM Engineering",
        "Manipal Institute","NMAMIT"
    ],
    "Kerala": [
        "IIT Palakkad","NIT Calicut","CUSAT","CET Trivandrum","Model Engineering",
        "Rajagiri Engineering","SCMS Engineering","TKM College","Amrita University",
        "MES Engineering","Mar Athanasius","Saintgits College","Adi Shankara",
        "Vidya Academy","GEC Thrissur","GEC Kannur","GEC Wayanad","Ilahia College",
        "Mangalam College","SNG College","Sahrdaya College","Jyothi Engineering",
        "Universal Engineering","LBS College","Federal Institute","Viswajyothi",
        "Christ College","Baselios College","De Paul Institute","Younus College",
        "College of Applied Science"
    ]
}

# ---------------- 50+ DEGREES ----------------
degree_list = [
    "BTech","BE","BCA","MCA","Diploma","ITI","BSc CS","BSc IT","BSc Physics",
    "BSc Chemistry","BSc Maths","BSc Statistics","BSc Biotechnology",
    "BSc Microbiology","BSc Agriculture","BCom","BCom Finance","BCom Banking",
    "BBA","MBA","MBA HR","MBA Finance","MBA Marketing","MBA Systems",
    "BA English","BA Economics","BA History","BA Political Science",
    "MA English","MA Economics","MA History","MA Sociology","BEd","MEd",
    "MBBS","BDS","BPharm","DPharm","PharmD","Nursing","BPT","MPT",
    "LLB","LLM","BA LLB","BBA LLB","Hotel Management","Aviation",
    "Animation","Graphic Design","Fashion Design","Interior Design",
    "Journalism","Mass Communication","Food Technology","Environmental Science",
    "Veterinary Science","Forestry","Cyber Security","Cloud Computing",
    "Artificial Intelligence","Machine Learning","Data Science","Robotics",
    "Mechatronics","Automobile Engineering","Civil Engineering","Mechanical Engineering",
    "Electrical Engineering","Electronics Engineering","Any Degree"
]

# ---------------- 25+ JOBS ----------------
jobs = [
    ["Infosys","Software Trainee",["BTech","BE","BCA","MCA"],60,18,28,"https://www.infosys.com/careers"],
    ["TCS","System Engineer",["BTech","BE"],60,18,28,"https://www.tcs.com/careers"],
    ["Wipro","Project Engineer",["BTech","BE","Diploma"],60,18,27,"https://careers.wipro.com"],
    ["HCL","Graduate Engineer",["BTech","BE"],60,18,28,"https://www.hcltech.com/careers"],
    ["Accenture","Associate Software Engineer",["BTech","BE"],60,18,28,"https://www.accenture.com/careers"],
    ["Capgemini","Analyst",["BTech","BE","MCA"],60,18,28,"https://www.capgemini.com/careers"],
    ["Cognizant","Programmer Analyst",["BTech","BE"],60,18,28,"https://careers.cognizant.com"],
    ["IBM","Associate Developer",["BTech","BE"],60,18,28,"https://www.ibm.com/careers"],
    ["Tech Mahindra","Software Engineer",["BTech","BE"],60,18,28,"https://careers.techmahindra.com"],
    ["Oracle","Junior Developer",["BTech","BE"],60,18,28,"https://www.oracle.com/careers"],
    ["Google","Support Engineer",["BTech","BE"],65,21,30,"https://careers.google.com"],
    ["Amazon","Cloud Support Associate",["BTech","BE"],65,21,30,"https://www.amazon.jobs"],
    ["Flipkart","Graduate Engineer",["BTech","BE"],60,21,30,"https://www.flipkartcareers.com"],
    ["SSC","CGL Officer",["Any Degree"],55,18,32,"https://ssc.nic.in"],
    ["RRB","NTPC Graduate",["Any Degree"],55,18,33,"https://www.rrbcdg.gov.in"],
    ["Bank PO","Probationary Officer",["Any Degree"],60,20,30,"https://ibps.in"],
    ["Indian Army","Technical Entry",["BTech","BE"],60,18,25,"https://joinindianarmy.nic.in"],
    ["Indian Navy","Graduate Entry",["BTech","BE"],60,19,25,"https://www.joinindiannavy.gov.in"],
    ["ISRO","Scientist Assistant",["BTech","BE"],65,21,30,"https://www.isro.gov.in/careers"],
    ["DRDO","Junior Scientist",["BTech","BE"],65,21,30,"https://www.drdo.gov.in"],
    ["HAL","Graduate Engineer",["BTech","BE"],60,21,30,"https://hal-india.co.in"],
    ["BSNL","Junior Engineer",["Diploma","BE"],55,18,30,"https://www.bsnl.co.in"],
    ["BEL","Engineer Trainee",["BTech","BE"],60,21,30,"https://bel-india.in"],
    ["NTPC","Graduate Engineer",["BTech","BE"],60,21,30,"https://www.ntpc.co.in"],
    ["ONGC","Trainee Engineer",["BTech","BE"],60,21,30,"https://www.ongcindia.com"]
]

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "form"

# ---------------- FORM ----------------
if st.session_state.page == "form":
    st.title("💼 Job Opportunity Portal")

    with st.form("job_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *")
            age = st.number_input("Your Age *",0,100)
            state = st.selectbox("State *",list(colleges_by_state.keys()))

            # ✅ UPDATED LINE (dynamic refresh)
            college = st.selectbox("College *", colleges_by_state[state], key=f"college_{state}")

        with col2:
            degree = st.selectbox("Degree *",degree_list)
            tenth = st.number_input("10th % *",0.0,100.0)
            twelfth = st.number_input("12th % *",0.0,100.0)
            photo = st.file_uploader("Upload Your Photo (PDF Only) *",["pdf"])
            certificate = st.file_uploader("Upload Degree Certificate (PDF Only) *",["pdf"])

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
            avg = (tenth+twelfth)/2
            eligible=[]
            for c,r,d,mn,a1,a2,link in jobs:
                if (degree in d or "Any Degree" in d) and avg>=mn and a1<=age<=a2:
                    eligible.append([c,r,link])
            st.session_state.name=name
            st.session_state.age=age
            st.session_state.eligible_jobs=eligible
            st.session_state.page="result"
            st.rerun()

# ---------------- RESULTS ----------------
if st.session_state.page=="result":
    st.success(f"Welcome {st.session_state.name}! Age: {st.session_state.age}")
    if st.session_state.eligible_jobs:
        for c,r,link in st.session_state.eligible_jobs:
            col1,col2=st.columns([3,1])
            col1.write(f"**{c}** — {r}")
            col2.markdown(f"[🚀 Apply Now]({link})")
    else:
        st.warning("No jobs matched.")
    if st.button("🔙 Go Back"):
        st.session_state.page="form"
        st.rerun()
