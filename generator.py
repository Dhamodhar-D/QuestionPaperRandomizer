from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit

def generate_pdf(question_list, file_path):
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica", 11)

    for idx, q in enumerate(question_list, start=1):
        question_text = f"{idx}. {q['question']}"
        q_lines = simpleSplit(question_text, "Helvetica", 11, width - 100)
        for line in q_lines:
            c.drawString(50, y, line)
            y -= 18

        # Add each option on its own line
        for opt in q['options']:
            opt_lines = simpleSplit(opt, "Helvetica", 11, width - 100)
            for line in opt_lines:
                c.drawString(70, y, line)
                y -= 18

        y -= 12  # spacing between questions

        if y < 100:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = height - 50

    c.save()
