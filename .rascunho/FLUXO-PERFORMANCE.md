# Fluxo de performance e escala

O sistema está lento ou vai receber mais carga. A regra central: **medir antes de mexer**. Otimizar sem medição costuma melhorar o que não importa e piorar o que importa. Cada fase termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Meta** | O que está lento, para quem, e qual é o alvo? | Definir métrica e número-alvo (ex.: p95 de 300 ms, 500 usuários simultâneos), o cenário e o prazo | Meta mensurável? |
| 2 | **Linha de base** | Como o sistema se comporta hoje? | Teste de carga e perfil em ambiente parecido com produção, métricas reais de produção quando houver | Número de partida registrado |
| 3 | **Diagnóstico** | Onde está o gargalo de verdade? | Profiling, traces, consultas lentas, uso de CPU, memória, rede e I/O. Achar o maior gargalo, não o mais óbvio. | Causa identificada com evidência? |
| 4 | **Opções** | Quais correções existem e a que custo? | Listar alternativas (consulta, índice, cache, concorrência, infraestrutura, arquitetura), esforço, risco e ganho esperado | Escolher a de melhor custo-benefício |
| 5 | **Rede de proteção** | Como garanto que a correção não muda o comportamento? | Testes do comportamento afetado antes de mexer | Testes verdes |
| 6 | **Otimização** | A mudança melhora o número? | Uma mudança por vez, medindo depois de cada uma | Ganho confirmado, ou reverter |
| 7 | **Verificação** | A meta foi atingida sem regressão? | Repetir o teste de carga, comparar com a linha de base, checar custo e consumo de recursos | Meta atingida? Senão, volta ao diagnóstico |
| 8 | **Guarda** | Como evito voltar ao problema? | Orçamento de performance, alertas, teste de carga no CI, painel de acompanhamento | Monitoramento ativo |
| 9 | **Registro** | O que aprendemos? | Documentar o gargalo, a correção, os números e o limite atual | Conhecimento guardado |

## Princípios

- **Uma mudança por vez**, ou não se sabe o que funcionou.
- **Medir em ambiente representativo.** Teste em máquina de desenvolvimento mente.
- **Escalar é a última opção.** Corrigir o gargalo costuma custar menos que adicionar servidores.
- **Parar quando a meta for atingida.** Otimizar além disso é desperdício e aumenta a complexidade.
- **Saída de emergência:** se o diagnóstico mostrar que o limite é arquitetural, o fluxo para e propõe redesenho ou migração.

Outros fluxos: [FLUXO-PROJETO-NOVO.md](FLUXO-PROJETO-NOVO.md), [FLUXO-FEATURE.md](FLUXO-FEATURE.md), [FLUXO-FEATURE-LEGADO.md](FLUXO-FEATURE-LEGADO.md).
