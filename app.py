import streamlit as st
from groq import Groq
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
from datetime import datetime 
import uuid
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")

st.set_page_config(
    page_title="MicroDx AI",
    page_icon="🦠",
    layout="wide"
)


from secret import GROQ_API_KEY


client = Groq(api_key=GROQ_API_KEY)

current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
report_id = str(uuid.uuid4())[:8].upper()

bg_img = get_base64_image("background.jpg")

st.markdown(
    f"""
    <style>

    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{bg_img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    

    /* Dark overlay for readability */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.45);
        z-index: -1;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# PASTE PDF FUNCTION HERE
def create_pdf_report(patient_name, age, gender, report_text):

    temp_pdf = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    doc = SimpleDocTemplate(temp_pdf.name)

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "MicroDx AI Clinical Screening Report",
        styles["Title"]
    )

    content.append(title)

    content.append(Spacer(1, 12))

    patient_details = Paragraph(
        f"""
        Patient Name: {patient_name}<br/>
        Age: {age}<br/>
        Gender: {gender}
        """,
        styles["BodyText"]
    )

    content.append(patient_details)

    content.append(Spacer(1, 12))

    report = Paragraph(
        report_text.replace("\n", "<br/>"),
        styles["BodyText"]
    )

    content.append(report)

    doc.build(content)

    return temp_pdf.name


    prompt = f"""
    You are MicroDx AI, an expert microbiologist and infectious disease decision-support assistant.

     Patient Information:
     Name: {name}
     Age: {age}
     Gender: {gender}
     Temperature: {temperature} °C
     Duration of Symptoms: {duration} days

Risk Factors:
Travel History: {travel_history}
Animal Contact: {animal_contact}
Immunocompromised: {immunocompromised}
Recent Hospitalization: {hospitalization}

Symptoms:
{", ".join(symptoms)}

Provide:

1. Infection Category
(Bacterial / Viral / Fungal / Parasitic / Non-Infectious)

2. Confidence Score (%)

3. Severity Score
(Low / Moderate / High / Critical)

4. Top 3 Suspected Diseases

5. Most Likely Causative Organisms

6. Recommended Laboratory Tests

7. Recommended Specialist

8. Supportive Care Advice

9. Red Flag Symptoms

10. Clinical Summary

IMPORTANT:
- Do not prescribe medicines.
- Do not prescribe antibiotics.
- Mention that this is not a confirmed diagnosis.
- Keep the report professional and concise.
"""

# Header

st.markdown("""
<h1 style='text-align:center;'>
🦠 MicroDx AI
</h1>

<h4 style='text-align:center; color:#00ff99;'>
AI-Powered Infectious Disease Intelligence Platform
</h4>
""", unsafe_allow_html=True)

# Patient Information

name = st.text_input("Patient Name")
st.markdown('<div class="report-card">', unsafe_allow_html=True)

age = st.number_input(
"Age",
min_value=0,
max_value=120,
value=25
)

gender = st.selectbox(
"Gender",
["Male", "Female", "Other"]
)

temperature = st.number_input(
"Body Temperature (°C)",
min_value=30.0,
max_value=45.0,
value=37.0
)

duration = st.number_input(
"Duration of Symptoms (Days)",
min_value=1,
max_value=365,
value=3
)
travel_history = st.selectbox(
    "Recent Travel History",
    ["No", "Yes"]
)

animal_contact = st.selectbox(
    "Animal Contact",
    ["No", "Yes"]
)

immunocompromised = st.selectbox(
    "Immunocompromised",
    ["No", "Yes"]
)

hospitalization = st.selectbox(
    "Recent Hospitalization",
    ["No", "Yes"]
)

symptoms = st.multiselect(
"Select Symptoms",
[
# General Symptoms
"Fever",
"Low Grade Fever",
"High Grade Fever",
"Chills",
"Night Sweats",
"Fatigue",
"Weakness",
"Weight Loss",
"Loss of Appetite",

    # Respiratory Symptoms
    "Cough",
    "Productive Cough",
    "Dry Cough",
    "Shortness of Breath",
    "Chest Pain",
    "Sore Throat",
    "Runny Nose",
    "Nasal Congestion",
    "Sneezing",
    "Wheezing",
    "Hemoptysis",

    # Gastrointestinal Symptoms
    "Nausea",
    "Vomiting",
    "Diarrhea",
    "Bloody Diarrhea",
    "Abdominal Pain",
    "Abdominal Cramps",
    "Constipation",
    "Bloating",

    # Neurological Symptoms
    "Headache",
    "Dizziness",
    "Confusion",
    "Seizures",
    "Neck Stiffness",
    "Photophobia",

    # Dermatological Symptoms
    "Rash",
    "Itching",
    "Skin Peeling",
    "Blisters",
    "Redness",
    "Skin Lesions",
    "Ulcers",

    # Musculoskeletal Symptoms
    "Joint Pain",
    "Muscle Pain",
    "Back Pain",
    "Bone Pain",

    # Urinary Symptoms
    "Burning Urination",
    "Frequent Urination",
    "Blood in Urine",
    "Flank Pain",

    # ENT Symptoms
    "Ear Pain",
    "Hearing Loss",
    "Difficulty Swallowing",

    # Eye Symptoms
    "Red Eyes",
    "Blurred Vision",
    "Eye Discharge",

    # Reproductive Symptoms
    "Vaginal Discharge",
    "Genital Ulcers",
    "Pelvic Pain",

    # Travel / Tropical Disease Indicators
    "Mosquito Bite Exposure",
    "Tick Bite Exposure",
    "Animal Bite",
    "Contaminated Water Exposure",

    # Immunological Indicators
    "Recurrent Infections",
    "Swollen Lymph Nodes",

    # Severe Warning Symptoms
    "Altered Mental Status",
    "Persistent Vomiting",
    "Severe Dehydration",
    "Loss of Consciousness"
]

)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("Analyze Symptoms"):

    if len(symptoms) == 0:
        st.error("Please select at least one symptom.")

    else:

        prompt = f"""

You are an expert microbiologist and infectious disease screening assistant.

Patient Information:
Name: {name}
Age: {age}
Gender: {gender}
Temperature: {temperature} °C
Report ID: MDX-{report_id}<br/>
Generated On: {current_time}
Duration of Symptoms: {duration} days

Symptoms:
{", ".join(symptoms)}

Analyze and provide:

1. Probable Infection Category
   (Bacterial / Viral / Fungal / Parasitic / Non-Infectious)

2. Confidence Score (%)

3. Top 3 Suspected Diseases

4. Suggested Laboratory Tests

5. Recommended Specialist

6. Supportive Care Advice

7. Red Flag Symptoms

IMPORTANT:

* Do not prescribe medicines.
* Do not prescribe antibiotics.
* Mention this is not a confirmed diagnosis.
  """

  
    try:

        with st.spinner("Analyzing symptoms..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert microbiologist and infectious disease specialist."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )

            result = response.choices[0].message.content

            st.success("Analysis Completed")
            st.subheader("📋 Clinical Screening Report")
            st.markdown(result)
            
            pdf_file = create_pdf_report(
            name,
            age,
            gender,
            result
           )

            with open(pdf_file, "rb") as file:

             st.download_button(
            label="📄 Download PDF Report",
            data=file,
            file_name=f"MicroDx_Report_{name}.pdf",
            mime="application/pdf"
            )

            if "critical" in result.lower():
             st.error("🚨 HIGH RISK CASE - Immediate Medical Attention Recommended")

    except Exception as e:
        st.error(f"Error: {str(e)}")

st.warning(
"⚠️ This AI tool is for educational purposes only and is not a medical diagnosis. Consult a qualified physician."
)

if st.button("Test Groq"):
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": "Say Hello MicroDx"
            }
        ]
    )
    st.write(response.choices[0].message.content)
