import json
import numpy as np

from app.config import embedding_model
from app.database import get_connection


def gerar_embedding_pergunta(pergunta):
    return np.array(embedding_model.encode(pergunta))


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