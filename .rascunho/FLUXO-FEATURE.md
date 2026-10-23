# Fluxo de feature em projeto existente feito com IA

O projeto já existe, então a incerteza está menos em "construir ou não" e mais em **entender o que já está lá e não quebrar nada**. Projetos feitos com IA costumam ter padrões inconsistentes, pouca documentação e testes irregulares. Por isso a primeira fase é ler o projeto. Cada fase termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Pedido** | O que a feature precisa fazer, para quem, e como saberei que está pronta? | Descrição curta, critérios de aceite testáveis, o que fica de fora | Escopo claro? |
| 2 | **Reconhecimento** | Onde isso entra no código existente? | Mapear módulos afetados, padrões em uso, testes existentes, dívidas e pontos frágeis | Entendi o suficiente para mexer? |
| 3 | **Plano** | Qual o menor caminho seguro? | Plano curto: arquivos a alterar, tarefas pequenas, riscos, ordem de execução | Plano aprovado |
| 4 | **Rede de proteção** | Se eu quebrar algo, vou perceber? | Rodar a suíte atual como linha de base, escrever testes do comportamento existente que será tocado e o teste da feature antes do código | Linha de base verde |
| 5 | **Implementação** | A feature funciona seguindo os padrões do projeto? | Fatias pequenas, com testes, em branch isolada, seguindo as convenções que já existem | Cada fatia passa nos testes |
| 6 | **Verificação** | Funciona de verdade, sem regressão e sem risco novo? | Suíte completa, uso real da feature, revisão do diff, checagem de segurança e de dependências novas | Pronto para integrar |
| 7 | **Integração** | Como entra no projeto? | Merge ou PR, atualização de docs e contexto do projeto, deploy se houver | Integrado |

## Diferenças em relação aos outros fluxos

- **Saem:** discovery, viabilidade, plano comercial, desenho de arquitetura nova e preparação de ambiente. Tudo isso já existe.
- **Reconhecimento é a fase nova e a mais valiosa.** Sem ela a IA inventa padrões próprios e duplica o que já existe.
- **Teste antes do código.** Em código gerado por IA a rede de proteção costuma ser frágil, então a linha de base verde vem antes de qualquer mudança.
- **Convenções do projeto mandam.** A feature segue o estilo atual, mesmo que haja algo melhor em outro lugar. Refatorar à parte vira outra tarefa.
- **Branch isolada e diff pequeno.** Facilita revisar e reverter.
- **Atualizar o contexto na integração.** Se o projeto tem arquivo de instruções para IA, ele fica em dia, para a próxima feature não recomeçar do zero.
- **Escopo contido.** Se o reconhecimento revelar que a feature exige mudança grande de arquitetura, o fluxo para e escala para o fluxo de projeto novo ou de refatoração.

## Em aberto

- A feature é sempre pequena (um ou dois dias) ou às vezes grande o bastante para várias tarefas em paralelo? Se for grande, a fase 3 ganha um passo de decomposição.

Outros fluxos: [FLUXO-PROJETO-NOVO.md](FLUXO-PROJETO-NOVO.md), [FLUXO-USO-PROPRIO.md](FLUXO-USO-PROPRIO.md).
