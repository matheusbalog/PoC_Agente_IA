import json
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
import requests

# .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# 1. Definição dos chamados (movida para o topo para evitar erro de referência)
chamados_teste = [
    {
        "titulo": "Impressora do 2º andar travada",
        "descricao": "A impressora fica piscando luz vermelha e não puxa papel.",
    },
    {
        "titulo": "Esqueci minha senha do ERP",
        "descricao": "Não consigo entrar no sistema de gestão, dá senha inválida.",
    },
    {
        "titulo": "Lentidão na rede Wi-Fi",
        "descricao": (
            "O sinal cai toda hora na sala de reuniões e não conecta."
        ),
    },
    {
        "titulo": "Erro 500 no painel",
        "descricao": "Está dando erro 500 ao tentar acessar a tela de relatórios.",
    },
]

url_servidor = "http://127.0.0.1:8001/api/jira/issues"

print("=== TESTES AUTOMÁTICOS ===\n")

for i, chamado in enumerate(chamados_teste, 1):
    print(f"--- Teste {i} ---")
    print(f"Título: {chamado['titulo']}")

    # Prompt
    prompt = f"""Analise o chamado de TI abaixo e categorize-o.
Retorne um JSON com exatamente estas três chaves:
- "categoria": Escolha entre "Bug", "Dúvida", "Melhoria", "Solicitação"
- "prioridade": Escolha entre "Baixa", "Média", "Alta", "Urgente"
- "departamento": Escolha entre "Suporte Técnico", "Desenvolvimento", "Infraestrutura"

Título: {chamado['titulo']}
Descrição: {chamado['descricao']}
"""

    try:
        # 1. Análise do chamado via IA
        resposta_ia = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        dados_ia = json.loads(resposta_ia.text)
        print(
            "🤖 Gemini Classificou -> Categoria:"
            f" {dados_ia.get('categoria')} | Prioridade:"
            f" {dados_ia.get('prioridade')} | Depto:"
            f" {dados_ia.get('departamento')}"
        )

    except Exception as e:
        # Fallback de emergência caso estoure a cota (429)
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print(
                "⚠️ Cota da API esgotada temporariamente. Usando resposta simulada"
                " (fallback) para a PoC."
            )
            dados_ia = {
                "categoria": "Solicitação",
                "prioridade": "Média",
                "departamento": "Suporte Técnico",
            }
        else:
            print(f"❌ Erro ao processar o teste {i}: {e}")
            continue

    # 2. Payload para o servidor
    payload_completo = {
        "titulo": chamado["titulo"],
        "descricao": chamado["descricao"],
        "categoria": dados_ia.get("categoria"),
        "prioridade": dados_ia.get("prioridade"),
        "departamento": dados_ia.get("departamento"),
    }

    # 3. Envia para o servidor simulado do GLPI
    try:
        resposta_servidor = requests.post(url_servidor, json=payload_completo)
        print(f"🖥️ Servidor GLPI Respondeu: {resposta_servidor.json()}")
    except Exception as server_error:
        print(f"⚠️ Aviso: Servidor local não respondeu ({server_error})")

    print("=" * 50)
    print("Aguardando 4 segundos para a próxima requisição...")
    time.sleep(4)