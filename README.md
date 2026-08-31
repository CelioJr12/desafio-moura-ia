# Assistente Inteligente de Consulta a Documentos Corporativos

MVP de um sistema de Perguntas e Respostas sobre documentos corporativos, usando o padrão **RAG (Retrieval-Augmented Generation)**. Desenvolvido como desafio técnico do processo seletivo de Estágio em Engenharia de Software e IA do Grupo Moura.

## O problema

Colaboradores do Grupo Moura precisam buscar manualmente em vários documentos internos (políticas, manuais, FAQs) para tirar dúvidas simples, como "quantos dias de férias eu acumulo?". Este projeto prototipa um assistente que responde a essas perguntas em linguagem natural, buscando a informação diretamente nos documentos da empresa e sempre citando a fonte.

## Arquitetura

Indexação (rodada uma vez, via python -m app.ingest):
data/*.md → divididos em "chunks" por seção → embedding local de cada chunk
→ salvo no SQLite

Consulta (a cada pergunta, via API):
pergunta → embedding da pergunta → similaridade de cosseno vs chunks no SQLite
→ top-3 trechos mais relevantes → prompt com esses trechos → Groq gera a resposta
→ API devolve {resposta, fontes} → interação salva no SQLite


## Stack e decisões técnicas

| Camada | Escolha | Por quê |
|---|---|---|
| API | FastAPI | Sugestão do desafio, tipagem forte com Pydantic, documentação automática (`/docs`) |
| Geração de resposta | Groq (`openai/gpt-oss-20b`) | API gratuita, sem exigência de conta de faturamento |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`), rodando localmente | Elimina dependência de disponibilidade de terceiros nessa etapa crítica; sem custo, sem limite de requisições |
| Busca por similaridade | Cálculo manual com `numpy` (cosseno) | Volume pequeno de documentos (MVP); um banco vetorial dedicado (FAISS, Chroma) seria o próximo passo natural em escala maior |
| Persistência | SQLite | Sem necessidade de servidor, ótimo para um MVP |

**Nota sobre a escolha de provedor de IA:** a primeira versão deste projeto usava a API do Gemini (Google), mas o acesso via API ficou bloqueado para a conta usada no desenvolvimento (exigência de conta de faturamento com liberação de até 24h, mesmo na camada gratuita). Diante do prazo do desafio, migrei a geração de texto para a Groq e os embeddings para um modelo local — decisão que, além de resolver o bloqueio, tornou o sistema mais resiliente (menos pontos de falha externos).

## Estrutura do projeto

desafio-moura-ia/
├── data/ # documentos corporativos ficticios
├── app/
│ ├── config.py # configuracao, cliente Groq, modelo de embedding
│ ├── database.py # schema e conexao SQLite
│ ├── ingest.py # leitura, chunking e indexacao dos documentos
│ ├── retrieval.py # busca por similaridade
│ ├── generation.py # montagem do prompt e geracao da resposta
│ ├── models.py # schemas Pydantic da API
│ └── main.py # aplicacao FastAPI
├── tests/
│ └── test_api.py
├── requirements.txt
└── README.md


## Como rodar

### 1. Pré-requisitos
- Python 3.12+
- Uma chave gratuita da Groq: https://console.groq.com/keys

### 2. Instalação
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows (PowerShell)
pip install -r requirements.txt
```

### 3. Configuração
Crie um arquivo `.env` na raiz com:

GROQ_API_KEY=sua_chave_aqui


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

Desenvolvido por Célio Pereira Dias Junior para o desafio técnico do Grupo Moura — Agosto de 2026.
