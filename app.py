import streamlit as st
from twilio.rest import Client
import joblib

# Function to set background color
def set_bg_color(color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize session state
if 'sms_ready' not in st.session_state:
    st.session_state.sms_ready = False

# Sidebar navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Select a page", ["🔐 Twilio SMS Setup", "🌐 URL Phishing Checker"])

# -------- Page 1: SMS Setup --------
if page == "🔐 Twilio SMS Setup":
    st.title("Twilio SMS Setup")

    # Input fields
    st.session_state.account_sid = st.text_input("Enter your Twilio Account SID", type="password")
    st.session_state.auth_token = st.text_input("Enter your Twilio Auth Token", type="password")
    st.session_state.twilio_number = st.text_input("Enter your Twilio Phone Number", type="password")
    st.session_state.your_mobile_number = st.text_input("Enter your Mobile Number to receive SMS", type="password")

    # Check if all are filled
    if (
        st.session_state.account_sid and
        st.session_state.auth_token and
        st.session_state.twilio_number and
        st.session_state.your_mobile_number
    ):
        st.success("✅ SMS setup completed. Now go to 'URL Phishing Checker' page.")
        st.session_state.sms_ready = True
    else:
        st.warning("🔐 Please fill all fields to continue.")

# -------- Page 2: Phishing Checker --------
elif page == "🌐 URL Phishing Checker":
    st.title("Phishing Website Checker")

    if not st.session_state.sms_ready:
        st.warning("⚠️ Please complete Twilio setup first in the 'SMS Setup' page.")
    else:
        # Load model (mock or real model)
        model = joblib.load("phishing_model.pkl")

        # Check phishing logic
        def is_phishing(url):
            return "login" in url or "update" in url

        # URL input
        url = st.text_input("Enter the URL to check")

        if st.button("Check Website"):
            if url:
                if is_phishing(url):
                    set_bg_color("#ffcccc")
                    st.error("⚠️ This might be a phishing website!")
                    client = Client(st.session_state.account_sid, st.session_state.auth_token)
                    client.messages.create(
                        body=f"Warning! {url} may be a phishing website!",
                        from_=st.session_state.twilio_number,
                        to=st.session_state.your_mobile_number
                    )
                    st.success("📩 SMS alert has been sent.")
                else:
                    set_bg_color("#ccffcc")
                    st.success("✅ This might be a safe website.")
            else:
                st.warning("⚠️ Please enter a URL.")
