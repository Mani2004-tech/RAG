import asyncio

import aiohttp

from config.config import EMBEDDING_ENDPOINT


class EmbeddingClient:

    def __init__(self, batch_size=32, max_concurrency=5):
        self.endpoint = EMBEDDING_ENDPOINT
        self.batch_size = batch_size
        self.max_concurrency = max_concurrency
        print("🧠 Embedding client initialized")

    async def _embed_batch(self, session, semaphore, batch):
        async with semaphore:
            payload = {"texts": batch}
            async with session.post(
                self.endpoint,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as resp:
                data = await resp.json()
                return data["embeddings"]

    async def _embed_async(self, texts):
        batches = [
            texts[i : i + self.batch_size]
            for i in range(0, len(texts), self.batch_size)
        ]

        print(f"📦 Total embedding batches: {len(batches)}")

        semaphore = asyncio.Semaphore(self.max_concurrency)

        async with aiohttp.ClientSession() as session:
            tasks = [
                self._embed_batch(session, semaphore, batch)
                for batch in batches
            ]
            results = await asyncio.gather(*tasks)

        embeddings = []
        for r in results:
            embeddings.extend(r)

        print(f"✅ Generated {len(embeddings)} embeddings")
        return embeddings

    def embed(self, texts):
        if not texts:
            return []

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            return loop.run_until_complete(self._embed_async(texts))
        finally:
            loop.close()
