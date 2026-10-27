---
name: progresso
description: Mostra quanto do trabalho já foi concluído — tarefas feitas e faltantes, com percentual, no item em andamento e no projeto todo (ex.: "Faltam 45 de 180 tarefas: 75% concluído"). Use quando o usuário digitar /progresso ou perguntar quanto falta, e no resumo de fim de fase e na retomada de sessão. Não use para planejar, estimar prazo nem alterar tarefas.
model: sonnet
effort: low
allowed-tools:
  - Bash(python .claude/scripts/progresso.py:*)
  - Read
  - Glob
---

# Progresso

Só lê. Não altera `tasks.md`, `STATE.md` nem nenhum artefato.

## 1. Rodar

```
python .claude/scripts/progresso.py
```

Para outro item que não o da Retomada: `--item .specs/features/<pasta>`.

## 2. Mostrar

Repita as linhas do script, sem enfeite. Exemplo:

```
Item atual (.specs/features/importar-extrato): Faltam 3 de 4 tarefas: 25% concluído
Projeto: Faltam 45 de 180 tarefas: 75% concluído
```

- **Sem tarefas ainda** (antes da fase de tarefas): o script mostra o fluxo e a fase da Retomada, se houver. Se não houver Retomada, descubra a fase pelos arquivos do item (a skill do fluxo explica como) e diga em uma linha, ex.: "Fase 4 de 10 do fluxo; ainda sem tarefas". Não invente percentual.
- **Item sem `tasks.md`**: diga que o item ainda não tem tarefas.

## 3. Ler com cuidado

Diga numa linha, quando valer:

- O percentual conta só o que está em `tasks.md`; tarefas de fases ainda não planejadas não entram, então o total cresce e o percentual pode cair quando uma feature nova é planejada.
- Todas as tarefas pesam igual, qualquer que seja o tamanho.
- Uma tarefa só conta como concluída com todas as caixas `Done when` marcadas (ou `**Status**` concluído, quando não há caixas); tarefa pronta no código mas sem a marca em `tasks.md` aparece como faltante. Se os números destoarem do que foi feito, confira o `tasks.md`.

## 4. Onde mais isso aparece

- **Fim de fase:** o resumo antes da pergunta seguir / ajustar / parar traz essas linhas (regra do `CLAUDE.md`).
- **Troca de sessão:** a seção `## Retomada` de `.specs/STATE.md` grava a linha do projeto e o `/fluxo` a repete ao retomar (ver `fluxo/references/marcos.md`).
