import streamlit as st
import openai
from openai import OpenAI
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

    # Function to extract text from the uploaded PDF


# Instantiate the OpenAI client
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def call_chatgpt(prompt):
    """Calls the OpenAI API using the latest client library and returns the response."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"



# Function to extract text from the uploaded PDF
def extract_text_from_pdf(uploaded_file):
    # Implement your PDF text extraction logic here
    return "Extracted text from PDF"

# Function to call ChatGPT with the provided prompt
def call_chatgpt(prompt):
    # Implement your API call to ChatGPT here
    return f"Response from ChatGPT for prompt: {prompt}"

# File uploader widget
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Initialize 'text' variable
text = ""

# If a file is uploaded, extract text and display success message
if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)
    st.success("File uploaded and text extracted successfully.")
else:
    st.warning("Please upload a PDF file to proceed.")

# Display the prompt input box
prompt = st.text_area("Enter your prompt", height=200)

# Process the combined prompt when the button is clicked
if st.button("Process"):
    with st.spinner("Processing..."):
        full_prompt = prompt + "\n\n" + text
        response = call_chatgpt(full_prompt)
        if response:
            st.write(response)

                    

