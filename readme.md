# PoC_Agente_IA - Mock Server

Servidor Mock desenvolvido em FastAPI para validação da lógica de orquestração de agentes de IA (GLPI -> Bitbucket > Jira).

## Objetivo
Testes rápidos e isolados para validação do fluxo de triagem, investigação e aprovação humana (HITL).

## Funcionalidades
- **Simulação de Polling:** Simula a busca periódica de chamados no GLPI.
- **Idempotência na Entrada:** Implementação de proteção contra reprocessamento de chamados já registrados na base de estados (evitando duplicidade de cards no Jira e desperdício de tokens).
- **Máquina de Estados:** Gerenciamento dos estados (`RECEIVED`, `CLASSIFYING`, `AWAITING_APPROVAL`, `DONE`).
- **HITL (Human-in-the-Loop):** Endpoint dedicado para simular a aprovação/reprovação de um card antes da criação efetiva no Jira.

### Instalação
```bash
# Clone o repositório
git clone [https://github.com/matheusbalog/PoC_Agente_IA.git](https://github.com/matheusbalog/PoC_Agente_IA.git)
cd PoC_Agente_IA

# Criar o .env e a chave de API do gemini

# Instale as dependências
pip install fastapi uvicorn google-generativeai pydantic python-dotenv

# Rode o servidor
uvicorn main:app --reload
