# Fluxo de correção de bug

Algo não se comporta como deveria. A regra central: **corrigir a causa, não o sintoma, e provar com um teste que falhava e agora passa**. Cada fase termina com uma decisão (seguir, escalar ou encerrar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Relato** | O que foi observado, onde e com que frequência? | Registrar passos, resultado esperado versus obtido, ambiente, versão, evidências (log, captura de tela) e impacto | Relato completo? |
| 2 | **Triagem** | É um bug de verdade, e quão grave? | Confirmar que contraria o comportamento definido (senão é pedido de feature), classificar severidade e urgência, juntar duplicados | Bug confirmado e priorizado? |
| 3 | **Reprodução** | Consigo fazer acontecer de forma consistente? | Reproduzir no ambiente local com o menor caso possível. Sem reprodução não há correção verificável. | Reproduzido? Senão, pedir mais dados |
| 4 | **Teste que falha** | Como provo que o bug existe? | Escrever o teste automatizado que reproduz o erro e falha pelo motivo certo | Teste vermelho pelo motivo correto |
| 5 | **Causa raiz** | Por que acontece? | Isolar por bissecção (git bisect, desativar partes), ler o código, formular hipóteses e testar. Perguntar "por quê" até a origem. | Causa confirmada com evidência? |
| 6 | **Correção** | Qual a menor mudança que resolve a causa? | Corrigir na origem, sem remendo no sintoma e sem aproveitar para refatorar | Teste passa |
| 7 | **Verificação** | Resolveu e não quebrou nada? | Suíte completa, verificação manual do cenário original e dos vizinhos, revisão do diff. Procurar o mesmo defeito em outros pontos. | Sem regressão? |
| 8 | **Liberação** | Como chega a quem sofre? | Deploy normal, ou hotfix se urgente, e confirmar em produção | Corrigido em produção |
| 9 | **Fechamento** | O relator sabe e o aprendizado ficou? | Avisar quem relatou, registrar causa e correção, e se a causa for recorrente, abrir ação de prevenção | Fechado |

## Princípios

- **Sem reprodução, sem correção.** Corrigir no escuro cria bugs novos.
- **O teste vem primeiro** e fica na suíte para sempre.
- **Mudança mínima.** Refatoração e correção na mesma alteração dificultam revisar e reverter.
- **Bug recorrente é sinal de problema de processo ou de projeto**, não só de código.
- **Saída de emergência:** se a causa revelar falha de arquitetura, o fluxo para e propõe refatoração. Se estiver em produção e grave, [FLUXO-INCIDENTE.md](FLUXO-INCIDENTE.md).

Outros fluxos: [FLUXO-INCIDENTE.md](FLUXO-INCIDENTE.md), [FLUXO-FEATURE.md](FLUXO-FEATURE.md).
