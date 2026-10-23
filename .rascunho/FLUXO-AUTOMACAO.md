# Fluxo de automação de processo

Automatizar uma tarefa repetitiva com script, bot, integração ou agente. A regra central: **automatizar um processo que já funciona manualmente**. Automatizar um processo confuso só produz confusão mais rápida. Cada fase termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Processo atual** | O que é feito hoje, passo a passo? | Fazer à mão e anotar cada passo, entradas, saídas, decisões, exceções e quem participa. Medir tempo e frequência. | Processo descrito |
| 2 | **Vale automatizar?** | O ganho compensa o custo? | Tempo economizado por mês versus tempo para construir e manter. Considerar erros evitados e risco de falha. | Retorno positivo? |
| 3 | **Escopo** | O que automatizar e o que ficar manual? | Cobrir o caminho comum (a maior parte dos casos) e deixar as exceções raras para o humano, com aviso claro quando ocorrerem | Escopo definido |
| 4 | **Escolha da ferramenta** | Qual o meio mais simples que serve? | Preferir o mais simples e mantido: recurso nativo da ferramenta, agendador, script curto, serviço de automação pronto. Código próprio e agentes de IA só quando necessário ([FLUXO-ESCOLHA-TECNOLOGIA.md](FLUXO-ESCOLHA-TECNOLOGIA.md)). | Ferramenta escolhida |
| 5 | **Desenho seguro** | O que pode dar errado? | Permissões mínimas, segredos fora do código, idempotência (rodar duas vezes não duplica), tratamento de falha parcial, limite de ação em massa, modo de simulação | Desenho aprovado |
| 6 | **Implementação** | Funciona nos casos reais? | Construir o caminho comum, com registro de cada ação, e testar com dados reais em cópia ou ambiente de teste | Resultado igual ao manual |
| 7 | **Execução assistida** | Posso confiar sem olhar? | Rodar em paralelo ao manual por algum tempo, ou com aprovação humana antes de agir. Comparar resultados. | Confiança estabelecida? |
| 8 | **Operação** | Como saberei se falhar? | Alertas de falha, relatório do que foi feito, botão de pausa, e dono definido. Falha silenciosa é o pior caso. | Monitoramento ativo |
| 9 | **Manutenção** | Continua funcionando quando algo muda? | Revisar quando o sistema de origem, a API ou o processo mudar. Documentar como funciona, o que faz e como desligar. | Documentado e com dono |

## Princípios

- **Entender antes de automatizar.** Se não dá para descrever o processo, não dá para automatizá-lo.
- **Começar pequeno e crescer.** Um passo automatizado e confiável vale mais que um fluxo todo frágil.
- **Falha visível.** Automação que falha em silêncio causa dano acumulado.
- **Ação destrutiva exige trava.** Apagar, enviar ou pagar em massa pede simulação e limite.
- **Humano nas decisões de risco.** Automatizar o trabalho braçal e manter a pessoa onde há julgamento.
- **Automação também é código.** Precisa de dono, versão e documentação.
- **Agentes de IA numa automação** têm saída variável: validar o que eles produzem antes de qualquer ação irreversível.

Outros fluxos: [FLUXO-INTEGRACAO.md](FLUXO-INTEGRACAO.md), [FLUXO-USO-PROPRIO.md](FLUXO-USO-PROPRIO.md), [FLUXO-ESCOLHA-TECNOLOGIA.md](FLUXO-ESCOLHA-TECNOLOGIA.md).
