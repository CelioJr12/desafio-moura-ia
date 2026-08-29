from app.config import client, GEN_MODEL

PROMPT_BASE = """Voce e um assistente corporativo do Grupo Moura. Responda a pergunta do
colaborador usando ESTRITAMENTE as informacoes do CONTEXTO abaixo, extraido dos
documentos internos da empresa. Nao utilize conhecimento externo.

Regras:
- Se a resposta estiver no contexto, responda de forma clara e objetiva.
- Sempre indique ao final de qual documento veio a informacao.
- Se o contexto nao tiver a resposta, diga claramente que nao encontrou essa
  informacao nos documentos disponiveis. Nao invente.

CONTEXTO:
{contexto}

PERGUNTA: {pergunta}

RESPOSTA:"""


def montar_contexto(trechos):
    partes = []
    for t in trechos:
        partes.append(f"[Fonte: {t['filename']} - {t['section_title']}]\n{t['content']}")
    return "\n\n".join(partes)


def gerar_resposta(pergunta, trechos):
    contexto = montar_contexto(trechos)
    prompt = PROMPT_BASE.format(contexto=contexto, pergunta=pergunta)

    resposta = client.chat.completions.create(
        model=GEN_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return resposta.choices[0].message.content