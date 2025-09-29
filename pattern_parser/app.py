# backend/main.py
from fastapi import FastAPI, File, UploadFile
import tempfile
from parser import process_pattern_file
import os

app = FastAPI()

@app.post("/process")
async def process(file: UploadFile = File(...)):
    suffix = ".pdf" if file.filename.lower().endswith(".pdf") else ".docx"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    parsed, flat_rows = process_pattern_file(tmp_path)

    # Read your result files
    files = {}
    for f in ["summary.txt","logs_correct.txt","logs_error.txt","logs_warning.txt"]:
        if os.path.exists(f):
            with open(f,"r",encoding="utf-8") as fh:
                files[f] = fh.read()

    return {"status":"ok","files":files}
