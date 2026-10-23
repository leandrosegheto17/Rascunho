# Fluxo de redesign de interface

Mudar a aparência ou a experiência sem mudar as regras de negócio. A regra central: **o desenho aprovado é a fonte de verdade**, e a implementação é comparada com ele. Cada fase termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Motivo e meta** | Por que redesenhar e como saberemos que melhorou? | Descrever o problema (confusão, aparência datada, conversão baixa, acessibilidade), métricas-alvo e o que não muda | Vale o esforço? |
| 2 | **Inventário** | O que existe hoje? | Mapear telas, fluxos, componentes, estilos e inconsistências, com capturas de tela do estado atual | Estado atual documentado |
| 3 | **Pesquisa** | Onde os usuários travam? | Analisar uso real, feedback, testes rápidos com usuários, referências do mercado | Problemas priorizados |
| 4 | **Direções** | Que caminhos visuais existem? | Duas ou três direções de uma tela-chave: identidade, tipografia, cores, densidade | Direção escolhida |
| 5 | **Sistema de design** | Como manter consistência? | Tokens (cores, espaçamento, tipografia), componentes base, regras de uso, acessibilidade (contraste, teclado, leitor de tela) | Sistema aprovado |
| 6 | **Mockup completo** | Como fica cada tela? | Todas as telas, versão desktop e celular, estados (vazio, carregando, erro, sucesso), em protótipo navegável | Mockup aprovado: vira fonte de verdade |
| 7 | **Plano de migração** | Em que ordem e com que risco? | Tela a tela ou fluxo a fluxo, coexistência do antigo e do novo, flag para alternar, testes de regressão do comportamento | Plano aprovado |
| 8 | **Implementação** | A tela reproduz o mockup? | Começar pelos tokens e componentes, depois as telas, com comparação visual automática contra o mockup | Diferença visual dentro do limite |
| 9 | **Verificação** | Funciona, é acessível e nada quebrou? | Testes funcionais, auditoria de acessibilidade, teste em vários dispositivos e navegadores, teste com usuários | Pronto para liberar |
| 10 | **Liberação e medição** | A meta foi atingida? | Liberação gradual (teste A/B quando couber), comparar métricas com a linha de base, coletar feedback | Manter, ajustar ou reverter |

## Princípios

- **Regras de negócio não mudam.** Se mudarem, vira outro fluxo (feature).
- **Mudança visual começa no mockup**, e não no código.
- **Acessibilidade é requisito**, não revisão final.
- **Migração gradual** reduz o risco de o usuário perder a familiaridade de uma vez só.
- **Saída de emergência:** se a pesquisa mostrar que o problema é de fluxo e não de aparência, o fluxo para e propõe uma mudança de produto.

Outros fluxos: [FLUXO-FEATURE.md](FLUXO-FEATURE.md), [FLUXO-PERFORMANCE.md](FLUXO-PERFORMANCE.md), [FLUXO-INTEGRACAO.md](FLUXO-INTEGRACAO.md).
