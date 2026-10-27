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

**Responda só com as linhas que o script imprimiu, copiadas como estão**: sem tabela, sem título, sem recalcular, sem analisar o projeto por conta própria. Mesmo formato em todo projeto:

```
Item atual (.specs/features/importar-extrato): Faltam 3 de 4 tarefas: 25% concluído
Projeto: Faltam 45 de 180 tarefas: 75% concluído
```

Só acrescente algo nestes casos, em **uma linha**:

- **"Sem tarefas ainda":** o projeto não usa `tasks.md` (ou ainda não chegou à fase de tarefas). Diga isso e pare; não invente percentual a partir de outros arquivos. Se a Retomada não existir, descubra a fase pelos arquivos do item (a skill do fluxo explica como).
- **Item atual sem tarefas, projeto com tarefas:** diga que o item ainda não tem `tasks.md`.
- **Linha de Retomada que contradiz os arquivos** (ex.: fase já concluída): avise que a Retomada está desatualizada.

## 3. Se perguntarem como é calculado

Só então explique: conta títulos `### T<n>:` dos `tasks.md` de `.specs/`; tarefa concluída = todas as caixas `Done when` marcadas (ou `**Status**` concluído, sem caixas); só entram tarefas já planejadas, então o total cresce quando uma feature nova é planejada; todas pesam igual.

## 4. Onde mais isso aparece

- **Fim de fase:** o resumo antes da pergunta seguir / ajustar / parar traz essas linhas (regra do `CLAUDE.md`).
- **Troca de sessão:** a seção `## Retomada` de `.specs/STATE.md` grava a linha do projeto e o `/fluxo` a repete ao retomar (ver `fluxo/references/marcos.md`).
