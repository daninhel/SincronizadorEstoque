# 🚀 Plano de Ação: Sincronizador de Estoque Omnichannel (PoC)

Este documento detalha como construir uma Prova de Conceito (PoC) de um sincronizador de estoque entre múltiplas plataformas, simulando um cenário real de e-commerce sem depender de contas pagas.

## 🎯 Objetivo
Demonstrar a capacidade de integrar APIs distintas, tratar concorrência de dados e garantir a consistência de estoque entre um "ERP Central" e "Canais de Venda".

---

## 🛠️ Estratégia de Desenvolvimento (Sem Clientes Reais)

Para replicar o cenário sem custos, utilizaremos **Mock APIs**. Isso demonstra que você sabe ler documentações técnicas e estruturar sistemas baseados em contratos de API.

### 1. Simulação das Pontas
- **Ponta A (ERP Mock):** Simularemos um ERP (ex: Bling/Tiny) usando um servidor local em **Python (FastAPI)** ou **JSON Server**.
- **Ponta B (Loja Mock):** Simularemos uma plataforma de e-commerce (ex: Shopify/Mercado Livre) também via Mock.
- **O Sincronizador:** Um script Python que roda periodicamente, compara as duas pontas e executa as atualizações.

---

## 📋 Fases do Projeto

### Fase 1: Arquitetura e Ambiente
- [x] Configurar um ambiente virtual Python (`venv`).
- [x] Criar o `server.py` que expõe endpoints como:
    - `GET /erp/produtos`: Retorna lista de produtos e quantidades.
    - `POST /erp/venda`: Simula uma venda vinda do PDV físico.
    - `GET /loja/produtos`: Retorna o estoque na "nuvem".
    - `PATCH /loja/atualizar-estoque`: Atualiza a quantidade na loja.

### Fase 2: O Motor de Sincronização
- [ ] Desenvolver o script de comparação:
    - Lê o estoque do ERP.
    - Lê o estoque da Loja.
    - Se `estoque_erp != estoque_loja`, prioriza o ERP e atualiza a Loja.
- [ ] Implementar **Logs Detalhados**: Essencial para B2B. Mostrar exatamente o que foi alterado e por quê.

### Fase 3: Tratamento de Conflitos
- [ ] Simular uma "Venda Simultânea": O que acontece se uma venda ocorre no ERP e na Loja ao mesmo tempo?
- [ ] Implementar lógica de reserva de estoque ou alertas via Webhook (simulado).

### Fase 4: Interface de Monitoramento (Opcional - Diferencial)
- [ ] Criar uma página simples em HTML (usando seu portfólio como base) que mostre o "Status da Sincronização" em tempo real consumindo os logs.

---

## 📦 Estrutura de Arquivos Sugerida
```text
projeto-sincronizador/
├── src/
│   ├── sync.py            # Lógica principal
│   ├── api_client.py      # Abstração das chamadas de API
│   └── utils/logger.py    # Sistema de logs
├── mocks/
│   ├── server.py          # Servidor FastAPI simulando as APIs
│   └── data.json          # Banco de dados fake
├── requirements.txt
└── README.md              # Explicação técnica para o cliente
```

---

## 📈 Como apresentar isso para um Cliente Freelance?

Ao invés de dizer "eu fiz um script", você dirá:
> "Desenvolvi um motor de sincronização omnichannel que garante que o estoque físico e o estoque virtual estejam sempre alinhados. Usei arquitetura baseada em APIs para garantir que a solução seja escalável para plataformas como Shopify, Mercado Livre e ERPs nacionais."

### Itens para mostrar:
1. **Vídeo do Terminal/Logs**: Mostrando o script detectando uma diferença e corrigindo-a automaticamente.
2. **Código Limpo**: Mostrar como você separa a lógica de negócio (sincronização) da lógica de infraestrutura (chamadas de API).
3. **Tratamento de Erros**: O que o script faz se a API da loja cair? (Implementar Retry Logic).

---
