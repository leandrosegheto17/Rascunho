# Fluxo de refatoração e dívida técnica

O código funciona, mas está difícil de entender, mudar ou testar. A regra central: **mudar a estrutura sem mudar o comportamento**, em passos pequenos, sempre com testes verdes. Cada fase termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Motivo** | Que dor a dívida causa hoje? | Ligar a dívida a um custo real: bugs recorrentes, features lentas, medo de mexer, onboarding difícil. Sem custo, não há porquê. | Vale pagar essa dívida agora? |
| 2 | **Alvo e meta** | O que exatamente vai mudar e como saberei que melhorou? | Delimitar o trecho, definir o resultado (ex.: função de 400 linhas dividida, dependência circular removida) e uma métrica | Escopo e meta claros |
| 3 | **Mapeamento** | O que depende disso? | Quem chama, quem é chamado, contratos públicos, dados e integrações afetados | Raio de impacto conhecido |
| 4 | **Rede de proteção** | Como saberei que o comportamento não mudou? | Testes de caracterização do comportamento atual antes de mexer. Sem testes, não se refatora. | Linha de base verde |
| 5 | **Plano em passos** | Qual a sequência segura? | Quebrar em passos pequenos e reversíveis, cada um terminando com o sistema funcionando. Preferir mudar por camadas paralelas (novo ao lado do antigo) a reescrever. | Plano aprovado |
| 6 | **Execução** | Cada passo preserva o comportamento? | Um passo por vez: mudar, rodar testes, commitar. Nunca misturar com feature ou correção. | Testes verdes a cada passo |
| 7 | **Verificação** | Melhorou de verdade e nada mudou por fora? | Suíte completa, comparar a métrica antes e depois, checar desempenho e revisar o diff | Meta atingida sem regressão? |
| 8 | **Integração** | Como entra com baixo risco? | PRs pequenos e frequentes em vez de um grande, liberação gradual se o trecho for crítico | Integrado |
| 9 | **Registro** | O que ficou melhor e o que sobrou? | Atualizar documentação e convenções, anotar a dívida remanescente e como evitar que volte | Registrado |

## Princípios

- **Comportamento constante.** Se algo observável mudou, deixou de ser refatoração.
- **Passos pequenos.** Um passo que não cabe em poucas horas deve ser quebrado.
- **Não misturar com feature ou bug.** Cada mudança tem um motivo, para poder ser revertida sozinha.
- **Refatore o que vai ser tocado.** Código estável que ninguém muda pode ficar como está.
- **Dívida tem juros.** Priorizar a que mais atrapalha, não a mais feia.
- **Parar quando a meta for atingida.** Refatorar por perfeccionismo é desperdício.
- **Saída de emergência:** se faltarem testes e for impossível criá-los, considerar reescrita isolada com execução paralela (estrangular o antigo aos poucos).

Outros fluxos: [FLUXO-FEATURE-LEGADO.md](FLUXO-FEATURE-LEGADO.md), [FLUXO-BUG.md](FLUXO-BUG.md), [FLUXO-PERFORMANCE.md](FLUXO-PERFORMANCE.md).
