import glob
import json
import os

from app.config import embedding_model
from app.database import get_connection, init_db


def carregar_documentos(pasta="data"):
    arquivos = glob.glob(os.path.join(pasta, "*.md")) + glob.glob(os.path.join(pasta, "*.txt"))
    documentos = []
    for caminho in arquivos:
        with open(caminho, "r", encoding="utf-8") as f:
            texto = f.read()
        titulo = texto.strip().split("\n")[0].lstrip("# ").strip()
        documentos.append({"filename": os.path.basename(caminho), "title": titulo, "content": texto})
    return documentos


def dividir_em_chunks(texto, max_chars=800):
    """Divide o documento por secoes (##) e quebra secoes muito longas."""
    secoes = texto.split("\n## ")
    chunks = []
    for i, secao in enumerate(secoes):
        secao = secao if i == 0 else "## " + secao
        linhas = secao.strip().split("\n")
        titulo_secao = linhas[0].lstrip("# ").strip()
        conteudo = secao.strip()
        if not conteudo:
            continue
        if len(conteudo) <= max_chars:
            chunks.append((titulo_secao, conteudo))
        else:
            for j in range(0, len(conteudo), max_chars):
                chunks.append((titulo_secao, conteudo[j:j + max_chars]))
    return chunks


def gerar_embedding(texto):
    return embedding_model.encode(texto).tolist()


def indexar():
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM chunks")
    cur.execute("DELETE FROM documents")
    conn.commit()

    documentos = carregar_documentos()
    print(f"{len(documentos)} documentos encontrados em /data")

    for doc in documentos:
        cur.execute(
            "INSERT INTO documents (filename, title) VALUES (?, ?)",
            (doc["filename"], doc["title"]),
        )
        document_id = cur.lastrowid

        chunks = dividir_em_chunks(doc["content"])
        print(f"  {doc['filename']}: {len(chunks)} chunks")

        for titulo_secao, conteudo in chunks:
            embedding = gerar_embedding(conteudo)
            cur.execute(
                "INSERT INTO chunks (document_id, section_title, content, embedding) VALUES (?, ?, ?, ?)",
                (document_id, titulo_secao, conteudo, json.dumps(embedding)),
            )

    conn.commit()
    conn.close()
    print("Indexacao concluida.")


if __name__ == "__main__":
    indexar()