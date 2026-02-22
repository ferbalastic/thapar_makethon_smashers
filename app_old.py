import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os


# from langchain_openai import ChatOpenAI
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_classic.chains.summarize import load_summarize_chain
# from langchain_core.prompts import PromptTemplate


# LANGCHAIN PART!!!
# llm = ChatOpenAI(
#     base_url="https://ai.megallm.io/v1",
#     api_key="sk-mega-2f0a3b23154fc9ff152021a43649647884c0222100f07f8c2ab126cf6f3241c2",
#     model="mistralai/mistral-nemotron"
# )
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# def process_and_save_pdf(pdf_path, index_name):
#     """Loads PDF, splits it, and saves a FAISS index."""
#     loader = PyPDFLoader(pdf_path)
#     pages = loader.load()
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
#     chunks = text_splitter.split_documents(pages)
    
#     vector_db = FAISS.from_documents(chunks, embeddings)
#     vector_db.save_local(index_name)
#     return chunks

# def analyze_scholarship_doc(chunks):
#     """Analyzes the whole document to extract all requirements."""
#     initial_prompt = PromptTemplate.from_template("Extract all scholarship rules from: {text}")
#     refine_prompt = PromptTemplate.from_template("Existing list: {existing_answer}\nNew text: {text}\nUpdate list:")
    
#     chain = load_summarize_chain(
#         llm=llm, chain_type="refine", 
#         question_prompt=initial_prompt, refine_prompt=refine_prompt
#     )
#     result = chain.invoke(chunks)
#     return result["output_text"]

# def check_user_eligibility(user_data, index_name):
#     """Checks user data against a specific saved FAISS index."""
#     vector_db = FAISS.load_local(index_name, embeddings, allow_dangerous_deserialization=True)
    
#     # Context-aware search
#     query = f"Criteria for {user_data.get('course')} income {user_data.get('income')}"
#     docs = vector_db.similarity_search(query, k=5)
#     context = "\n\n".join([d.page_content for d in docs])
    
#     prompt = f"""
#     Analyze eligibility for {user_data['name']}.
#     User Info: {user_data}
#     Scholarship Context: {context}
#     Return result in JSON format with keys: 'eligible' (bool), 'reasons' (list), 'missing_docs' (list).
#     """
#     response = llm.invoke(prompt)
#     return response.content


# -------------------------
# Basic Config
# -------------------------

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------
# Routes
# -------------------------

@app.route("/analyze")
def analyze():
    return render_template("analyze.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "pdf" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["pdf"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # TODO: Call your ingestion pipeline here
        # ingest_pdf(filepath)

        return jsonify({"message": "PDF uploaded successfully!"})

    return jsonify({"error": "Invalid file type"}), 400

@app.route("/pdf")
def pdfchecker():
    return render_template('uploadpdf.html')

@app.route("/summarize", methods=["POST"])
def summarize():
    file = request.files['pdf']

    # if file.filename == "":
    #     return jsonify({"error": "No file selected"}), 400

    # filename = secure_filename(file.filename)
    # filepath = os.path.join("uploads", filename)

    # file.save(filepath)
    # return jsonify({analyze_scholarship_doc(process_and_save_pdf(filepath, 0))})
    # os.remove(filepath)

    return jsonify({"summary":"processed successfully"})
    
# should change this, will break if multiple users use the app
user_details = []


@app.route('/chatting', methods=["GET", "POST"])
def chatting():

    if request.method == "POST":
        user_data = request.json

        return jsonify({"redirect": "/chatting"})

    return render_template('chat.html')

@app.route("/upload_cv", methods=["POST"])
def upload_cv():
    file = request.files["cv"]

    # TODO: Extract CV data using PyPDFLoader
    # Run RAG eligibility

    return jsonify({"result": "CV processed successfully"})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    user_data = session.get("user_details", {})

    
    return jsonify({
        "reply": f"User profile: {user_data}\nAI Response to: {user_message}"
    })

@app.route("/ask", methods=["POST"])
def ask():
    user_data = request.json
    index_name = 0

    # result = check_user_eligibility(user_data, index_name)

    return jsonify({"result": "result"})



# -------------------------
# Run
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)