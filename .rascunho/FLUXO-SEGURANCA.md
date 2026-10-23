# Fluxo de auditoria de segurança

Revisar a segurança de um projeto antes de expô-lo, vendê-lo ou depois de uma suspeita. A regra central: **pensar como atacante, priorizar por risco real e provar a correção**. Cada fase termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Escopo** | O que será auditado e com que autorização? | Definir sistemas, ambientes e limites. Ter permissão explícita para testar. Nunca testar o que não é seu sem autorização por escrito. | Escopo e autorização claros |
| 2 | **Ativos e superfície** | O que vale proteger e por onde se entra? | Listar dados sensíveis, contas, segredos, pontos de entrada (rotas, formulários, uploads, APIs, integrações, painéis) e quem tem acesso | Superfície mapeada |
| 3 | **Modelo de ameaças** | Quem atacaria, como e o que ganharia? | Para cada ativo, listar ameaças prováveis (injeção, acesso indevido, vazamento, negação de serviço, roubo de conta), usando uma lista de referência como OWASP Top 10 | Ameaças priorizadas |
| 4 | **Varredura automática** | O que as ferramentas encontram? | Dependências com falhas conhecidas, segredos no código e no histórico do git, análise estática, configuração de infraestrutura | Achados brutos coletados |
| 5 | **Revisão manual** | O que as ferramentas não veem? | Autenticação, autorização (acesso a dados de outros usuários), validação de entrada, sessões, criptografia, regras de negócio abusáveis, logs com dado sensível | Falhas lógicas identificadas |
| 6 | **Teste ativo** | A falha é explorável de verdade? | Testar a aplicação em execução em ambiente seguro (local ou staging), com sondas e ferramentas de teste dinâmico. Confirmar cada achado, descartar falsos positivos. | Achados confirmados |
| 7 | **Classificação** | Quão grave é cada um? | Severidade por impacto e facilidade de exploração (crítico, alto, médio, baixo), com evidência e passos de reprodução | Lista priorizada |
| 8 | **Correção e reteste** | Foi resolvido de fato? | Corrigir do mais grave ao menos grave (pelo [FLUXO-BUG.md](FLUXO-BUG.md)), com teste que impede o retorno, e repetir o teste que achou a falha | Críticos e altos fechados |
| 9 | **Relatório e prevenção** | Como evitar que volte? | Relatório com resumo, achados, correções e riscos aceitos (com justificativa). Incluir varredura no CI, rotação de credenciais e revisão periódica. | Relatório entregue |

## Princípios

- **Autorização antes de tudo.** Teste sem permissão é ataque.
- **Risco real, não lista de verificação.** Priorizar o que é explorável e valioso.
- **Se um segredo vazou, trocar.** Apagar do código não basta: ele permanece no histórico.
- **Acesso a dado de outro usuário é a falha mais comum e mais cara.** Testar autorização em cada rota.
- **Risco aceito é decisão registrada**, com dono e prazo de revisão.
- **Suspeita de invasão em curso** muda o fluxo: ver [FLUXO-INCIDENTE.md](FLUXO-INCIDENTE.md).

Outros fluxos: [FLUXO-BUG.md](FLUXO-BUG.md), [FLUXO-INCIDENTE.md](FLUXO-INCIDENTE.md), [FLUXO-INTEGRACAO.md](FLUXO-INTEGRACAO.md).
