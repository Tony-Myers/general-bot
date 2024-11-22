import streamlit as st
import openai
import io
from PyPDF2 import PdfReader
from docx import Document
from warnings import PendingDeprecationWarning


# Set OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]
client = openai

# Password Authentication
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["passwords"]["app_password"]:
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
        return text

    # Function to extract text from DOCX
    def extract_text_from_docx(file):
        doc = Document(file)
        text = ''
        for para in doc.paragraphs:
            text += para.text + '\n'
        return text

    # Function to call ChatGPT
    def call_chatgpt(prompt, model="gpt-4", max_tokens=500, temperature=0.6, retries=2):
        """Calls the OpenAI API and returns the response as text."""
        try:
             client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="model,
            messages=messages,
            max_tokens= max_tokens,
            n=1,
            temperature=0.6,
        )
            content = response.choices[0].message.content
        # Your code that may raise exceptions
        return content
    except SpecificExceptionType as e:
        st.error(f"A specific error occurred: {e}")
        logging.error(f"SpecificExceptionType: {e}")
        return None
    except AnotherExceptionType as e:
        st.error(f"Another error occurred: {e}")
        logging.error(f"AnotherExceptionType: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected error: {e}")
        return None
    finally:
        # Perform any necessary cleanup here
        pass

    uploaded_file = st.file_uploader("Choose a PDF or Word document", type=["pdf", "docx"])

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(uploaded_file)
        else:
            st.error("Unsupported file type.")
            st.stop()
        
        st.success("File uploaded and text extracted successfully.")
        # Optionally display the extracted text
        # st.write(text)
        
        prompt = st.text_area("Enter your prompt", height=200)

        if st.button("Process"):
            with st.spinner("Processing..."):
                full_prompt = prompt + "\n\n" + text
                response = call_chatgpt(full_prompt)
                if response:
                    st.write(response)
