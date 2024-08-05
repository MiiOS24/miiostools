import os
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
import bcrypt

# Load environment variables
load_dotenv()

# Debugging: Print environment variables to ensure they are loaded
print("NAME:", os.getenv("NAME"))
print("PASSWORD:", os.getenv("PASSWORD"))

# Load credentials from environment variables
NAME = os.getenv("NAME")
PASSWORD = os.getenv("PASSWORD")

# Check if environment variables are loaded correctly
if NAME is None or PASSWORD is None:
    raise ValueError("Environment variables NAME and PASSWORD must be set")

# Ensure PASSWORD is in bytes
PASSWORD_BYTES = PASSWORD.encode('utf-8')

# Hash the password
hashed_password = bcrypt.hashpw(PASSWORD_BYTES, bcrypt.gensalt())

# User credentials (hashed password for security)
USER_CREDENTIALS = {
    NAME: hashed_password
}

# Authenticate user
def authenticate(email, password):
    if email in USER_CREDENTIALS:
        # Convert the input password to bytes and compare
        return bcrypt.checkpw(password.encode('utf-8'), USER_CREDENTIALS[email])
    return False

# Login function
def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(email, password):
            st.session_state['authenticated'] = True
            st.session_state['user'] = email
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid email or password")
            st.session_state['authenticated'] = False

# Main function to run the app
def main():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        login()
    else:
        # Sidebar for navigation
        st.sidebar.title("🧰 MiiOS Toolbox")
        st.sidebar.write("Your Pocket-Sized Team for Everyday Tasks Powering Your Research Journey")

        # Navigation using the radio button
        page = st.sidebar.radio("Go to", [
            "💡 Info",
            "📝 SurveyBuilder (soon)",  
            "🧼 betterDATA",
            "🏷️ autoCODE beta",
            "☢️ Bad Ids",  
            "🎙️ Whisper",
            "🤖 Interview Bot",
            "✍️ goethe",
            "👤 PersonaBot (soon)",
            "🚀 Onboarding (soon)",
            "📚 Knowledge Now (soon)",
            "🔢 Madde Hours"
        ])

        # Navigation
        if page == "💡 Info":
            base_page()
        elif page == "📝 SurveyBuilder (soon)":
            survey_builder_page()
        elif page == "🧼 betterDATA":
            better_data_page()
        elif page == "🏷️ autoCODE beta":
            auto_code_tool_page()
        elif page == "☢️ Bad Ids":
            bad_ids_page()
        elif page == "🎙️ Whisper":
            whisper_page()
        elif page == "🤖 Interview Bot":
            interview_bot_page()
        elif page == "✍️ goethe":
            goethe_page()
        elif page == "👤 PersonaBot (soon)":
            persona_bot_page()
        elif page == "🚀 Onboarding (soon)":
            onboarding_page()
        elif page == "📚 Knowledge Now (soon)":
            knowledge_manager_page()
        elif page == "🔢 Madde Hours":
            maddehours_page()

        # Footer
        st.write("\n\n")
        current_date = datetime.now().strftime("%d.%m.%Y")
        st.markdown(f"<div style='color: grey; text-align: center;'>🤖 MiiOS Toolbox | {current_date}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
