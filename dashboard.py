
import streamlit as st
from pathlib import Path



st.set_page_config(
    page_title="AI Border Surveillance",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI Border Surveillance System")
st.caption("AI-Based Intelligent Video Analytics for Border Monitoring")

st.divider()

# System overview
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("System", "ONLINE")

with col2:
    st.metric("AI Model", "YOLO11n")

with col3:
    st.metric("Camera", "ACTIVE")

with col4:
    st.metric("Threat Level", "NORMAL")

st.divider()

# Main surveillance area
left, right = st.columns([2, 1])

with left:
    st.subheader("📹 Surveillance Feed")

    st.info(
        "Live CCTV/Camera feed is processed by the AI detection module."
    )

    st.markdown("""
    ### Detection Pipeline

    **Camera → YOLO11n → Person Detection → Tracking → Restricted Zone**
    """)

with right:
    st.subheader("🚨 Security Status")

    st.success("SYSTEM OPERATIONAL")

    st.write("👤 Persons detected: Monitoring")
    st.write("📍 Restricted zone: Active")
    st.write("🤖 AI detection: Running")

st.divider()

# Security events
st.subheader("🚨 Security Events")

alert_file = Path("alerts.txt")

if alert_file.exists():

    alerts = alert_file.read_text(
        encoding="utf-8"
    ).strip()

    if alerts:

        for alert in reversed(alerts.splitlines()):
            st.error(alert)

    else:
        st.success("No intrusion events recorded.")

else:
    st.success("No intrusion events recorded.")

st.divider()

st.subheader("💡 How the Prototype Works")

st.write(
    "The system uses an existing camera/CCTV feed, "
    "detects people using YOLO11n, assigns tracking IDs, "
    "checks whether a person enters a predefined restricted zone, "
    "and records an intrusion event with a timestamp."
)