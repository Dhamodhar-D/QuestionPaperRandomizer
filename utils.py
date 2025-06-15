import zipfile
import os

def zip_output_pdfs(output_dir, zip_filename="question_papers.zip"):
    zip_path = os.path.join(output_dir, zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_name in os.listdir(output_dir):
            if file_name.endswith(".pdf"):
                full_path = os.path.join(output_dir, file_name)
                zipf.write(full_path, arcname=file_name)
    return zip_path
