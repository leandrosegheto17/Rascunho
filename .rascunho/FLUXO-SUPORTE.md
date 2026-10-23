# Fluxo de suporte ao cliente

Um usuário traz um problema, uma dúvida ou uma reclamação. A regra central: **resolver o problema da pessoa e transformar cada atendimento em melhoria do produto**. Cada fase termina com uma decisão (resolver, escalar ou encerrar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Recebimento** | O que a pessoa precisa? | Registrar em um lugar único: quem é, o que tentava fazer, o que esperava, o que aconteceu, ambiente e evidências. Confirmar o recebimento e dar um prazo. | Registrado e confirmado |
| 2 | **Classificação** | Que tipo de caso é, e qual a urgência? | Dúvida de uso, bug, pedido de feature, cobrança, conta, segurança. Prioridade por impacto: perda de dado, bloqueio total e vazamento sobem na fila. | Tipo e prioridade definidos |
| 3 | **Verificação rápida** | Já existe resposta? | Procurar em base de conhecimento, casos anteriores e problemas conhecidos. Verificar se é falha em andamento ([FLUXO-INCIDENTE.md](FLUXO-INCIDENTE.md)). | Resposta conhecida? |
| 4 | **Diagnóstico** | O que está acontecendo com essa pessoa? | Reproduzir, conferir a conta e os dados (com acesso mínimo e registrado), pedir só o que falta e uma vez. Evitar interrogatório. | Causa identificada |
| 5 | **Resolução** | Como resolvo? | Instrução clara e passo a passo, correção na conta, contorno temporário. Se for bug, abrir o [FLUXO-BUG.md](FLUXO-BUG.md) e dar à pessoa um contorno e uma expectativa honesta. | Resolvido ou encaminhado |
| 6 | **Comunicação** | A pessoa entendeu e foi tratada bem? | Linguagem simples, sem culpar, admitir erro quando for nosso, dizer o que será feito e quando. Nunca prometer o que não se controla. | Resposta enviada |
| 7 | **Confirmação** | Resolveu mesmo? | Perguntar se resolveu e só encerrar com confirmação ou depois de um prazo sem resposta | Caso fechado |
| 8 | **Escalonamento** | Quando passo adiante? | Fora da minha alçada ou capacidade: bug, falha de segurança, questão legal ou financeira. Passar o caso completo para a pessoa não precisar repetir. | Encaminhado com contexto |
| 9 | **Aprendizado** | O que este caso ensina? | Tags por causa raiz, contagem de casos repetidos, entrada na base de conhecimento, sugestões vão ao [FLUXO-SUGESTAO-TERCEIROS.md](FLUXO-SUGESTAO-TERCEIROS.md), pedidos recorrentes viram prioridade | Melhoria registrada |

## Princípios

- **Um registro único por caso.** Conversa espalhada gera retrabalho.
- **Primeira resposta rápida, mesmo sem solução.** Saber que foi visto reduz a irritação.
- **Pedir informação uma vez só.** Perguntar de novo o que já foi dito irrita.
- **Acesso mínimo aos dados do cliente**, registrado, e somente para resolver o caso. Dado pessoal exige cuidado (LGPD).
- **Cobrança, segurança e legal vão para quem decide.** Não improvisar.
- **Muitos casos iguais indicam problema no produto**, não no usuário.
- **Documentar a resposta boa.** Resolver uma vez e escrever evita resolver dez.

Outros fluxos: [FLUXO-BUG.md](FLUXO-BUG.md), [FLUXO-INCIDENTE.md](FLUXO-INCIDENTE.md), [FLUXO-SUGESTAO-TERCEIROS.md](FLUXO-SUGESTAO-TERCEIROS.md).
