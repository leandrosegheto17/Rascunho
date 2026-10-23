---
name: fluxo
description: Ponto de entrada dos fluxos de trabalho — entende o que o usuário quer fazer (projeto novo, feature, bug, refatoração, incidente etc.), escolhe o fluxo certo e o aciona. Use quando o usuário digitar /fluxo, disser que quer começar algo novo sem dizer como, ou perguntar quais fluxos existem.
---

# Fluxo: escolher por onde começar

## 1. Entender o pedido

Se o usuário já disse o que quer, escolha o fluxo pela tabela abaixo. Se não, pergunte em uma linha, com as opções mais comuns:

> "O que vamos fazer? A) projeto novo para vender, B) feature num projeto existente, C) corrigir um bug, D) outro (diga qual)."

Se ficar entre dois fluxos, pergunte qual, explicando a diferença em uma linha.

## 2. Fluxos

| # | Fluxo | Quando | Situação |
|---|---|---|---|
| 1 | Projeto novo (construir para vender) | Ideia de produto do zero | **Pronto**: acione a skill `projeto-novo` |
| 2 | Aplicação para uso próprio | Ferramenta pessoal, servidor local ou gratuito | Em preparação |
| 3 | Feature em projeto feito com IA | Nova funcionalidade num projeto existente | Em preparação |
| 4 | Feature em projeto legado | Nova funcionalidade em código antigo, sem testes | Em preparação |
| 5 | Performance e escala | Sistema lento ou com mais carga | Em preparação |
| 6 | Integração com terceiros | API, pagamento ou serviço externo | Em preparação |
| 7 | Redesign de interface | Mudar aparência ou experiência | Em preparação |
| 8 | Aprendizado | Projeto para estudar uma tecnologia | Em preparação |
| 9 | Investigação de incidentes | Algo quebrou em produção | Em preparação |
| 10 | Sugestão de melhoria de terceiros | Usuário ou cliente sugeriu algo | Em preparação |
| 11 | Solicitação de feature sob demanda | Cliente ou gestor pediu uma funcionalidade | Em preparação |
| 12 | Correção de bug | Algo não funciona como deveria | Em preparação |
| 13 | Refatoração e dívida técnica | Código difícil de manter | Em preparação |
| 14 | Documentar projeto existente | Projeto sem documentação ou contexto para IA | Em preparação |
| 16 | Auditoria de segurança | Revisar antes de expor ou vender | Em preparação (o agente `auditor-seguranca` já pode ser usado) |
| 17 | Prova de conceito (spike) | Testar uma dúvida técnica | Em preparação |
| 24 | Revisão de código | Revisar contribuição ou código gerado por IA | Em preparação |
| 25 | Escolha de tecnologia | Decidir stack, banco, fornecedor | Em preparação |
| 27 | Avaliação de projeto de terceiros | Antes de comprar, herdar ou adotar código | Em preparação |
| 30 | Automação de processo | Automatizar tarefa repetitiva | Em preparação |
| 32 | Suporte ao cliente | Atender usuário com problema | Em preparação |

## 3. Acionar

- **Fluxo pronto:** acione a skill indicada e deixe que ela conduza.
- **Fluxo em preparação:** diga que ainda não foi construído e ofereça:
  - conduzir manualmente, seguindo o desenho do fluxo (arquivo `FLUXO-*.md` correspondente em `.rascunho/`, se existir neste projeto), com aprovação a cada fase; ou
  - usar diretamente uma peça que já existe, quando servir (ex.: `tlc-spec-driven` para feature, `systematic-debugging` para bug, `auditor-seguranca` para auditoria).

Tudo em português.
