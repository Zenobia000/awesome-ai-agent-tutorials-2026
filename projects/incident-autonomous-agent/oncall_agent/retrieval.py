"""Dense + BM25 + RRF；模型或 Neo4j 無法使用時保留唯讀備援。"""

import json
import os
import re
from pathlib import Path
from uuid import uuid4

import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

ROOT = Path(__file__).resolve().parents[1]


def tokens(text):
    return re.findall(r"[a-z0-9_-]+|[\u4e00-\u9fff]", text.lower())


class Runbooks:
    def __init__(self, settings):
        self.settings = settings
        self.docs = [
            {"source": p.name, "text": p.read_text()}
            for p in sorted((ROOT / "data/runbooks").glob("*.md"))
        ]
        self.sparse = BM25Okapi([tokens(d["text"]) for d in self.docs])
        # Offline demonstration uses latent semantic vectors, not fake scores.
        self.vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(1, 3))
        features = self.vectorizer.fit_transform(d["text"] for d in self.docs)
        self.svd = TruncatedSVD(
            n_components=min(3, len(self.docs) - 1), random_state=42
        )
        self.dense = normalize(self.svd.fit_transform(features))

    def search(self, query, limit=3):
        scores = self.sparse.get_scores(tokens(query))
        sparse = [int(i) for i in np.argsort(-scores) if scores[i] > 0]
        warning = ""
        try:
            if self.settings.mode == "live":
                dense = self._ollama_chroma(query)
                method = "ollama-chroma+bm25+rrf"
            else:
                vector = normalize(
                    self.svd.transform(self.vectorizer.transform([query]))
                )[0]
                similarities = self.dense @ vector
                dense = [
                    int(i)
                    for i in np.argsort(-similarities)
                    if similarities[i] > 0
                ]
                method = "offline-lsa+bm25+rrf"
        except Exception as exc:
            # Retrieval cannot grant write authority, even when degraded.
            dense = []
            method = "bm25-fallback"
            warning = f"Dense 檢索失敗：{type(exc).__name__}"
        fused = {}
        for ranking in (dense, sparse):
            for rank, index in enumerate(ranking, start=1):
                fused[index] = fused.get(index, 0) + 1 / (60 + rank)
        hits = [
            {**self.docs[i], "score": fused[i]}
            for i in sorted(fused, key=fused.get, reverse=True)[:limit]
        ]
        return {"method": method, "warning": warning, "hits": hits}

    def _ollama_chroma(self, query):
        import chromadb
        from openai import OpenAI

        client = OpenAI(
            base_url=os.getenv("LOCAL_BASE_URL", "http://localhost:11434/v1"),
            api_key="ollama",
            timeout=30,
            max_retries=0,
        )
        response = client.embeddings.create(
            model=os.getenv("EMBED_MODEL", "bge-m3"),
            input=[d["text"] for d in self.docs] + [query],
        )
        vectors = [
            v.embedding for v in sorted(response.data, key=lambda v: v.index)
        ]
        # A request-scoped collection avoids stale embeddings across models.
        chroma = chromadb.EphemeralClient()
        name = f"runbooks-{uuid4().hex}"
        collection = chroma.create_collection(name)
        try:
            collection.add(
                ids=[str(i) for i in range(len(self.docs))],
                embeddings=vectors[:-1],
            )
            result = collection.query(
                query_embeddings=[vectors[-1]], n_results=len(self.docs)
            )
            return [int(i) for i in result["ids"][0]]
        finally:
            chroma.delete_collection(name)


class Topology:
    def __init__(self, settings):
        self.settings = settings

    def lookup(self, service):
        if self.settings.neo4j_uri:
            try:
                from neo4j import GraphDatabase

                with GraphDatabase.driver(
                    self.settings.neo4j_uri,
                    auth=(
                        self.settings.neo4j_user,
                        self.settings.neo4j_password,
                    ),
                    connection_timeout=3,
                    max_transaction_retry_time=0,
                ) as driver:
                    records, _, _ = driver.execute_query(
                        "MATCH (a:Service)-[:DEPENDS_ON]->(b:Service) "
                        "WHERE a.name=$service OR b.name=$service "
                        "RETURN a.name AS source,b.name AS target",
                        service=service,
                        routing_="r",
                    )
                    if records:
                        return {
                            "source": "neo4j",
                            "edges": [dict(r) for r in records],
                        }
            except Exception:
                pass
        edges = json.loads((ROOT / "data/topology.json").read_text())
        return {
            "source": "local-topology-fallback",
            "edges": [
                {"source": a, "target": b}
                for a, b in edges
                if service in (a, b)
            ],
        }
