import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="HealthPulse AI | Smart Healthcare", page_icon="🩺", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*="css"] {font-family: 'DM Sans', sans-serif;}
.stApp {background: radial-gradient(circle at 10% 0%, #132c48 0%, #071321 42%, #071321 100%); color:#eaf3ff;}
section[data-testid="stSidebar"] {background:linear-gradient(180deg,#0b1b2d,#071321); border-right:1px solid #19334c;}
h1,h2,h3 {font-family:'Space Grotesk',sans-serif !important; color:#eaf3ff;}
.hero {padding:1.2rem 0 1rem 0;}
.kicker {color:#43e5e8; font-size:.72rem; letter-spacing:2px; font-weight:700;}
.hero-title {font-size:2.8rem; line-height:1.08; font-weight:700; margin:.3rem 0;}
.gradient {background:linear-gradient(90deg,#43e5e8,#8aa8ff,#a27bff);-webkit-background-clip:text;background-clip:text;color:transparent;}
.hero-sub {color:#9bb2ca; max-width:700px;}
.metric-card {background:linear-gradient(145deg,#10243a,#0b1b2d); border:1px solid #213a54; border-radius:18px; padding:18px 20px; min-height:125px;}
.metric-label {font-size:.78rem;color:#9bb2ca;}
.metric-value {font-family:'Space Grotesk';font-size:1.75rem;font-weight:700;color:#f3f8ff;margin:.2rem 0;}
.metric-note {font-size:.7rem;color:#54dfad;}
.panel {background:linear-gradient(145deg,#10243a,#0b1b2d);border:1px solid #213a54;border-radius:18px;padding:18px;}
div[data-testid="stMetric"] {background:#10243a;border:1px solid #213a54;padding:14px;border-radius:14px;}
div[data-testid="stMetric"] label {color:#9bb2ca;}
.stButton button {border-radius:10px;background:linear-gradient(90deg,#43dfe1,#5c8cff);color:#071321;border:0;font-weight:700;}
div[data-testid="stAlert"] {border-radius:12px;}
hr {border-color:#1c344c;}
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🩺 HealthPulse AI")
    st.caption("SMART HEALTH ANALYTICS")
    page = st.radio("Navigation", ["Dashboard", "Health Risk Assessment", "Health Insights", "About Project"], label_visibility="collapsed")
    st.divider()
    st.markdown("### Demo profile")
    st.caption("No sign-in required. Your form inputs are not saved or uploaded.")
    st.markdown("**Academic prototype · 2026**")

# ---------- Helpers ----------
def calculate_demo_score(age, bmi, bp, heart_rate, glucose, activity, smoker, family):
    score = 8
    if age >= 60: score += 18
    elif age >= 45: score += 10
    elif age >= 35: score += 5
    if bmi >= 30: score += 15
    elif bmi >= 25: score += 7
    if bp >= 140: score += 18
    elif bp >= 130: score += 10
    elif bp >= 120: score += 4
    if heart_rate > 100: score += 10
    elif heart_rate < 50: score += 5
    if glucose >= 126: score += 18
    elif glucose >= 100: score += 7
    if activity < 75: score += 8
    elif activity >= 150: score -= 5
    if smoker: score += 15
    if family: score += 8
    return max(0, min(100, score))

def risk_label(score):
    if score < 30: return "Lower demo score", "#54dfad"
    if score < 60: return "Moderate demo score", "#ffc46b"
    return "Higher demo score", "#ff8295"

def advice_for(values):
    tips=[]
    if values["activity"] < 150:
        tips.append("If appropriate for you, gradually build a regular activity routine.")
    if values["bmi"] >= 25:
        tips.append("Discuss nutrition and weight goals with a qualified healthcare professional.")
    if values["bp"] >= 130:
        tips.append("Recheck blood pressure with a validated device and discuss readings with a clinician.")
    if values["glucose"] >= 100:
        tips.append("Ask a clinician whether glucose testing or follow-up is appropriate.")
    if values["smoker"]:
        tips.append("A healthcare professional can offer evidence-based smoking cessation support.")
    if values["family"]:
        tips.append("Share family history with your healthcare provider.")
    tips.append("Keep routine check-ups and seek urgent care for severe or sudden symptoms.")
    return tips[:5]

# ---------- Pages ----------
if page == "Dashboard":
    st.markdown('<div class="hero"><div class="kicker">SMART HEALTH ANALYTICS</div><div class="hero-title">Your health.<br><span class="gradient">Informed by data.</span></div><p class="hero-sub">Explore a wellness-focused screening estimate using selected health indicators. This academic demo does not diagnose disease.</p></div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    metrics=[("❤️","Heart rate","72 BPM","Illustrative sample"),("🫁","Blood oxygen","98%","Illustrative sample"),("👟","Daily activity","6,240 steps","Sample dashboard data"),("✚","Wellness status","Good","Not a real measurement")]
    for col,(icon,label,value,note) in zip([c1,c2,c3,c4],metrics):
        with col:
            st.markdown(f'<div class="metric-card"><div>{icon} <span class="metric-label">{label}</span></div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',unsafe_allow_html=True)
    st.write("")
    left,right=st.columns([1.15,0.85])
    with left:
        st.markdown("### 📈 Sample wellness trends")
        sample=pd.DataFrame({"Day":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],"Activity minutes":[25,40,30,55,35,65,45],"Sleep hours":[7.1,6.8,7.5,7.0,7.7,8.0,7.4]})
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=sample.Day,y=sample["Activity minutes"],mode="lines+markers",name="Activity minutes",line=dict(color="#43e5e8",width=3)))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#bcd0e5",height=320,margin=dict(l=10,r=10,t=20,b=10),yaxis_title="Minutes",xaxis=dict(showgrid=False),yaxis=dict(gridcolor="#20384e"))
        st.plotly_chart(fig,use_container_width=True)
    with right:
        st.markdown("### 🧬 Health indicators")
        fig2=go.Figure(go.Bar(x=["Sleep","Activity","Hydration","Nutrition"],y=[72,65,80,70],marker_color=["#43e5e8","#5c8cff","#54dfad","#a27bff"]))
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#bcd0e5",height=320,margin=dict(l=10,r=10,t=20,b=10),yaxis=dict(range=[0,100],gridcolor="#20384e"),xaxis=dict(showgrid=False),showlegend=False)
        st.plotly_chart(fig2,use_container_width=True)
    st.info("The cards and charts on this dashboard contain illustrative values. They are not live wearable data or medical measurements.")
    st.markdown("### Start a screening demo")
    st.write("Use the sidebar to open **Health Risk Assessment** and enter example health indicators.")

elif page == "Health Risk Assessment":
    st.markdown('<div class="kicker">PERSONALIZED SCREENING DEMO</div><h1>Health risk <span class="gradient">assessment</span></h1>',unsafe_allow_html=True)
    st.write("Enter the sample values below to see how the educational scoring logic responds. Values stay in this app session.")
    with st.form("health_form"):
        c1,c2,c3=st.columns(3)
        age=c1.number_input("Age (years)",min_value=18,max_value=100,value=35)
        bmi=c2.number_input("BMI (kg/m²)",min_value=10.0,max_value=60.0,value=24.5,step=0.1)
        bp=c3.number_input("Systolic blood pressure (mmHg)",min_value=70,max_value=250,value=120)
        c4,c5,c6=st.columns(3)
        heart_rate=c4.number_input("Resting heart rate (BPM)",min_value=35,max_value=220,value=72)
        glucose=c5.number_input("Glucose (mg/dL)",min_value=40,max_value=500,value=95)
        activity=c6.number_input("Weekly activity (minutes)",min_value=0,max_value=1000,value=150)
        c7,c8=st.columns(2)
        smoker=c7.checkbox("Current smoker")
        family=c8.checkbox("Family history of chronic disease")
        submitted=st.form_submit_button("✨ Calculate demo score",use_container_width=True)
    if submitted:
        values={"age":age,"bmi":bmi,"bp":bp,"heart_rate":heart_rate,"glucose":glucose,"activity":activity,"smoker":smoker,"family":family}
        score=calculate_demo_score(age,bmi,bp,heart_rate,glucose,activity,smoker,family)
        label,color=risk_label(score)
        st.divider()
        a,b=st.columns([0.75,1.25])
        with a:
            fig=go.Figure(go.Indicator(mode="gauge+number",value=score,title={"text":"DEMO SCORE","font":{"color":"#9bb2ca","size":16}},gauge={"axis":{"range":[0,100],"tickcolor":"#9bb2ca"},"bar":{"color":color},"bgcolor":"#10243a","bordercolor":"#213a54","steps":[{"range":[0,30],"color":"#183c37"},{"range":[30,60],"color":"#493a28"},{"range":[60,100],"color":"#482b38"}]}))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font_color="#eaf3ff",height=300,margin=dict(l=15,r=15,t=35,b=10))
            st.plotly_chart(fig,use_container_width=True)
        with b:
            st.markdown(f"### <span style='color:{color}'>{label}</span>",unsafe_allow_html=True)
            st.write("This category reflects only the simplified demonstration formula and should not be interpreted as a medical risk estimate.")
            st.markdown("#### General wellness prompts")
            for tip in advice_for(values):
                st.markdown(f"- {tip}")
        st.warning("Educational prototype only. This score is not clinically validated, does not diagnose disease and must not be used for treatment decisions. Consult a qualified healthcare professional for health concerns.")
    else:
        st.markdown('<div class="panel"><h3>🧾 Your result will appear here</h3><p style="color:#9bb2ca">Submit the form to calculate a transparent, non-clinical demo score.</p></div>',unsafe_allow_html=True)

elif page == "Health Insights":
    st.markdown('<div class="kicker">HEALTH INSIGHTS</div><h1>Small steps, <span class="gradient">better habits</span></h1>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    cards=[("🏃","Move regularly","Build toward regular physical activity that fits your ability and medical advice."),("🩺","Know your numbers","Track measurements using appropriate devices and discuss trends with a clinician."),("✨","Healthy routines","Prioritize sleep, balanced meals, hydration and stress management.")]
    for col,(icon,title,desc) in zip([c1,c2,c3],cards):
        with col:
            st.markdown(f'<div class="metric-card"><div style="font-size:1.7rem">{icon}</div><h3>{title}</h3><p style="color:#9bb2ca">{desc}</p></div>',unsafe_allow_html=True)
    st.markdown("### Common indicators")
    st.dataframe(pd.DataFrame({"Indicator":["Blood pressure","BMI","Glucose","Resting heart rate"],"Unit":["mmHg","kg/m²","mg/dL","BPM"],"Reminder":["Interpret with clinician guidance","Does not describe body composition","Context and testing matter","Varies by individual and circumstances"]}),use_container_width=True,hide_index=True)

else:
    st.markdown('<div class="kicker">PROJECT OVERVIEW</div><h1>About <span class="gradient">HealthPulse AI</span></h1>',unsafe_allow_html=True)
    st.markdown("### Smart Healthcare Prediction System")
    st.write("HealthPulse AI is an academic demonstration of a responsive healthcare dashboard and a transparent rule-based scoring interface.")
    st.markdown("**Technology stack**")
    st.write("Python · Streamlit · Pandas · Plotly · HTML/CSS styling")
    st.markdown("**Project features**")
    st.markdown("- Interactive health profile form\n- Demo risk score and category\n- Conditional wellness prompts\n- Dashboard charts\n- Mobile-friendly layout\n- GitHub and Render deployment")
    st.markdown("**Optional ML workflow**")
    st.write("A separate training script can use a synthetic CSV dataset to demonstrate model training and evaluation. Synthetic data is not clinical evidence.")
    st.markdown("**Disclaimer**")
    st.error("This project is not a medical device, clinical decision-support system or validated prediction model. It is for educational demonstration only. Do not use it for diagnosis or treatment.")
