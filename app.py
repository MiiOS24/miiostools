import streamlit as st
from datetime import datetime
from maddehours import maddehours_page

# Import your custom pages
from base import base_page
from interview_bot import interview_bot_page
from better_data import better_data_page
from goethe import goethe_page
from auto_code import auto_code_tool_page
from whisper import whisper_page
from survey_builder import survey_builder_page
from bad_ids import bad_ids_page
from onboarding import onboarding_page
from knowledge_manager import knowledge_manager_page
from persona_bot import persona_bot_page
from binary_coding_page import binary_coding_page  # Import the new page

# Main function to run the app
def main():
    # Sidebar for navigation
    st.sidebar.title("🧰 MiiOS Toolbox")
    st.sidebar.write("Your Pocket-Sized Team for Everyday Tasks Powering Your Research Journey")

    # Navigation using the radio button
    page = st.sidebar.radio("Go to", [
        "💡 Info",
        "📝 SurveyBuilder (soon)",  
        "🧼 betterDATA",
        "🏷️ autoCODE beta",
        "🗃️ manuCODE",  # New page placed right under autoCODE
        "☢️ Bad Ids",  
        "🎙️ Whisper",
        "🤖 Interview Bot",
        "✍️ goethe",
        "👤 PersonaBot (soon)",
        "🚀 Onboarding (soon)",
        "📚 Knowledge Now (soon)",
        "🔢 Madde"
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
    elif page == "🗃️ manuCODE":  # New page handler
        binary_coding_page()
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
    elif page == "🔢 Madde":
        maddehours_page()

    # Footer
    st.write("\n\n")
    current_date = datetime.now().strftime("%d.%m.%Y")
    st.markdown(f"<div style='color: grey; text-align: center;'>🤖 MiiOS Toolbox | {current_date}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
