import streamlit as st
import openai
import docx2txt
import PyPDF2

# Retrieve password and OpenAI API key from Streamlit secrets
PASSWORD = st.secrets["password"]
OPENAI_API_KEY = st.secrets["openai_api_key"]

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Function to authenticate user
def authenticate():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("Login")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if password == PASSWORD:
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Invalid password.")

# Function to extract text from uploaded file
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfFileReader(uploaded_file)
        text = ""
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extract_text()
        return text
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx2txt.process(uploaded_file)
    else:
        st.error("Unsupported file type.")
        return None

# Function to process text with ChatGPT
def process_with_chatgpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Main application logic
authenticate()

if st.session_state.get("authenticated"):
    st.title("Document Processor with ChatGPT")
    uploaded_file = st.file_uploader("Upload a PDF or Word document", type=["pdf", "docx"])
    if uploaded_file is not None:
        text = extract_text_from_file(uploaded_file)
        if text:
            st.text_area("Extracted Text", text, height=300)
            prompt = st.text_area("Enter your prompt for ChatGPT")
            if st.button("Process with ChatGPT"):
                if prompt:
                    result = process_with_chatgpt(prompt)
                    st.text_area("ChatGPT Response", result, height=300)
                else:
                    st.error("Please enter a prompt.")
