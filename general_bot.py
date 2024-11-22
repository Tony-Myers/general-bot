import streamlit as st
import openai
from openai import OpenAI
from PyPDF2 import PdfReader


# Retrieve password and OpenAI API key from Streamlit secrets
PASSWORD = st.secrets["password"]
client = OpenAI(api_key=st.secrets["openai"]["api_key"])


# Password Authentication
if check_password():
    st.title("ChatGPT Document Analyzer")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    # Initialize 'text' variable
    text = ""

    # If a file is uploaded, extract text and display a success message
    if uploaded_file is not None:
        with st.spinner("Extracting text from the uploaded PDF..."):
            text = extract_text_from_pdf(uploaded_file)
        st.success("File uploaded and text extracted successfully.")
    else:
        st.warning("Please upload a PDF file to proceed.")

    # Display the prompt input box
    prompt = st.text_area("Enter your prompt", height=200)

    # Process the combined prompt when the button is clicked
    if st.button("Process"):
        if prompt.strip():
            with st.spinner("Processing..."):
                full_prompt = prompt + "\n\n" + text
                response = call_chatgpt(full_prompt)
                if response:
                    st.write(response)
        else:
            st.error("Please enter a prompt before processing.")

    # Function to extract text from the uploaded PDF


# Instantiate the OpenAI client
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



def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to call ChatGPT with the provided prompt
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

                    

