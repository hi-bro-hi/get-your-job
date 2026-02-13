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
colleges_by_state = {

    "Tamil Nadu": [
        "IIT Madras","NIT Tiruchirappalli","Anna University","University of Madras",
        "Bharathiar University","Bharathidasan University","Alagappa University",
        "Madurai Kamaraj University","Periyar University",
        "Manonmaniam Sundaranar University",
        "Tamil Nadu Agricultural University",
        "Tamil Nadu Dr. MGR Medical University",
        "Tamil Nadu Veterinary and Animal Sciences University",
        "Annamalai University","VIT Vellore",
        "SRM Institute of Science and Technology",
        "SASTRA University","Amrita Vishwa Vidyapeetham Coimbatore",
        "Hindustan Institute of Technology and Science",
        "Saveetha Institute of Medical and Technical Sciences",
        "Bharath Institute of Higher Education and Research",
        "Sathyabama Institute of Science and Technology",
        "Karunya Institute of Technology and Sciences",
        "PSG College of Technology","Coimbatore Institute of Technology",
        "Kumaraguru College of Technology","Kongu Engineering College",
        "Thiagarajar College of Engineering",
        "Sri Krishna College of Engineering and Technology",
        "Vel Tech Rangarajan Dr. Sagunthala R&D Institute",
        "Rajalakshmi Engineering College","Panimalar Engineering College",
        "Easwari Engineering College","Jeppiaar Engineering College",
        "St Joseph’s College of Engineering","SSN College of Engineering",
        "RMK Engineering College","Velammal Engineering College",
        "Sri Sairam Engineering College","Loyola College Chennai",
        "Madras Christian College","Stella Maris College",
        "Women’s Christian College","Presidency College Chennai",
        "Ethiraj College for Women","PSG College of Arts and Science",
        "American College Madurai","Bishop Heber College",
        "Lady Doak College","Madras Medical College",
        "Stanley Medical College","Kilpauk Medical College",
        "Coimbatore Medical College","Madurai Medical College",
        "Tirunelveli Medical College","Chengalpattu Medical College",
        "Thoothukudi Medical College",
        "Dr Ambedkar Government Law College Chennai",
        "Tamil Nadu National Law University",
        "Agricultural College and Research Institute Coimbatore",
        "Forest College and Research Institute Mettupalayam",
        "Sri Ramachandra Institute of Higher Education and Research",
        "Chettinad Academy of Research and Education"
    ],

    "Karnataka": [
        "Indian Institute of Science Bangalore","NIT Surathkal",
        "University of Mysore","Bangalore University",
        "Karnataka University Dharwad","Mangalore University",
        "Kuvempu University","Gulbarga University",
        "Visvesvaraya Technological University",
        "University of Agricultural Sciences Bangalore",
        "University of Agricultural Sciences Dharwad",
        "Rajiv Gandhi University of Health Sciences",
        "National Law School of India University",
        "Christ University","Jain University",
        "Manipal Academy of Higher Education",
        "Alliance University","Reva University",
        "Presidency University Bangalore","Azim Premji University",
        "RV College of Engineering","PES University",
        "BMS College of Engineering",
        "MS Ramaiah Institute of Technology",
        "Dayananda Sagar College of Engineering",
        "New Horizon College of Engineering",
        "CMR Institute of Technology",
        "Sir M Visvesvaraya Institute of Technology",
        "BNM Institute of Technology","SJBIT Bangalore",
        "KLE Technological University","SDM College of Engineering",
        "Bangalore Medical College","Mysore Medical College",
        "Kasturba Medical College Manipal","St John’s Medical College",
        "JSS Medical College","Mount Carmel College",
        "St Joseph’s College Bangalore",
        "Kristu Jayanti College","NMKRV College",
        "Government Arts College Bangalore",
        "KLE Society Law College",
        "University Law College Bangalore",
        "Garden City University","East West Institute of Technology",
        "Global Academy of Technology","Oxford College of Engineering",
        "AMC Engineering College","T John College",
        "Acharya Institute of Technology",
        "RNS Institute of Technology","MVJ College of Engineering"
    ],

    "Kerala": [
        "IIT Palakkad","NIT Calicut","University of Kerala",
        "Mahatma Gandhi University Kerala","University of Calicut",
        "Cochin University of Science and Technology",
        "Kerala Agricultural University",
        "Kerala University of Health Sciences",
        "Kerala Veterinary and Animal Sciences University",
        "Central University of Kerala",
        "Amrita Vishwa Vidyapeetham",
        "APJ Abdul Kalam Technological University",
        "College of Engineering Trivandrum",
        "Government Engineering College Thrissur",
        "Government Engineering College Kozhikode",
        "Rajagiri School of Engineering and Technology",
        "Model Engineering College Kochi",
        "Mar Athanasius College of Engineering",
        "TKM College of Engineering",
        "Saintgits College of Engineering",
        "Adi Shankara Institute of Engineering and Technology",
        "Vidya Academy of Science and Technology",
        "Sahrdaya College of Engineering",
        "Jyothi Engineering College",
        "Viswajyothi College of Engineering",
        "Government Medical College Thiruvananthapuram",
        "Government Medical College Kozhikode",
        "Government Medical College Kottayam",
        "Amrita Institute of Medical Sciences",
        "Jubilee Mission Medical College",
        "Pushpagiri Medical College",
        "St Teresa’s College Kochi",
        "Sacred Heart College Thevara",
        "Mar Ivanios College",
        "Farook College Kozhikode",
        "Maharaja’s College Ernakulam",
        "Government Law College Ernakulam",
        "National University of Advanced Legal Studies",
        "Federal Institute of Science and Technology",
        "Ilahia College of Engineering",
        "Mangalam College of Engineering",
        "Younus College of Engineering",
        "College of Applied Science Trivandrum"
    ]
}


# ---------------- 100+ JOBS ----------------
jobs += [

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

["SSC","CGL Officer",["Any"],55,18,32,"https://ssc.nic.in"],
["RRB","NTPC Graduate",["Any"],55,18,33,"https://www.rrbcdg.gov.in"],
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





