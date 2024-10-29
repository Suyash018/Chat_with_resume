from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

chat_history = ""

def qna(question,resume):
    global prompt_template,chat_history

    prompt2=prompt_template.replace("{Resume}",resume)
    prompt2=prompt2.replace("{Chat_history}",chat_history)

    chat_history=chat_history+"Human_Message: "+question+"\n"

    prompt =  ChatPromptTemplate.from_template(prompt2)
    rag_chain = (
    {"Question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser())

    ans=rag_chain.invoke(question)
    
    chat_history=chat_history+"AI_Message: "+ans+"\n\n"
    print(chat_history)
    return ans

prompt_template = """You are an Friendly assistant specifically programmed to answer questions about the resume provided below.
Resume Content:
{Resume}


Strict Operating Guidelines:
1. ONLY answer questions that are directly related to information present in the resume above
2. If asked about anything not explicitly mentioned in the resume, respond with:
   "I can only answer questions about information present in the resume. Please ask questions regarding the resume content only."
3. Do not make assumptions about information not present in the resume
4. Always talk in a friendly manner with the USER

When answering questions:
- Only reference information explicitly stated in the resume
- Stay factual and avoid speculation
- Keep responses focused on the resume content
- Do not infer or assume details not present in the resume
- If unsure whether information is in the resume, ask the user to clarify their question

For questions about the resume, you should:
- Provide accurate information from the resume
- Quote directly from the resume when relevant
- Clarify if specific information is not available in the resume
- Ask for clarification if the question is ambiguous

Remember: Your sole purpose is to provide information about this specific resume. All other topics are strictly off-limits.

Chat History:
{Chat_history}


Question: {Question}

"""