# Fluxo de investigação de incidentes

Algo quebrou, degradou ou se comportou de forma inesperada em produção. A regra central: **conter e restaurar primeiro, investigar depois**. A causa raiz só se estuda com o sistema estável, e o aprendizado só vale se virar prevenção. Cada fase termina com uma decisão (seguir, escalar ou encerrar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Detecção e triagem** | O que está acontecendo e qual a gravidade? | Registrar o sintoma, quando começou, quem é afetado, o alcance e o impacto no negócio. Classificar a severidade. | Incidente real? Que severidade? |
| 2 | **Contenção** | Como paro o dano agora? | Medida rápida e reversível: desligar a feature (flag), reverter a última mudança, isolar o componente, limitar o tráfego, avisar os afetados | Dano contido? |
| 3 | **Restauração** | O serviço voltou ao normal? | Reverter, reiniciar, aplicar correção emergencial mínima. Confirmar com métricas, não com impressão. | Serviço estável? |
| 4 | **Linha do tempo** | O que aconteceu e em que ordem? | Reconstruir os eventos com logs, métricas, traces, deploys, mudanças de configuração e alertas. Preservar as evidências antes que expirem. | Sequência dos fatos estabelecida |
| 5 | **Hipóteses e causa raiz** | Por que aconteceu de verdade? | Levantar hipóteses, testar contra as evidências, perguntar "por quê" até chegar à causa sistêmica e não só ao gatilho. Descartar culpa de pessoas. | Causa raiz confirmada com evidência? |
| 6 | **Correção definitiva** | Como elimino a causa? | Seguir o fluxo de correção de bug ou de feature conforme o caso: teste que reproduz, correção, verificação de regressão | Correção em produção e verificada |
| 7 | **Prevenção** | Como evito que volte, e como detecto mais cedo? | Novos testes, alertas, limites, validações, revisão do processo de deploy, checklist | Ações com responsável e prazo |
| 8 | **Post-mortem** | O que aprendemos? | Documento curto e sem culpa: resumo, impacto, linha do tempo, causa raiz, o que funcionou e o que não, ações | Post-mortem registrado |
| 9 | **Comunicação** | Quem precisa saber o que aconteceu? | Informar usuários e interessados do ocorrido e do que mudou. Se houve dado pessoal exposto, avaliar notificação legal (LGPD). | Comunicado enviado |

## Princípios

- **Restaurar antes de entender.** A causa se investiga com calma depois.
- **Mudança reversível primeiro.** Em emergência, o que se desfaz fácil vale mais do que a correção perfeita.
- **Preservar evidências cedo.** Logs rodam e somem; copiar antes de mexer.
- **Sem culpados.** O objetivo é achar a falha do sistema ou do processo, e não de uma pessoa.
- **Um incidente sem ação de prevenção vai se repetir.**
- **Suspeita de segurança muda o fluxo.** Se houver indício de invasão ou vazamento, isolar, preservar evidências forenses, trocar credenciais e avaliar a obrigação legal antes de restaurar.

Outros fluxos: [FLUXO-FEATURE-LEGADO.md](FLUXO-FEATURE-LEGADO.md), [FLUXO-PERFORMANCE.md](FLUXO-PERFORMANCE.md), [FLUXO-INTEGRACAO.md](FLUXO-INTEGRACAO.md).
