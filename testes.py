import json
import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

#.env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Lista com vários tipos de chamados
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

url_servidor = "http://127.0.0.1:8000/receber-chamado"

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
    # 1.Análise do chamado 
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

    # 2.Payload 
    payload_completo = {
        "titulo": chamado["titulo"],
        "descricao": chamado["descricao"],
        "categoria": dados_ia.get("categoria"),
        "prioridade": dados_ia.get("prioridade"),
        "departamento": dados_ia.get("departamento"),
    }

    # 3. Envia para o servidor simulado do GLPI
    resposta_servidor = requests.post(url_servidor, json=payload_completo)
    print(f"🖥️ Servidor GLPI Respondeu: {resposta_servidor.json()}")

  except Exception as e:
    print(f"❌ Erro ao processar o teste {i}: {e}")

  print("=" * 50)