import asyncio
import os
import shutil
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from pipeline import AgenticRAGPipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = AgenticRAGPipeline()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

executor = ThreadPoolExecutor(max_workers=4)


def run_pipeline(path: str):
    """Run the ingestion pipeline synchronously inside worker threads."""
    return pipeline.run(path)


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("📂 File received:", file.filename)

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, run_pipeline, path)

    return {"file": file.filename, "result": result}


@app.post("/ingest-multiple")
async def ingest_multiple(files: list[UploadFile] = File(...)):
    paths = []

    for file in files:
        path = f"{UPLOAD_DIR}/{file.filename}"

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("📂 Processing:", file.filename)
        paths.append(path)

    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(executor, run_pipeline, path) for path in paths]
    results = await asyncio.gather(*tasks)

    return {"processed_files": len(paths), "results": results}
