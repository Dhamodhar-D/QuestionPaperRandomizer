import pdfplumber
import re

def extract_questions(pdf_path):
    questions = []

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            lines = page.extract_text().split("\n")
            clean_lines = [line.strip() for line in lines if is_valid_line(line)]
            full_text += "\n".join(clean_lines) + "\n"

    # Normalize multiple line breaks
    full_text = re.sub(r'\n+', '\n', full_text)

    # Split by possible numbered questions
    blocks = re.split(r'\n(?=\d{1,3}\.\s)', full_text)

    for block in blocks:
        block = block.strip()
        if not block or len(block) < 20:
            continue

        # Remove original numbering
        block = re.sub(r'^\d{1,3}\.\s*', '', block)

        # Match options (a)...(d)
        options = re.findall(r'\([a-dA-D]\)\s*[^()]+', block)
        if len(options) < 2:
            continue  # Skip if options are missing or incomplete

        question_text = block.split("(a)")[0].strip()

        questions.append({
            "question": clean_math_text(question_text),
            "options": [clean_math_text(opt.strip()) for opt in options]
        })

    return questions

def is_valid_line(line):
    return not any(skip in line for skip in ["CHAPTER", "HIGHER SECONDARY", "D.RAMAN", "SCHOOL"]) and line.strip()

def clean_math_text(text):
    replacements = {
        "∞": "infinity",
        "Γ": "Gamma",
        "π": "pi",
        "Δ": "Delta",
        "∫": "∫",
        "√": "sqrt",
        "×": "*",
        "^": "**"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text
