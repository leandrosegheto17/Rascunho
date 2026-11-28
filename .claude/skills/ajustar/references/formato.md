# Formato do ajuste

## Revisão da spec

No topo: `**Revisão**: <N>`. Ao fim:

```markdown
## Histórico de revisões

### Revisão 2 — <AAAA-MM-DD>

- **Origem**: teste do usuário | roteiro manual reprovado
- **Mudou**: FUN-03 (alterado): <antes> → <depois>
- **Entrou**: FUN-09: <critério>
- **Saiu**: FUN-05: <motivo>
```

## Phase e tarefa no `tasks.md`

```markdown
### Phase 6: Ajuste J1

​```
T31 -> T32
​```
```

```markdown
### T31: <o que muda>

**What**: <uma frase>
**Estimativa**: 1h
**Risco**: alto
**Domínio**: não
**Criticidade**: comum
**Depends on**: —
**Reuses**: <tarefa anterior afetada e arquivo:linha>
**Requirement**: FUN-03 (revisão 2) · Ajuste: J1
**Tests**: <teste do critério revisado, que falha antes da mudança>
**Gate**: <comando>

- [ ] Concluída
```

Tarefa aberta cujo critério saiu:

```markdown
**Status**: cancelada — FUN-05 removido na revisão 2
```

O `progresso.py` tira a cancelada de todas as contas e trata a Phase `Ajuste J<n>` como lote próprio ("Lote J1 (ajuste)").
