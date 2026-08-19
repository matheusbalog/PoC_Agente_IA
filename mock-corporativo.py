from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Mock Corporativo (Jira & Bitbucket)")

# --- MODELO DE DADOS ---
class JiraPayload(BaseModel):
    titulo: str
    descricao: str
    categoria: str
    prioridade: str
    departamento: str

# --- 1. MOCK DO JIRA (Criação de Cards) ---
@app.post("/api/jira/issues")
def criar_card_jira(payload: JiraPayload):
    print(f"\n[MOCK JIRA] Recebida solicitação para criar card:")
    print(f"  -> Título: {payload.titulo}")
    print(f"  -> Prioridade: {payload.prioridade}")

    # Simula a resposta de sucesso do Jira gerando uma chave falsa
    return {
        "status": "sucesso",
        "mensagem": "Card criado com sucesso no Jira",
        "key": "GLPI-1024",
        "self": "https://jira.suaempresa.com/browse/GLPI-1024"
    }

# --- 2. MOCK DO BITBUCKET (Busca de Código / Investigação) ---
@app.get("/api/bitbucket/search")
def buscar_codigo_bitbucket(termo: str):
    print(f"\n[MOCK BITBUCKET] O agente pediu busca por: {termo}")

    # Simula um retorno de código-fonte relevante para ajudar o agente de IA
    return {
        "arquivo": "src/services/printer_service.py",
        "linha": 42,
        "trecho_codigo": "def resetar_hardware_impressora():\n    # TODO: Tratar erro de luz vermelha piscando\n    raise TimeoutError('Hardware nao responde')",
        "contexto": "Código legado responsável pelo controle de periféricos."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)