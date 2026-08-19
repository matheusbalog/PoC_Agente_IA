from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DadosChamado(BaseModel.model_config == {**BaseModel.model_config, "extra": "allow"}): 
    titulo: str
    descricao: str
    classificacao: str = "Desconhecida"
    prioridade: str = "Média"
    departamento: str = "Geral"

@app.post("/receber-chamado")
def receber_chamado(dados: dict):
    print(f"\n[GLPI MOCK] Novo chamado recebido!")
    print(f"Título: {dados.get('titulo')}")
    print(f"IA - Categoria: {dados.get('classificacao')}")
    print(f"IA - Prioridade: {dados.get('prioridade')}")
    print(f"IA - Departamento: {dados.get('departamento')}")
    
    return {
        "status": "sucesso",
        "id_chamado": 501,
        "mensagem": "Chamado triado e categorizado com sucesso pela IA!"
    }