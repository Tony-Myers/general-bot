import streamlit as st
import openai
from PyPDF2 import PdfReader

# Retrieve password and OpenAI API key from Streamlit secrets
PASSWORD = st.secrets["password"]
OPENAI_API_KEY = st.secrets["api_keys"]["openai"]

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["passwords"]["app_password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # delete password from session_state
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Enter password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter password", type="password", on_change=password_entered, key="password")
        st.error("Password incorrect")
        return False
    else:
        return True

if check_password():
    st.title("ChatGPT Document Analyzer")

    # Function to extract text from PDF
    def extract_text_from_pdf(file):
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

    uploaded_file = st.file_uploader("Choose a PDF document", type=["pdf"])

    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        st.success("File uploaded and text extracted successfully.")

        prompt = st.text_area("Enter your prompt", height=200)

        if st.button("Process"):
            with st.spinner("Processing..."):
                full_prompt = prompt + "\n\n" + text
                response = call_chatgpt(full_prompt)
                if response:
                    st.write(response)
