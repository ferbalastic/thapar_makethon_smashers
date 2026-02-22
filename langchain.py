import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
# In 2026, this is the most likely location for legacy chains
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate

# 1. Load and Split (Your existing logic)
loader = PyPDFLoader("scholarship_guidelines_20-21-1.pdf")
pages = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000, # Larger chunks for better extraction context
    chunk_overlap=200
)
chunks = text_splitter.split_documents(pages)


# Now 'chunks' is ready to be sent to your Vector Store (FAISS/Chroma)

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Initialize the Embedding Model (Free & Local)
# This converts text into 384-dimensional numbers
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Create the Vector Database from your chunks
# 'chunks' is the variable from your previous PDF splitting code
print("Generating embeddings... this might take a minute.")
vector_db = FAISS.from_documents(chunks, embeddings)

# 3. Save it locally so you don't have to re-process the PDF every time
vector_db.save_local("scholarship_faiss_index")
print("Vector database saved to 'scholarship_faiss_index' folder.")

# 4. Quick Test: Try a search
query = "What is the eligibility for the scholarship?"
docs = vector_db.similarity_search(query, k=6)

print("\n--- Top Result Found ---")
print(docs[0].page_content[:500])

# 2. Setup the LLM (Gemini 1.5 Flash is great for this)
# Replace with your actual API Key or set as environment variable
llm = ChatOpenAI(
    base_url="https://ai.megallm.io/v1",
    api_key="sk-mega-2f0a3b23154fc9ff152021a43649647884c0222100f07f8c2ab126cf6f3241c2", # Your key from line 9
    model="mistralai/mistral-nemotron" 
)

# 3. Define the Extraction Prompts
# This prompt runs on the very first chunk
initial_prompt_template = """
You are an AI specialized in analyzing scholarship documents.
Below is the first part of a document. Extract all eligibility requirements, 
rules, income limits, and academic criteria.

TEXT: "{text}"

EXTRACTED REQUIREMENTS (Bullet points):"""

# This prompt runs on every subsequent chunk to "refine" the list
refine_template = """
You have a current list of scholarship requirements:
{existing_answer}

Now, look at the following additional part of the document:
------------
{text}
------------

Update the list by adding any NEW requirements found in the text above. 
If the information is already in the list, do not repeat it.
Organize the final output into clear categories like:
- Academic Requirements
- Financial/Income Rules
- Demographic/Category Criteria
- Required Documents

FINAL UPDATED LIST:"""

# Create the prompt objects
INITIAL_PROMPT = PromptTemplate(template=initial_prompt_template, input_variables=["text"])
REFINE_PROMPT = PromptTemplate(template=refine_template, input_variables=["existing_answer", "text"])

# 4. Create and Run the Chain
print(f"Analyzing {len(chunks)} chunks for all requirements...")
chain = load_summarize_chain(
    llm=llm,
    chain_type="refine",
    question_prompt=INITIAL_PROMPT,
    refine_prompt=REFINE_PROMPT,
    verbose=False
)

# This will loop through every chunk and build the final list
# full_requirements_list = chain.invoke(chunks)
full_requirements_list = chain.invoke(docs)
print("\n=== MASTER SCHOLARSHIP REQUIREMENTS ===")
print(full_requirements_list["output_text"])


# Dummy user based on your current project context
user_profile = {
    "name": "Vikas Lochab",
    "course": "B.Tech Electrical Engineering",
    "current_year": "2nd Year",
    "cgpa": 7.2,
    "annual_family_income": 450000, # 4.5 LPA
    "category": "General",
    "state": "Punjab",
    "city": "Chandigarh"
}

# 5. Search for rules relevant to the user's profile
# We search for terms that specifically matter to this user
search_query = f"Eligibility criteria for {user_profile['course']} students with income {user_profile['annual_family_income']}"
relevant_docs = vector_db.similarity_search(search_query, k=5)
context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

# 6. Final Eligibility Prompt
eligibility_prompt = f"""
You are an expert Scholarship Eligibility Officer. 
Compare the USER PROFILE against the PROVIDED GUIDELINES.

USER PROFILE:
- Course: {user_profile['course']}
- Year: {user_profile['current_year']}
- CGPA: {user_profile['cgpa']}
- Income: ₹{user_profile['annual_family_income']}
- Category: {user_profile['category']}

GUIDELINES FROM PDF:
{context_text}

TASK:
1. State clearly if the user is ELIGIBLE or NOT ELIGIBLE.
2. List the specific rules that the user meets.
3. Highlight any 'Gaps' (reasons for ineligibility).
4. If eligible, list the next steps/documents required.
"""

print("\n--- Performing Eligibility Analysis ---")
verdict = llm.invoke(eligibility_prompt)
print(verdict.content)

# ==========================================
# PHASE 5: INTERACTIVE CHATBOT WITH MEMORY
# ==========================================

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. Define the Chat Prompt
# This MUST have {context}, {input}, and the chat_history placeholder
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Scholara AI, an expert scholarship assistant. Use the following context from the official guidelines to answer the student's questions accurately: \n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

# 2. Build the Document Chain 
# (This automatically maps your PDF chunks to the {context} variable)
document_chain = create_stuff_documents_chain(llm, chat_prompt)

# 3. Build the Retrieval Chain
# (This links your FAISS vector_db to the document chain)
chatbot_chain = create_retrieval_chain(vector_db.as_retriever(search_kwargs={"k": 5}), document_chain)

# 4. The Interactive Loop
if __name__ == "__main__":
    print("\n✅ Scholara Intelligence Engine Ready!")
    print("--------------------------------------------------")
    
    # 🧠 THE MAGIC FIX: Pre-load the memory!
    # We pass the user_profile and the exact 'verdict' generated in Phase 6 into the history.
    # Now the bot "remembers" the eligibility check before the user even speaks.
    chat_history = [
        ("human", f"Hi, I am {user_profile['name']}. My profile: Course: {user_profile['course']}, CGPA: {user_profile['cgpa']}, Income: {user_profile['annual_family_income']}. Am I eligible?"),
        ("assistant", verdict.content) 
    ] 
    
    print(f"Scholara AI: Hello {user_profile['name']}! I have analyzed your profile against the scholarship guidelines. Feel free to ask me why you are or aren't eligible, or any other questions.")
    
    while True:
        student_query = input("\nStudent: ").strip()
        
        if student_query.lower() in ["exit", "quit", "q"]:
            print(f"\nScholara AI: Good luck with your studies, {user_profile['name']}! Goodbye 👋")
            break
        if not student_query: continue
            
        print("Scholara AI is checking history and PDF rules...\n")
        
        try:
            # We use chatbot_chain.invoke and pass BOTH 'input' and 'chat_history'
            response = chatbot_chain.invoke({
                "input": student_query,
                "chat_history": chat_history
            })
            
            # The modern chain returns the actual response string in the "answer" key
            output = response["answer"]
            
            # Update history with the new exchange so it remembers follow-up questions
            chat_history.extend([
                ("human", student_query),
                ("assistant", output),
            ])
            
            print("🎓 SCHOLARA AI RESPONSE:")
            print(output)
            print("--------------------------------------------------")
            
        except Exception as e:
            print(f"\n⚠️ System Error: {e}")
