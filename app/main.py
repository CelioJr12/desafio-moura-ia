import json

from fastapi import FastAPI, HTTPException

from app.database import get_connection, init_db
from app.models import PerguntaRequest, RespostaResponse, Fonte
from app.retrieval import buscar_trechos
from app.generation import gerar_resposta

app = FastAPI(
    title="Assistente Inteligente de Consulta a Documentos Corporativos",
    description="MVP de um sistema RAG para consulta a documentos internos do Grupo Moura.",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/perguntar", response_model=RespostaResponse)
def perguntar(request: PerguntaRequest):
    if not request.pergunta or not request.pergunta.strip():
        raise HTTPException(status_code=400, detail="A pergunta nao pode ser vazia.")

    trechos = buscar_trechos(request.pergunta, top_k=3)
    if not trechos:
        raise HTTPException(
            status_code=500,
            detail="Base de documentos vazia. Rode 'python -m app.ingest' primeiro.",
        )

    resposta_texto = gerar_resposta(request.pergunta, trechos)

    fontes = [
        Fonte(documento=t["filename"], secao=t["section_title"], similaridade=round(t["score"], 4))
        for t in trechos
    ]

    conn = get_connection()
    conn.execute(
        "INSERT INTO interactions (question, answer, sources) VALUES (?, ?, ?)",
        (request.pergunta, resposta_texto, json.dumps([f.documento for f in fontes])),
    )
    conn.commit()
    conn.close()

    return RespostaResponse(resposta=resposta_texto, fontes=fontes)