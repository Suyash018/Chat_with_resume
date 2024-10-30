from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class JsonFormat(BaseModel):
    First_Name: str = Field(description="First name of the applicant. Set to 'Nan' if not provided.")
    Last_Name: str = Field(description="Last name of the applicant. Set to 'Nan' if not provided.")
    Email_Address: str = Field(description="Email address of the applicant. Set to 'Nan' if not provided.")
    Phone_Number: str = Field(description="Phone number of the applicant. Set to 'Nan' if not provided.")
    Education_History: List[str] = Field(description="List of string of educational qualifications of the applicant . Set to 'Nan' if not provided.")
    Work_Experience_Summary: str = Field(description="Summary of the applicant's work experience. Set to 'Nan' if not provided.")
    Skills: List[str] = Field(description="List of skills possessed by the applicant. Set to 'Nan' if not provided.")
    Current_Position: str = Field(description="Current job position of the applicant. Set to 'Nan' if not provided.")
    Years_of_Experience: float = Field(description="Total years of professional experience of the applicant. Set to 0 if not provided. if applicant has 2 years 6 months experince then answer shoulb be 2.5")
    is_resume: bool= Field(description="True if it is an resume else false")

parser = JsonOutputParser(pydantic_object=JsonFormat)




def resume_summarizer(text):

    prompt =  PromptTemplate.from_template(prompt_template, partial_variables={"format_instructions": parser.get_format_instructions()})
    rag_chain = (
    {"Resume": RunnablePassthrough()}
    | prompt
    | llm
    | JsonOutputParser())

    ans=rag_chain.invoke(text)
    return ans



prompt_template = """You are a smart assistant designed to help extracting info from an resume.

Resume: {Resume}



You need to extract the following
   - First Name
   - Last Name
   - Email Address
   - Phone Number
   - Education History
   - Work Experience Summary
   - Skills
   - Current Position
   - Years of Experience

Output should be in json format as 

    "First_Name" str: "First name of the applicant. Set to 'Nan' if not provided.",
    "Last_Name" str: "Last name of the applicant. Set to 'Nan' if not provided.",
    "Email_Address" str: "Email address of the applicant. Set to 'Nan' if not provided.",
    "Phone_Number" : "Phone number of the applicant. Set to 'Nan' if not provided.",
    "Education_History": "List of string  educational qualifications of the applicant in markdown format. Set to 'Nan' if not provided.",
    "Work_Experience_Summary": "Summary of the applicant's work experience. Set to 'Nan' if not provided.",
    "Skills": "List of skills possessed by the applicant. Set to 'Nan' if not provided.",
    "Current_Position": "Current job position of the applicant. Set to 'Nan' if not provided.",
    "Years_of_Experience": "Total years of professional experience of the applicant. Set to 0 if not provided. If applicant has 2 years 6 months experience, then the answer should be 2.5."
    "is_resume": "True if it is an resume else false"

Important:
 Work_Experience_Summary should be a summary in str format
 Education_History should be a list of string in readable format
"""
