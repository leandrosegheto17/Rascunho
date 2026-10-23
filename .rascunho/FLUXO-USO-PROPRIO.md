# Fluxo de aplicação para uso próprio

Aplicação sem fins comerciais, para uso próprio, em servidor local ou camada gratuita. A pergunta central deixa de ser "alguém pagaria?" e passa a ser "isso vale o meu tempo e funciona na minha infraestrutura?". Cada fase termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Necessidade** | Que dor ou desejo isso resolve? O que já existe pronto? | Descrever o problema e procurar alternativas prontas ou open source | Construir, adaptar algo existente ou desistir? |
| 2 | **Escopo pessoal** | O que é o essencial para eu usar de verdade? | Lista curta de funcionalidades, o que fica de fora, e o que é "bom o bastante" | Escopo aprovado |
| 3 | **Restrições e viabilidade** | Onde vai rodar e quanto posso gastar? | Servidor local ou camada gratuita (limites, expiração, suspensão por inatividade), stack que conheço ou quero aprender, dados e backup | Cabe no ambiente e no orçamento zero? |
| 4 | **Desenho enxuto** | Qual a estrutura mais simples que serve? | Arquitetura mínima, banco simples, telas em rascunho, decisões em poucas linhas | Desenho aprovado |
| 5 | **Preparação** | Como vou trabalhar? | Repositório, ambiente local reproduzível (ex.: Docker), tarefas pequenas, esqueleto que roda ponta a ponta | Roda "olá mundo" no destino |
| 6 | **Construção** | Cada fatia já é usável? | Fatias verticais pequenas com testes nas regras que importam, usando a aplicação desde cedo | Fatia funciona para mim |
| 7 | **Validação** | Funciona, é seguro e os dados estão a salvo? | Testes, checagem de segredos e dependências, exposição à internet, backup e restauração testados | Pronto para uso diário |
| 8 | **Implantação** | Como coloco no ar com pouco esforço? | Script ou comando único de deploy, domínio ou acesso local, plano de reversão simples | No ar |
| 9 | **Uso e manutenção** | Continua útil e funcionando? | Uso real, correções, atualização de dependências, monitoramento leve, revisão periódica | Manter, evoluir ou aposentar |

## Diferenças em relação ao fluxo de venda

- **Saem:** plano comercial, validação de preço e canais, teste com usuários externos, lançamento gradual e suporte.
- **Discovery vira necessidade.** Sem pesquisa com terceiros, a etapa mais importante é checar se já existe algo pronto que resolva.
- **Restrições de infraestrutura entram cedo.** Os limites do plano gratuito e a pausa por inatividade podem decidir a stack.
- **Dados e backup ganham peso.** Em uso próprio, perder os dados é o risco principal.
- **Segurança é proporcional.** Se ficar só na rede local, é simples. Se for exposta à internet, precisa de autenticação, HTTPS e atualização das dependências.
- **A manutenção pesa mais que o lançamento.** Uma ferramenta pessoal morre por abandono, então a fase 9 inclui a decisão de aposentar.
- **Menos cerimônia.** Especificação, desenho e tarefas cabem em um ou dois arquivos curtos.

## Em aberto

- O uso é só do autor ou também de família e amigos? Com mais gente entram login, privacidade e suporte informal, o que aproxima este fluxo do de venda ([FLUXO-PROJETO-NOVO.md](FLUXO-PROJETO-NOVO.md)).
