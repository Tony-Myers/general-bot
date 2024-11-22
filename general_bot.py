import streamlit as st
import openai
from PyPDF2 import PdfReader


# Retrieve password and OpenAI API key from Streamlit secrets
PASSWORD = st.secrets["password"]
OPENAI_API_KEY = st.secrets["openai_api_key"]

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY
# Password Authentication
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # delete password from session_state
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input("Enter password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Enter password", type="password", on_change=password_entered, key="password")
        st.error("Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    st.title("ChatGPT Document Analyzer")

    # Function to extract text from PDF
    def extract_text_from_pdf(file):
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
       
    uploaded_file = st.file_uploader("Choose a PDF document", type=["pdf"])

    text = ""

# If a file is uploaded, extract text and display success message
if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)
    st.success("File uploaded and text extracted successfully.")

# Display the prompt input box
prompt = st.text_area("Enter your prompt", height=200)

                    
def call_chatgpt(prompt):
    """Calls the OpenAI API and returns the response as text."""
    try:
        response = client.chat.completions.create(
            model='gpt-4o',  # Replace with your model
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

