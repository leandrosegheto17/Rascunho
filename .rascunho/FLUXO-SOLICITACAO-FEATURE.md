# Fluxo de solicitação de feature sob demanda

Uma pessoa com autoridade (cliente, dono do produto, gestor) pede uma funcionalidade e espera resposta e entrega. Diferente da sugestão de terceiros, há um solicitante que **decide e cobra**. A regra central: **alinhar o entendimento e as expectativas antes de construir**. A maior causa de retrabalho é entregar bem algo diferente do que se queria. Cada fase termina com uma decisão (seguir, renegociar ou recusar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Recebimento** | O que foi pedido, por quem e para quando? | Registrar o pedido com as palavras do solicitante, a urgência declarada e o motivo | Registrado |
| 2 | **Esclarecimento** | O que o solicitante quer de verdade? | Perguntar o objetivo, quem vai usar, o que acontece hoje, o que é indispensável e o que é desejável. Reescrever o pedido em critérios de aceite testáveis. | Entendimento confirmado por escrito? |
| 3 | **Triagem** | É uma feature nova, ajuste, bug ou outro fluxo? | Classificar e checar se já existe, se conflita com algo, se muda regra de negócio, dados, segurança ou custo | Fluxo correto escolhido |
| 4 | **Estimativa e opções** | Quanto custa e que alternativas existem? | Estimar esforço e risco. Oferecer opções: versão mínima agora e completa depois, ou solução parcial por menos. | Solicitante vê as opções |
| 5 | **Negociação e prioridade** | O que entra, o que sai e quando? | Comparar com o trabalho em andamento, deixar claro o que será adiado, acordar escopo, prazo e critério de aceite | Acordo registrado |
| 6 | **Execução** | A feature é construída com qualidade? | Acionar o fluxo adequado: [FLUXO-FEATURE.md](FLUXO-FEATURE.md) para projeto com IA, [FLUXO-FEATURE-LEGADO.md](FLUXO-FEATURE-LEGADO.md) para legado | Critérios de aceite atendidos |
| 7 | **Acompanhamento** | O solicitante sabe como está? | Atualizar nos marcos combinados e avisar logo sobre qualquer desvio de prazo ou de escopo | Sem surpresas |
| 8 | **Aceite** | O solicitante confirma que é isso? | Demonstração contra os critérios de aceite combinados. Ajustes pequenos entram, mudanças de escopo viram novo pedido. | Aceite registrado |
| 9 | **Entrega e fechamento** | Foi liberado e documentado? | Deploy, atualização de documentação e do contexto do projeto, comunicado, registro do que foi entregue | Ciclo fechado |

## Princípios

- **Pedido não é especificação.** Reescrever em critérios de aceite antes de estimar.
- **Estimar sempre antes de prometer.** Prazo dito no primeiro contato vira compromisso.
- **Mudança de escopo é novo pedido.** Evita crescimento silencioso do trabalho.
- **Não pular a triagem.** Muitos pedidos "de feature" são bugs, ou já existem.
- **Dizer o que sai quando algo entra.** Capacidade é finita.
- **Aceite explícito.** Sem ele, "pronto" depende da memória de cada um.

Outros fluxos: [FLUXO-SUGESTAO-TERCEIROS.md](FLUXO-SUGESTAO-TERCEIROS.md), [FLUXO-FEATURE.md](FLUXO-FEATURE.md), [FLUXO-FEATURE-LEGADO.md](FLUXO-FEATURE-LEGADO.md).
