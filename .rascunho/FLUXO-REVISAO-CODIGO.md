# Fluxo de revisão de código

Revisar uma contribuição de uma pessoa ou de uma IA antes de integrá-la. A regra central: **revisar o que mudou contra o que foi pedido**, com atenção redobrada ao código gerado por IA, que parece correto antes de ser. Cada fase termina com uma decisão (aprovar, pedir mudanças ou recusar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Contexto** | O que a mudança deveria fazer? | Ler a descrição, a tarefa ou o pedido original e os critérios de aceite antes de ver o código | Objetivo entendido? |
| 2 | **Tamanho e escopo** | A mudança é revisável? | Ver o tamanho do diff e se mistura assuntos (feature, refatoração, formatação). Pedir para dividir se for grande demais. | Escopo revisável? |
| 3 | **Verificação automática** | O que as máquinas já checam? | Confirmar que build, testes, lint e varreduras de segurança passam. Não gastar atenção humana no que a ferramenta resolve. | Checagens verdes? |
| 4 | **Correção** | Faz o que foi pedido, inclusive nos casos difíceis? | Ler a lógica, casos limite, erros, concorrência, dados vazios ou inválidos. Executar a mudança, não só lê-la. | Comportamento correto? |
| 5 | **Testes** | Os testes provam alguma coisa? | Cobrem o critério de aceite e os erros? Falhariam se o código estivesse errado? Cuidado com teste que só repete a implementação. | Testes confiáveis? |
| 6 | **Segurança e dados** | Abre alguma porta? | Entrada validada, autorização em cada acesso, segredos fora do código, consultas seguras, logs sem dado sensível, dependências novas justificadas | Sem risco novo? |
| 7 | **Design e consistência** | Combina com o projeto? | Segue convenções e camadas existentes, não duplica o que já há, nomes claros, complexidade proporcional. Sem abstração sem necessidade. | Coerente com o projeto? |
| 8 | **Armadilhas de IA** | O que a IA costuma errar? | Funções ou pacotes que não existem, API usada de forma errada, tratamento de erro engolido, código morto, mudanças fora do pedido, testes que foram enfraquecidos ou apagados | Sem sinais de alucinação? |
| 9 | **Retorno** | O autor sabe o que fazer? | Comentários específicos e acionáveis, separando o que bloqueia do que é sugestão. Explicar o porquê. Reconhecer o que está bom. | Retorno entregue |
| 10 | **Decisão e reteste** | Pode entrar? | Aprovar, ou pedir mudanças e revisar de novo só o que mudou. Ao aprovar, confirmar que a descrição e a documentação refletem o resultado. | Aprovado, ou nova rodada |

## Princípios

- **Revisar contra o pedido**, não só contra o gosto.
- **Executar, não só ler.** Código lido parece correto.
- **Separar bloqueio de sugestão**, para a revisão não virar discussão de estilo.
- **Quem pediu o código para a IA continua responsável por ele.** O revisor é a segunda checagem e não a primeira.
- **Diff pequeno é revisão boa.** Revisão de diff gigante vira carimbo.
- **Teste enfraquecido para passar** é bandeira vermelha, em especial em código de IA.

Outros fluxos: [FLUXO-FEATURE.md](FLUXO-FEATURE.md), [FLUXO-BUG.md](FLUXO-BUG.md), [FLUXO-SEGURANCA.md](FLUXO-SEGURANCA.md).
