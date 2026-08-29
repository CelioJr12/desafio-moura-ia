import json
import numpy as np
from google.genai import types

from app.config import client, EMBED_MODEL
from app.database import get_connection


def gerar_embedding_pergunta(pergunta):
    resultado = client.models.embed_content(
        model=EMBED_MODEL,
        contents=pergunta,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    return np.array(resultado.embeddings[0].values)


def similaridade_cosseno(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def buscar_trechos(pergunta, top_k=3):
    embedding_pergunta = gerar_embedding_pergunta(pergunta)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT chunks.content, chunks.section_title, chunks.embedding, documents.filename, documents.title
        FROM chunks JOIN documents ON chunks.document_id = documents.id
    """)
    linhas = cur.fetchall()
    conn.close()

    resultados = []
    for linha in linhas:
        embedding_chunk = np.array(json.loads(linha["embedding"]))
        score = similaridade_cosseno(embedding_pergunta, embedding_chunk)
        resultados.append({
            "content": linha["content"],
            "section_title": linha["section_title"],
            "filename": linha["filename"],
            "title": linha["title"],
            "score": score,
        })

    resultados.sort(key=lambda r: r["score"], reverse=True)
    return resultados[:top_k]