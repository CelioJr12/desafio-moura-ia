from pydantic import BaseModel
from typing import List, Optional


class PerguntaRequest(BaseModel):
    pergunta: str


class Fonte(BaseModel):
    documento: str
    secao: Optional[str] = None
    similaridade: float


class RespostaResponse(BaseModel):
    resposta: str
    fontes: List[Fonte]