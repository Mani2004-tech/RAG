
# from langsmith import traceable
# from agentic_rag.ingestion_layer.ingestion_executor import execute_ingestion
# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import shutil
# import os
# import asyncio
# from concurrent.futures import ThreadPoolExecutor

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

# # Initialize pipeline
# pipeline = AgenticRAGPipeline()

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # Worker pool for parallel ingestion
# executor = ThreadPoolExecutor(max_workers=4)


# def run_pipeline(path: str):
#     """
#     Runs the ingestion pipeline synchronously
#     (executed inside worker threads)
#     """
#     return pipeline.run(path)


# # -----------------------------------------
# # Single File Ingestion
# # -----------------------------------------
# @app.post("/ingest")
# async def ingest(file: UploadFile = File(...)):

#     path = f"{UPLOAD_DIR}/{file.filename}"

#     with open(path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     print("📂 File received:", file.filename)

#     loop = asyncio.get_event_loop()

#     result = await loop.run_in_executor(
#         executor,
#         run_pipeline,
#         path
#     )

#     return {
#         "file": file.filename,
#         "result": result
#     }


# # -----------------------------------------
# # Multiple File Ingestion (Parallel)
# # -----------------------------------------
# @traceable(name="api_ingestion_endpoint", run_type="chain")
# @app.post("/ingest-multiple")
# async def ingest_multiple(files: list[UploadFile] = File(...)):

#     paths = []

#     for file in files:

#         path = f"{UPLOAD_DIR}/{file.filename}"

#         with open(path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         print("📂 Processing:", file.filename)

#         paths.append(path)

#     loop = asyncio.get_event_loop()

#     tasks = [
#         loop.run_in_executor(
#             executor,
#             run_pipeline,
#             path
#         )
#         for path in paths
#     ]

#     results = await asyncio.gather(*tasks)

#     return {
#         "processed_files": len(paths),
#         "results": results
#     }
from langsmith_setup import init_langsmith
from langsmith import traceable
from ingestion_executor import execute_ingestion

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import shutil
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

from pipeline import AgenticRAGPipeline

init_langsmith()
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

# Worker pool
executor = ThreadPoolExecutor(max_workers=4)


# 🔥 FIX: wrap execution with traceable executor
def run_pipeline(path: str):
    return execute_ingestion(pipeline, path)


# -----------------------------------------
# Single File Ingestion
# -----------------------------------------
@traceable(name="api_ingestion_single", run_type="chain")
@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):

    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("📂 File received:", file.filename)

    loop = asyncio.get_event_loop()

    result = await loop.run_in_executor(
        executor,
        run_pipeline,   # ✅ now traced
        path
    )

    return {
        "file": file.filename,
        "result": result
    }


# -----------------------------------------
# Multiple File Ingestion (Parallel)
# -----------------------------------------
@traceable(name="api_ingestion_multiple", run_type="chain")
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
            run_pipeline,   # ✅ traced wrapper
            path
        )
        for path in paths
    ]

    results = await asyncio.gather(*tasks)

    return {
        "processed_files": len(paths),
        "results": results
    }