import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# LangChain
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# -------------------------
# Flask Setup
# -------------------------

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -------------------------
# 🔥 GLOBAL HACKATHON STATE
# -------------------------

user_details = {}
chat_history = []

# -------------------------
# 🔥 Initialize AI Once
# -------------------------

llm = ChatOpenAI(
    base_url="https://ai.megallm.io/v1",
    api_key="YOUR_HARDCODED_KEY",
    model="mistralai/mistral-nemotron"
)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load FAISS index (make sure it exists)
vector_db = FAISS.load_local(
    "scholarship_faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# Build Retrieval Chain
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Scholara AI. Use the scholarship guidelines context to answer accurately.\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

document_chain = create_stuff_documents_chain(llm, chat_prompt)

chatbot_chain = create_retrieval_chain(
    vector_db.as_retriever(search_kwargs={"k": 5}),
    document_chain
)

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    return render_template("analyze.html")


# -------------------------
# Eligibility Check
# -------------------------

@app.route("/ask", methods=["POST"])
def ask():
    global user_details, chat_history

    user_details = request.json
    chat_history = []

    query = f"Eligibility criteria for {user_details.get('major')} students"
    docs = vector_db.similarity_search(query, k=5)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
    Compare USER PROFILE against GUIDELINES.

    USER PROFILE:
    {user_details}

    GUIDELINES:
    {context}

    1. State if ELIGIBLE or NOT ELIGIBLE.
    2. List reasons.
    3. Mention missing criteria.
    """

    response = llm.invoke(prompt)

    # preload memory for chat
    chat_history.append(("human", "Am I eligible?"))
    chat_history.append(("assistant", response.content))

    return jsonify({"result": response.content})


# -------------------------
# Chat Page
# -------------------------

@app.route("/chatting")
def chatting():
    return render_template("chat.html")


# -------------------------
# Chat API
# -------------------------

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history

    user_message = request.json.get("message")

    response = chatbot_chain.invoke({
        "input": user_message,
        "chat_history": chat_history
    })

    answer = response["answer"]

    chat_history.append(("human", user_message))
    chat_history.append(("assistant", answer))

    return jsonify({"reply": answer})


# -------------------------
# Upload New Scholarship PDF
# -------------------------

@app.route("/upload", methods=["POST"])
def upload_pdf():
    file = request.files["pdf"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    loader = PyPDFLoader(filepath)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(pages)

    new_vector_db = FAISS.from_documents(chunks, embeddings)
    new_vector_db.save_local("scholarship_faiss_index")

    return jsonify({"message": "Scholarship PDF processed successfully"})


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)