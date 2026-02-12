import streamlit as st
import csv
import os

st.set_page_config(page_title="Job Opportunity Portal", page_icon="💼", layout="wide")

# ---------------- COLLEGES (30+ EACH STATE) ----------------
colleges_by_state = {
    "Tamil Nadu": [
        "Anna University","IIT Madras","NIT Trichy","VIT Vellore","SRM IST",
        "PSG College of Technology","SSN College of Engineering",
        "Thiagarajar College of Engineering","SASTRA University",
        "Amrita Vishwa Vidyapeetham","Vel Tech","Hindustan University",
        "Kongu Engineering College","Kumaraguru College of Technology",
        "Coimbatore Institute of Technology","Rajalakshmi Engineering College",
        "St Joseph’s College of Engineering","Panimalar Engineering College",
        "Saveetha Engineering College","Jeppiaar Engineering College",
        "Karunya University","Bannari Amman Institute of Technology",
        "Sri Krishna College of Engineering","Mepco Schlenk Engineering College",
        "Government College of Technology","Madras Institute of Technology",
        "Loyola College","Madras Christian College","Bharath University",
        "Crescent University","Periyar Maniammai Institute"
    ],
    "Karnataka": [
        "IISc Bangalore","NIT Surathkal","RV College of Engineering",
        "BMS College of Engineering","MS Ramaiah Institute of Technology",
        "PES University","Christ University","Jain University",
        "Dayananda Sagar College","Sir M Visvesvaraya Institute",
        "New Horizon College","Reva University","CMR Institute of Technology",
        "Alliance University","Presidency University","Acharya Institute",
        "KLE Technological University","SDM College of Engineering",
        "Bangalore Institute of Technology","Global Academy of Technology",
        "Dr Ambedkar Institute of Technology","East West Institute",
        "Oxford College of Engineering","RNS Institute of Technology",
        "T John Institute","Nitte Meenakshi Institute",
        "Bangalore University","Manipal Institute of Technology",
        "Visvesvaraya Technological University","Mount Carmel College",
        "St Joseph’s College Bangalore"
    ],
    "Kerala": [
        "IIT Palakkad","NIT Calicut","CUSAT","College of Engineering Trivandrum",
        "Government Engineering College Thrissur","TKM College of Engineering",
        "MEC Kochi","Amrita School of Engineering","Rajagiri School of Engineering",
        "Mar Baselios College","SCMS School of Engineering","Saintgits College",
        "Federal Institute of Science and Technology","Adi Shankara Institute",
        "Ilahia College of Engineering","Jyothi Engineering College",
        "Vidya Academy of Science and Technology","Christ College Irinjalakuda",
        "Muthoot Institute of Technology","Sree Buddha College",
        "College of Engineering Adoor","Government Engineering College Kozhikode",
        "College of Engineering Kottayam","College of Engineering Chengannur",
        "College of Engineering Poonjar","College of Engineering Perumon",
        "College of Engineering Vadakara","MES College of Engineering",
        "KMCT College of Engineering","Universal Engineering College",
        "Sahrdaya College of Engineering"
    ]
}

# ---------------- JOB DATABASE ----------------
jobs = [
    ["Infosys","Software Trainee",["BTech","BE","BCA","MCA"],60,18,28],
    ["TCS","Assistant System Engineer",["BTech","BE"],60,18,28],
    ["Wipro","Project Engineer",["BTech","BE","Diploma"],60,18,27],
    ["SSC","CGL Officer",["Any"],55,18,32],
    ["RRB","NTPC Graduate",["Any"],55,18,33]
]

