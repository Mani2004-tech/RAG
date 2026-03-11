# # from fastapi import FastAPI, UploadFile, File
# # import shutil
# # import os

# # from preprocessing_pipeline.preprocessing_pipeline import PreprocessingPipeline
# # from indexing.multi_index_pipeline import MultiIndexPipeline

# # app = FastAPI()

# # preprocess = PreprocessingPipeline()
# # index_pipeline = MultiIndexPipeline()

# # UPLOAD_DIR = "uploads"

# # os.makedirs(UPLOAD_DIR, exist_ok=True)


# # @app.post("/ingest")

# # async def ingest(file: UploadFile = File(...)):

# #     path = f"{UPLOAD_DIR}/{file.filename}"

# #     with open(path, "wb") as buffer:

# #         shutil.copyfileobj(file.file, buffer)

# #     print("📂 File received:", file.filename)

# #     text, metadata = preprocess.run(path)

# #     chunks = metadata["sentences"]

# #     index_pipeline.run(text, chunks)

# #     return {"status": "ingested", "chunks": len(chunks)}


# # @app.post("/ingest-multiple")

# # async def ingest_multiple(files: list[UploadFile] = File(...)):

# #     results = []

# #     for file in files:

# #         path = f"{UPLOAD_DIR}/{file.filename}"

# #         with open(path, "wb") as buffer:

# #             shutil.copyfileobj(file.file, buffer)

# #         text, metadata = preprocess.run(path)

# #         chunks = metadata["sentences"]

# #         index_pipeline.run(text, chunks)

# #         results.append(file.filename)

# #     return {"ingested_files": results}

# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import shutil
# import os

# from pipeline import AgenticRAGPipeline

# app = FastAPI()

# # ---------- CORS ----------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# pipeline = AgenticRAGPipeline()

# UPLOAD_DIR = "uploads"

# os.makedirs(UPLOAD_DIR, exist_ok=True)


# @app.post("/ingest")

# async def ingest(file: UploadFile = File(...)):

#     path = f"{UPLOAD_DIR}/{file.filename}"

#     with open(path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     print("📂 File received:", file.filename)

#     result = pipeline.run(path)

#     return result


# @app.post("/ingest-multiple")

# async def ingest_multiple(files: list[UploadFile] = File(...)):

#     results = []

#     for file in files:

#         path = f"{UPLOAD_DIR}/{file.filename}"

#         with open(path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         print("📂 Processing:", file.filename)

#         result = pipeline.run(path)

#         results.append({
#             "file": file.filename,
#             "result": result
#         })

#     return {"results": results}

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

from pipeline import AgenticRAGPipeline


app = FastAPI()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline
pipeline = AgenticRAGPipeline()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Worker pool for parallel ingestion
executor = ThreadPoolExecutor(max_workers=4)


def run_pipeline(path: str):
    """
    Runs the ingestion pipeline synchronously
    (executed inside worker threads)
    """
    return pipeline.run(path)


# -----------------------------------------
# Single File Ingestion
# -----------------------------------------
@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):

    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("📂 File received:", file.filename)

    loop = asyncio.get_event_loop()

    result = await loop.run_in_executor(
        executor,
        run_pipeline,
        path
    )

    return {
        "file": file.filename,
        "result": result
    }


# -----------------------------------------
# Multiple File Ingestion (Parallel)
# -----------------------------------------
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

    tasks = [
        loop.run_in_executor(
            executor,
            run_pipeline,
            path
        )
        for path in paths
    ]

    results = await asyncio.gather(*tasks)

    return {
        "processed_files": len(paths),
        "results": results
    }