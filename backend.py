from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
RESULT_PATH = "result.jpg"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/fusion")
async def fusionar_fotos(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    path1 = os.path.join(UPLOAD_DIR, "1.jpg")
    path2 = os.path.join(UPLOAD_DIR, "2.jpg")
    with open(path1, "wb") as f1:
        shutil.copyfileobj(file1.file, f1)
    with open(path2, "wb") as f2:
        shutil.copyfileobj(file2.file, f2)

    os.system(f"facefusion --source {path1} --target {path2} --output {RESULT_PATH} --headless")

    return FileResponse(RESULT_PATH, media_type="image/jpeg")
