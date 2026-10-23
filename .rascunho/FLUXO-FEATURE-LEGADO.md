# Fluxo de feature em projeto legado

O código é antigo, quase sem testes, escrito por pessoas que talvez não estejam mais lá, e o comportamento real muitas vezes não está documentado em lugar nenhum. A pergunta central é: **como mexer sem entender tudo e sem quebrar o que funciona há anos?** Cada fase termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Pedido** | O que a feature precisa fazer e como saberei que está pronta? | Descrição curta, critérios de aceite testáveis, o que fica de fora | Escopo claro? |
| 2 | **Arqueologia** | Como essa parte do sistema funciona de fato? | Ler o código afetado, rastrear fluxos de dados, consultar histórico do git e documentos antigos, perguntar a quem conhece, observar o comportamento em execução | Entendi o suficiente do trecho que vou tocar? |
| 3 | **Fronteira e risco** | Onde posso mexer com segurança? | Achar costuras (pontos onde se insere código novo sem alterar o antigo), mapear dependências, clientes e integrações, avaliar o raio de impacto | Existe um caminho de baixo impacto? |
| 4 | **Rede de proteção** | Como saberei se quebrei algo? | Testes de caracterização: registrar o comportamento atual (mesmo o estranho) antes de mudar. Se o ambiente não roda, primeiro fazê-lo rodar. | Comportamento atual capturado |
| 5 | **Plano** | Qual o menor desvio possível? | Plano curto: código novo isolado ao lado do antigo, ponto único de integração, ordem de passos, plano de reversão | Plano aprovado |
| 6 | **Implementação** | A feature funciona sem alterar o que existe? | Fatias pequenas em branch isolada, teste primeiro, mudança mínima no código antigo, feature flag quando possível | Cada fatia passa nos testes de caracterização e nos novos |
| 7 | **Verificação** | Funciona e não houve regressão? | Suíte completa, teste manual dos fluxos vizinhos, revisão do diff, checagem de segurança e de dependências | Pronto para liberar |
| 8 | **Liberação cuidadosa** | Como colocar no ar com reversão fácil? | Deploy com flag desligada ou liberação gradual, monitoramento, reversão testada | No ar e estável |
| 9 | **Registro** | O próximo a mexer aqui vai sofrer menos? | Documentar o que foi descoberto, os testes de caracterização e as armadilhas | Conhecimento guardado |

## Diferenças em relação a "feature em projeto feito com IA"

- **Arqueologia no lugar de reconhecimento.** Em código com IA o padrão existe, só é inconsistente. No legado o conhecimento se perdeu, então é preciso reconstituí-lo.
- **Teste de caracterização, não só de linha de base.** Quem escreveu o código sumiu e não há critério de correto, então o teste registra o que o sistema faz hoje, mesmo que pareça errado.
- **Mudar o mínimo do código antigo.** A feature entra ao lado, por uma costura, e não dentro do emaranhado. Refatorar fica para outra tarefa.
- **Liberação mais cautelosa.** Feature flag, liberação gradual e reversão pronta são regra e não exceção.
- **Fazer o ambiente rodar pode ser a primeira tarefa.** Versão antiga de linguagem, dependências sem suporte e build manual são comuns.
- **Registro obrigatório.** Cada passagem deixa o terreno mais conhecido.
- **Saída de emergência.** Se a arqueologia mostrar que o impacto é alto demais, o fluxo para e propõe refatoração prévia, ou uma solução fora do legado (um serviço novo ao lado).

## Em aberto

- O legado tem ambiente de teste ou staging, ou tudo é testado só em produção? Isso muda o peso das fases 7 e 8.

Outros fluxos: [FLUXO-PROJETO-NOVO.md](FLUXO-PROJETO-NOVO.md), [FLUXO-USO-PROPRIO.md](FLUXO-USO-PROPRIO.md), [FLUXO-FEATURE.md](FLUXO-FEATURE.md).
