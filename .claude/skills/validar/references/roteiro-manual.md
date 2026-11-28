# Modelo de `roteiro-manual.md`

Um bloco por critério com `Prova: manual`. Quem testa é o usuário: escreva passos que dispensem conhecer o código. Nunca use dado real de terceiros no roteiro.

```markdown
# Roteiro manual: <item>

- **Gerado em**: <AAAA-MM-DD> · **Revisão da spec**: <N> · **Commit**: <hash curto>

## FUN-07: <critério em uma linha>

- **Por que é manual**: <motivo>
- **Preparação**: <ambiente, endereço, usuário de teste, dados, flag>
- **Passos**:
  1. <ação exata>
- **Esperado**: <o que se vê, com os valores>
- **Como verificar**: <onde olhar: tela, registro, e-mail>
- **Resultado**: pendente
```

**Resultado** aceita: `pendente`, `aprovado (<data>)`, `reprovado (<data>): <o que se viu>` ou `dispensado (<data>) — <motivo>`. Só o usuário aprova ou dispensa.
