# Diagnóstico em produção

Usado pelos fluxos de bug, suporte e incidente quando a evidência só existe em produção. Tudo aqui é **só leitura**: correção de dado é outra ação, com confirmação própria e jeito de desfazer.

## Consulta ao banco

Só quando código, log e relato não bastam. Antes de **cada** consulta, pergunte via `AskUserQuestion` mostrando:

- **Hipótese** que a consulta vai testar e por que o resto não basta;
- **ambiente** e conta ou cliente consultado;
- a **consulta** mínima: colunas nomeadas (nunca `SELECT *`), filtro e limite de linhas;
- **risco** operacional (tabela grande, horário, bloqueio) e tempo limite.

A aprovação vale **a cada execução** e a consulta nunca na lista de permissões do projeto. Use credencial somente leitura; sem ela, entregue a consulta para o usuário rodar. Resuma o resultado, sem despejar linhas nem dado pessoal na conversa ou nos artefatos, e diga se ele **confirmou ou refutou** a hipótese.

## Logs

Ausência de linha não prova que o evento não ocorreu. Antes de concluir por ausência, confirme que: o serviço e a instância são os certos; há log dele na janela (veja uma linha qualquer); e o **nível** daquela mensagem é coletado (log informativo costuma ficar só na máquina). Descarte silencioso (`catch` vazio, filtro, `continue`) com log não coletado é parte da causa: registre. Cite a evidência por serviço, data e hora e mensagem, sem segredo, valor sensível ou dado pessoal.

## Consulta alterada pela correção

Correção que cria ou muda consulta (filtro, junção, ordenação, agrupamento, inclusive `UPDATE` e `DELETE`) mede a **antiga e a nova** no mesmo ambiente, com a chave de **pior caso** (a que alcança mais linhas), pelo método de `.claude/skills/performance/references/medicao.md`. Confira os índices que existem no banco (não só os declarados no código) e o tipo do parâmetro contra o da coluna. `UPDATE` e `DELETE` são medidos por um `SELECT` com o mesmo critério, que não mede o custo de escrita: diga o número de linhas afetadas. Índice novo só com a medição mostrando a necessidade. O antes e o depois vão para `causa.md`.

## Aviso a quem relatou

O que aconteceu, por quê e o que foi corrigido, em linguagem do processo de quem usa: sem nome de classe, tabela ou erro interno, sem culpar a pessoa e sem prazo não combinado. Enviar é ação externa: confirme o texto exato.
