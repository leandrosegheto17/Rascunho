# Fluxo de projeto novo: construir um software e vender

Ciclo de vida de um produto, do zero. O princípio: **reduzir incerteza o mais barato possível antes de gastar com construção**. Cada fase responde uma pergunta e termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Ideia** | Qual problema, para quem, e por que agora? | Escrever a ideia numa página, listar hipóteses e o que seria preciso ser verdade | Vale investigar? |
| 2 | **Discovery** | O problema é real e dói o bastante? | Conversar com usuários, analisar alternativas e concorrentes, buscar evidência | O problema se confirma? |
| 3 | **Solução e valor** | Qual a menor solução que resolve o problema e que alguém usaria ou pagaria? | Esboços, protótipo clicável, teste de interesse | A solução faz sentido para o usuário? |
| 4 | **Viabilidade técnica** | Dá para construir, com que risco? | Spike (teste técnico descartável) nas partes incertas, avaliação de stack, integrações, segurança, legal e dados | O risco técnico é aceitável? |
| 5 | **Viabilidade de negócio** | Os números fecham? | Preço, custo, canais, ponto de equilíbrio | Segue, ajusta ou para? |
| 6 | **Definição do MVP** | O que entra e o que fica de fora, e como saberemos que deu certo? | Escopo mínimo, requisitos, métricas de sucesso, critério de parada | Escopo e métricas aprovados |
| 7 | **Desenho** | Como será estruturado? | Arquitetura enxuta, decisões registradas, desenho das telas, riscos de segurança | Desenho aprovado |
| 8 | **Preparação** | Como vamos trabalhar? | Time e papéis, quebra em tarefas pequenas, repositório, CI/CD, ambientes e esqueleto funcional ponta a ponta | Pronto para construir |
| 9 | **Construção** | Estamos entregando valor a cada ciclo? | Fatias verticais pequenas, com testes e revisão a cada tarefa | Cada fatia atende o critério de aceite |
| 10 | **Validação** | Está correto, seguro e utilizável? | Testes, auditoria de segurança, teste com usuários reais | Pronto para liberar |
| 11 | **Lançamento** | Como colocar no ar com segurança? | Staging, liberação gradual, plano de reversão | Liberar |
| 12 | **Operação e aprendizado** | A hipótese se confirmou? | Monitoramento, métricas, feedback, incidentes | Persistir, pivotar ou encerrar |

## Princípios

- **Não é uma cascata.** É um funil com laços: se a viabilidade falhar, volta-se à solução; se a validação falhar, volta-se à construção. Cada fase pode terminar em "parar", e isso é um resultado válido.
- **Discovery e solução vêm antes de qualquer especificação.** Até a fase 3 o foco é evidência, não documento.
- **Protótipos e spikes entram cedo.** Dissolvem a incerteza mais barato que qualquer análise escrita.
- **Esqueleto funcional ponta a ponta na preparação.** Uma versão mínima que vai do usuário ao deploy já na fase 8, para o pipeline nunca ser surpresa.
- **Construção por fatias que entregam valor**, não por camadas técnicas.
- **Métricas e critério de parada nascem no MVP**, não depois do lançamento.
- **Segurança, legal e dados percorrem as fases 4 a 11.** Não são uma etapa isolada.
- **A fase 12 realimenta a 1.** O aprendizado vira a próxima ideia.

## Em aberto

- Time (pessoas ou agentes) fica na fase 8; pode entrar antes se já estiver definido.
- A fase 5 (viabilidade de negócio) é **opcional** (decidido em 2026-10-23). Se pulada, a decisão final registra que a viabilidade comercial não foi avaliada.

## Próximo passo

Buscar nas fontes o que existe de melhor para cada fase: `.claude_legado`, `.tlc`, `.superpowers`, `.anthropic-skills`, `.speckit`, `.bmad`, `.openspec`, `.wshobson`, `.anthropic-plugins`, `.awesome` e a web.
