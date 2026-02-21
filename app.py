import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# -------------------------
# Basic Config
# -------------------------

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------
# Utility Functions
# -------------------------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# !!!
# THIS IS WRONG, CHANGE THIS AND ADD AI
# !!!
def fake_ai_evaluation(profile):
   

    gpa = float(profile.get("gpa", 0))
    income = float(profile.get("income", 0))

    # Demo logic
    if gpa >= 3.5:
        return {
            "eligible": True,
            "reason": "Your GPA meets the minimum requirement of 3.5.",
            "gap_analysis": "None",
            "confidence": 0.92
        }
    else:
        gap = round(3.5 - gpa, 2)
        return {
            "eligible": False,
            "reason": "The scholarship requires a minimum GPA of 3.5.",
            "gap_analysis": f"Increase GPA by {gap} points.",
            "confidence": 0.87
        }


# -------------------------
# Routes
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")


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


@app.route("/ask", methods=["POST"])
def ask():
    profile = request.json
# ADD AI PART HERE
    # TODO:
    # 1. Retrieve relevant chunks from vector DB
    # 2. Send to MegaLLM
    # 3. Return structured JSON

    result = fake_ai_evaluation(profile)

    return jsonify(result)


# -------------------------
# Run
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)