def save_application(name, age, degree, company, role):
    file_exists = os.path.isfile("applications.csv")
    with open("applications.csv","a",newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name","Age","Degree","Company","Role"])
        writer.writerow([name,age,degree,company,role])

if "page" not in st.session_state:
    st.session_state.page="form"

# ---------------- FORM ----------------
if st.session_state.page=="form":
    st.title("💼 Job Opportunity Portal")

    with st.form("job_form"):
        col1,col2=st.columns(2)

        with col1:
            name=st.text_input("Full Name *")
            age=st.number_input("Your Age *",0,100)
            state=st.selectbox("State *",list(colleges_by_state.keys()))
            college=st.selectbox("College *",colleges_by_state[state])

        with col2:
            degree=st.selectbox("Degree *",[

                # Engineering
                "BTech","BE","B.E Civil","B.E Mechanical","B.E Electrical",
                "B.E Electronics","B.E ECE","B.E EEE","B.E Automobile",
                "B.Tech IT","B.Tech CSE","B.Tech AI","B.Tech Data Science",
                "B.Tech Biotechnology","B.Tech Chemical","B.Tech Aeronautical",
                "B.Tech Mechatronics","B.Tech Robotics",

                # IT & Computer
                "BCA","MCA","BSc Computer Science","BSc IT","BSc Data Science",
                "Diploma Computer","Diploma IT","Cyber Security","Cloud Computing",
                "Artificial Intelligence","Machine Learning",

                # Science
                "BSc Physics","BSc Chemistry","BSc Maths","BSc Statistics",
                "BSc Biotechnology","BSc Microbiology","BSc Zoology","BSc Botany",
                "MSc Physics","MSc Chemistry","MSc Maths","MSc Biotechnology",

                # Commerce
                "BCom","BCom Finance","BCom Accounting","BCom Banking",
                "MCom","BBA","MBA HR","MBA Finance","MBA Marketing",
                "MBA Systems","MBA Operations","MBA Business Analytics",

                # Arts
                "BA English","BA Economics","BA History","BA Political Science",
                "BA Sociology","MA English","MA Economics","MA History",
                "MA Sociology","Journalism","Mass Communication",

                # Medical
                "MBBS","BDS","MDS","BPT","MPT","BSc Nursing",
                "GNM Nursing","PharmD","BPharm","DPharm",
                "Medical Lab Technology","Radiology","Optometry",

                # Law
                "LLB","LLM","BA LLB","BBA LLB",

                # Education
                "BEd","MEd","D.El.Ed",

                # Design
                "BFA","MFA","Animation","Graphic Design","Fashion Designing",
                "Interior Design","Multimedia",

                # Hospitality
                "Hotel Management","Catering Technology","Tourism",
                "Aviation","Air Hostess Training",

                # Agriculture
                "BSc Agriculture","BSc Horticulture","Veterinary Science",
                "Food Technology","Environmental Science",

                # Technical
                "Diploma Mechanical","Diploma Civil","Diploma Electrical",
                "ITI Fitter","ITI Electrician","ITI Welder",

                "Any Degree"
            ])

            tenth=st.number_input("10th Percentage *",0.0,100.0)
            twelfth=st.number_input("12th Percentage *",0.0,100.0)
            photo=st.file_uploader("Upload Photo *",type=["jpg","png"])
            certificate=st.file_uploader("Upload Degree Certificate *",type=["jpg","png","pdf"])

        submit=st.form_submit_button("🔍 Find Eligible Jobs")

    if submit:
        errors=[]
        if not name.strip(): errors.append("Full Name is required")
        if age<18: errors.append("You must be at least 18 years old")
        if tenth==0 or twelfth==0: errors.append("10th and 12th percentages required")
        if photo is None: errors.append("Photo upload required")
        if certificate is None: errors.append("Degree certificate upload required")

        if errors:
            for e in errors: st.error(e)
        else:
            avg=(tenth+twelfth)/2
            eligible=[]
            for c,r,d,m,a1,a2 in jobs:
                if (degree in d or "Any" in d) and avg>=m and a1<=age<=a2:
                    eligible.append([c,r])

            st.session_state.name=name
            st.session_state.age=age
            st.session_state.degree=degree
            st.session_state.eligible_jobs=eligible
            st.session_state.page="result"
            st.rerun()

# ---------------- RESULTS ----------------
if st.session_state.page=="result":
    st.success(f"Welcome {st.session_state.name}! Age: {st.session_state.age}")

    if st.session_state.eligible_jobs:
        st.subheader("🎯 Jobs You Are Eligible For")
        for c,r in st.session_state.eligible_jobs:
            col1,col2=st.columns([3,1])
            col1.write(f"**{c}** — {r}")
            if col2.button("Apply Now",key=f"{c}_{r}"):
                save_application(st.session_state.name,st.session_state.age,st.session_state.degree,c,r)
                st.success(f"Applied to {c} for {r}!")
    else:
        st.warning("No jobs matched your profile.")

    if st.button("🔙 Go Back"):
        st.session_state.page="form"
        st.rerun()
