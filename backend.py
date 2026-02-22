import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

# Langchain Imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

# ==========================================
# 1. SERVER SETUP
# ==========================================
app = FastAPI(title="Scholara API Engine")

# This allows your Chrome Extension to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 2. SCHEMA DEFINITION
# ==========================================
class StudentProfile(BaseModel):
    name: str = Field(description="The student's full name")
    major: str = Field(description="The student's degree and major")
    current_year: str = Field(description="The student's current year of study (e.g., 1st Year, 2nd Year)")
    cgpa: float = Field(description="The student's current CGPA as a decimal")
    annual_family_income: int = Field(description="The student's annual family income in INR. Extract just the number.")
    category: str = Field(description="The student's category or caste")
    volunteer_hours: int = Field(description="Total logged volunteer hours. If none, return 0.")
    technical_skills: List[str] = Field(description="List of technical skills and software")

# ==========================================
# 3. GLOBAL ENGINE INITIALIZATION
# ==========================================
print("1. Loading Scholarship PDF and building Vector Database...")
rule_loader = PyPDFLoader("pec_guidelines.pdf")
chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150).split_documents(rule_loader.load())

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

print("2. Connecting to MegaLLM...")
MEGALLM_API_KEY = "sk-mega-2f0a3b23154fc9ff152021a43649647884c0222100f07f8c2ab126cf6f3241c2" 
llm = ChatOpenAI(
    base_url="https://ai.megallm.io/v1",
    api_key=MEGALLM_API_KEY,
    model="mistralai/mistral-nemotron", 
    temperature=0 
)

print("3. Analyzing Student CV...")
cv_loader = PyPDFLoader("mock_cv.pdf")
cv_text = "\n".join([page.page_content for page in cv_loader.load()])

structured_llm = llm.with_structured_output(StudentProfile)
extracted_profile = structured_llm.invoke(f"Extract the profile:\n\n{cv_text}")
student_cv_text = json.dumps(extracted_profile.model_dump(), indent=2)

print("4. Linking Neural Pathways...")
system_prompt = (
    "You are the Scholara AI Advisor. You are talking to a specific student.\n"
    "--- STUDENT PROFILE ---\n"
    "{student_profile}\n"
    "-----------------------\n\n"
    "Use the provided context from the official scholarship guidelines to answer their questions.\n"
    "RULES:\n"
    "1. Give a direct, accurate answer tailored to their CV.\n"
    "2. If they are not eligible, perform a 'Gap Analysis' explaining exactly what they need to improve.\n"
    "3. Always cite the specific rule you are pulling from the PDF.\n\n"
    "Context from PDF Guidelines:\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "Previous Conversation:\n{chat_history}\n\nNew Question: {input}"),
])

rag_chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))
print(f"✅ Scholara Engine Ready! Logged in as: {extracted_profile.name}")

# In-memory chat history for the API
chat_memory = ""

# ==========================================
# 4. API ENDPOINTS
# ==========================================

# Endpoint 1: Standard Chat (Uses the PEC PDF RAG)
class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    global chat_memory
    try:
        response = rag_chain.invoke({
            "input": req.query,
            "student_profile": student_cv_text, 
            "chat_history": chat_memory
        })
        
        chat_memory += f"Student: {req.query}\nScholara: {response['answer']}\n\n"
        return {"status": "success", "answer": response["answer"]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint 2: Chrome Extension Web Scraper (Uses the live website text)
class WebsiteRequest(BaseModel):
    website_text: str

@app.post("/analyze_website")
async def analyze_website(req: WebsiteRequest):
    try:
        safe_text = req.website_text[:15000] 

        prompt = f"""
        You are Scholara AI. Read the text scraped from a university admissions webpage.
        
        WEBSITE TEXT:
        {safe_text}
        
        STUDENT PROFILE:
        {student_cv_text}
        
        TASK:
        Check if the student is eligible based ONLY on the webpage text. 
        Return a short JSON with exactly two keys:
        'status': "ELIGIBLE", "NOT_ELIGIBLE", or "NEED_MORE_INFO"
        'reason': A short 2-sentence explanation of why.
        """
        
        response = llm.invoke(prompt)
        clean_json = response.content.replace("```json", "").replace("```", "").strip()
        
        return json.loads(clean_json)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# 5. START SERVER
# ==========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)