from flask import Flask, jsonify, request
from flask_cors import CORS  # ✅ Add this
from semantic import get_semantic_links, semantic_search, get_persona_highlights
import fitz
import os

app = Flask(__name__)
CORS(app)
# Helper to get absolute path to the PDF
def get_pdf_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "input", "sample.pdf"))

@app.route("/extract-outline")
def extract_outline():
    pdf_path = get_pdf_path()
    doc = fitz.open(pdf_path)
    headings = []
    for page_num in range(len(doc)):
        blocks = doc[page_num].get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if span["size"] > 12:
                        headings.append({"id": f"p{page_num}", "text": span["text"]})
    return jsonify(headings)

@app.route("/semantic-links")
def semantic_links():
    pdf_path = get_pdf_path()
    return jsonify(get_semantic_links(pdf_path))

@app.route("/search")
def search():
    query = request.args.get("q")
    pdf_path = get_pdf_path()
    doc = fitz.open(pdf_path)
    sections = [page.get_text() for page in doc]
    result = semantic_search(query, sections)
    return jsonify(result)

@app.route("/persona")
def persona_view():
    persona = request.args.get("role", "student")
    pdf_path = get_pdf_path()
    doc = fitz.open(pdf_path)
    sections = [page.get_text() for page in doc]
    filtered = get_persona_highlights(sections, persona)
    return jsonify(filtered)

@app.route("/")
def home():
    return "✅ Backend is running!"

if __name__ == "__main__":
    app.run(debug=True)
