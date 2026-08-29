
### 4. Indexar os documentos
```bash
python -m app.ingest
```

### 5. Subir a API
```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa em `http://127.0.0.1:8000/docs`.

## Exemplo de uso

**Requisição:**
```json
POST /perguntar
{
  "pergunta": "Quantos dias de ferias eu acumulo por mes?"
}
```

**Resposta:**
```json
{
  "resposta": "Você acumula 2,5 dias de férias por mês trabalhado. (Fonte: politica_ferias.md - Acúmulo de dias)",
  "fontes": [
    {
      "documento": "politica_ferias.md",
      "secao": "Acúmulo de dias",
      "similaridade": 0.6296
    }
  ]
}
```

Se a pergunta não tiver relação com nenhum documento, o assistente responde que não encontrou a informação, em vez de inventar uma resposta.

## Limitações conhecidas e próximos passos

- A busca por similaridade é feita em memória com `numpy`; não escala bem além de algumas centenas de documentos. Em produção, migraria para um banco vetorial dedicado (FAISS, Chroma ou pgvector).
- Não há autenticação na API.
- Não há interface web; a interação é feita via `/docs` ou requisições HTTP diretas.
- O chunking é feito por seção (`##`) com um limite simples de caracteres; poderia ser refinado com sobreposição (overlap) entre chunks.

## Testes

```bash
pytest
```

---

Desenvolvido por [Célio Pereira Dias Junior] para o desafio técnico do Grupo Moura — Agosto de 2026.