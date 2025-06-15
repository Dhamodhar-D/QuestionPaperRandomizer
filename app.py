from flask import Flask, request, render_template, send_from_directory
from parser import extract_questions
from randomizer import generate_question_sets
from generator import generate_pdf
from utils import zip_output_pdfs
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    download_link = None

    if request.method == "POST":
        uploaded_file = request.files["pdf_file"]
        num_papers = int(request.form["num_papers"])

        filename = secure_filename(uploaded_file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(input_path)

        questions = extract_questions(input_path)
        sets = generate_question_sets(questions, num_papers)

        for file in os.listdir(OUTPUT_FOLDER):
            os.remove(os.path.join(OUTPUT_FOLDER, file))

        for i, question_set in enumerate(sets):
            path = os.path.join(OUTPUT_FOLDER, f"question_paper_{i+1}.pdf")
            generate_pdf(question_set, path)

        zip_path = zip_output_pdfs(OUTPUT_FOLDER)
        download_link = f"/download/{os.path.basename(zip_path)}"

    return render_template("index.html", download_link=download_link)

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)  # intranet-compatible
