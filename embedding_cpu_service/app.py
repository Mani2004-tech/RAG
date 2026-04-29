import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from model import EmbeddingModel

app = FastAPI()
model = EmbeddingModel()

# ------------------------------
# BATCH QUEUE
# ------------------------------
request_queue = []
BATCH_SIZE = 64
TIMEOUT = 0.01


class EmbedRequest(BaseModel):
    texts: List[str]


# ------------------------------
# WORKER
# ------------------------------
async def batch_worker():
    while True:
        await asyncio.sleep(TIMEOUT)

        if not request_queue:
            continue

        batch = request_queue[:BATCH_SIZE]
        del request_queue[:BATCH_SIZE]

        texts = []
        futures = []

        for item in batch:
            texts.extend(item["texts"])
            futures.append(item["future"])

        embeddings = model.embed(texts)

        idx = 0
        for i, item in enumerate(batch):
            count = len(item["texts"])
            result = embeddings[idx: idx + count]
            idx += count

            futures[i].set_result(result)


@app.on_event("startup")
async def startup():
    asyncio.create_task(batch_worker())


# ------------------------------
# API
# ------------------------------
@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/embed")
async def embed(req: EmbedRequest):

    loop = asyncio.get_event_loop()
    future = loop.create_future()

    request_queue.append({
        "texts": req.texts,
        "future": future
    })

    result = await future

    return {"embeddings": result}