import streamlit as st
import docx2txt
from pypdf import PdfReader

from function import resume_summarizer
from chat_rag import qna


# Mantain Sessions
if 'more_than_2_pages' not in st.session_state:
    st.session_state.more_than_2_pages = False

if 'Other_file_type' not in st.session_state:
    st.session_state.Other_file_type = False

if 'chat_start' not in st.session_state:
    st.session_state.chat_start = False

if 'ans' not in st.session_state:
    st.session_state.ans = None

if 'resume' not in st.session_state:
    st.session_state.resume = None



# File Upload buttopn
uploaded_files = st.file_uploader(
    label="Upload PDF files", type=["pdf","docx"], accept_multiple_files=False
)

# Mantain State for reupload
if uploaded_files:
    st.session_state.more_than_2_pages = False
    st.session_state.Other_file_type = False

# Generate Summary from LLM
if st.button('Generate'):
    st.write("Loading... Loading... Loading...")
    st.session_state.more_than_2_pages = False
    st.session_state.Other_file_type = False
    st.session_state.chat_start = False
    st.session_state.ans= None
    st.session_state.resume = None


    try:
        # Check File type to convert to txt
        if uploaded_files.type=="application/pdf":

            with open("temp.pdf", "wb") as f:
                f.write(uploaded_files.getvalue())
            reader = PdfReader('temp.pdf')

            # Resume length Should be less than 2
            if len(reader.pages) > 2:
                st.session_state.more_than_2_pages = True
                st.write("Please upload resume limited to 2 pages")
            elif len(reader.pages) == 2:
                text = (reader.pages[0]).extract_text()+(reader.pages[1]).extract_text()
            else:
                text = (reader.pages[0]).extract_text()

        # if file is docx type
        elif uploaded_files.type=="application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            with open("temp.docx", "wb") as f:
                f.write(uploaded_files.getvalue())
            text = docx2txt.process("temp.docx")

        # if Something else than return error
        else:
            st.session_state.Other_file_type= True
            st.write("Please upload PDF or Docx file format")
    except Exception as e:
        st.session_state.Other_file_type= True
        st.write("File is corrupted. Please upload a good file")

        
    if st.session_state.Other_file_type == False and st.session_state.more_than_2_pages == False:

        try:
            st.session_state.resume=text
            ans=resume_summarizer(text)

            # If file is not resume error
            if ans["is_resume"] == False:
                st.session_state.ans= None
                st.session_state.resume=None
                st.write("Please upload an Resume")

            else:
                st.session_state.ans= ans
        except Exception as e:
            st.write("OH No, We faced an network Error while using the llm api. Please try agaib")


    
# Generate Output
if  st.session_state.ans is not None:
    # Personal Information
    ans=st.session_state.ans
    st.header("Personal Information")
    st.write(f"**First Name:** {ans['First_Name']}")
    st.write(f"**Last Name:** {ans['Last_Name']}")
    st.write(f"**Email Address:** {ans['Email_Address']}")
    st.write(f"**Phone Number:** {ans['Phone_Number']}")

    # Current Position
    st.header("Current Position")
    st.write(ans['Current_Position'])

    # Years of Experience
    st.header("Years of Experience")
    st.write(f"{ans['Years_of_Experience']} years")

    # Education History
    st.header("Education History")
    for education in ans['Education_History']:
        st.write(f"- {education}")

    # Work Experience Summary
    st.header("Work Experience Summary")
    st.write(ans['Work_Experience_Summary'])

    # Skills
    st.header("Skills")
    for skill in ans['Skills']:
        st.write(f"- {skill}")
    
    st.session_state.chat_start = True

# Extra Feature a Simple Chatbot
if st.session_state.chat_start == True:
    resume=st.session_state.resume
    with st.sidebar:
        messages = st.container(height=400)
        messages.chat_message("assistant").write("Hello! How can I assist you today?")
        if prompt := st.chat_input("Ask About the document"):
            messages.chat_message("user").write(prompt)
            messages.chat_message("assistant").write(qna(prompt,resume))






