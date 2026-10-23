# Fluxo de prova de conceito (spike)

Um experimento técnico curto para responder uma dúvida antes de se comprometer com a construção. A regra central: **o produto do spike é a resposta, não o código**. O código é descartável. Cada fase termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Pergunta** | Que dúvida exata preciso resolver? | Escrever uma pergunta só, que tenha resposta sim ou não, ou um número (ex.: "essa API aguenta 50 chamadas por segundo?"). Se houver várias, fazer vários spikes. | Pergunta única e verificável? |
| 2 | **Critério de sucesso** | O que eu aceitaria como resposta? | Definir antes o que significa "deu certo" e "deu errado", com limites numéricos quando possível | Critério escrito |
| 3 | **Limite de tempo** | Quanto vale gastar? | Fixar um prazo curto (horas ou poucos dias) e respeitá-lo. Estourar o prazo já é uma resposta: é mais difícil do que parece. | Prazo definido |
| 4 | **Experimento** | O caminho mais curto até a resposta? | Código mínimo, sem testes, sem estrutura, sem tratamento de erro, dados falsos se servir. Fazer só o que responde a pergunta. | Experimento rodando |
| 5 | **Observação** | O que aconteceu de fato? | Medir e anotar resultados, surpresas, obstáculos, comportamentos inesperados e o esforço real | Resultados coletados |
| 6 | **Conclusão** | Qual é a resposta? | Comparar com o critério de sucesso: sim, não, ou sim com ressalvas. Dizer o nível de confiança e o que ficou sem resposta. | Veredito registrado |
| 7 | **Registro** | Como guardo o aprendizado? | Nota curta: pergunta, método, resultado, conclusão, riscos descobertos e links. Guardar o código só como referência. | Registrado |
| 8 | **Descarte ou promoção** | E o código? | Descartar o código e reconstruir direito, ou, se algo for realmente reaproveitável, reescrevê-lo com testes. Nunca promover um spike direto a produto. | Código descartado ou reescrito |

## Princípios

- **Uma pergunta, um spike.**
- **Qualidade de código não importa aqui**, mas a honestidade do resultado importa.
- **Prazo curto e respeitado.** Spike sem limite vira projeto.
- **Resultado negativo é sucesso.** Descobrir que não dá para fazer antes de construir economiza muito.
- **Descartar o código.** Código de spike carrega atalhos que viram bugs.
- **Alimenta outros fluxos:** a conclusão entra em [FLUXO-PROJETO-NOVO.md](FLUXO-PROJETO-NOVO.md) (viabilidade técnica), em [FLUXO-ESCOLHA-TECNOLOGIA.md](FLUXO-ESCOLHA-TECNOLOGIA.md) ou em [FLUXO-INTEGRACAO.md](FLUXO-INTEGRACAO.md).

Outros fluxos: [FLUXO-APRENDIZADO.md](FLUXO-APRENDIZADO.md), [FLUXO-ESCOLHA-TECNOLOGIA.md](FLUXO-ESCOLHA-TECNOLOGIA.md).
