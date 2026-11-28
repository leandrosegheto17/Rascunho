# Modelo de `.specs/projeto/regras-execucao.md`

Lido antes do primeiro lote por `/rascunho`, `/executar` e `/validar`. Só o que evita erro ou parada; até ~60 linhas. O que se firmar passa para o contexto do projeto e sai daqui.

```markdown
# Regras de execução: <projeto>

## Comandos

| Para | Comando | Observação |
|---|---|---|
| Typecheck | | |
| Testes de um pacote | | reporter mínimo |
| Subir serviços | | porta, nome do container |

## Armadilhas

- <o que acontece> → <o que fazer>

## Testes que já falham

| Teste | Desde | Motivo conhecido |
|---|---|---|

(nenhum: escreva "nenhum, medido em <data>")

## Lições

| Data | Lição |
|---|---|
```

Falha que está em **Testes que já falham** não bloqueia; falha nova bloqueia. Entrar nessa lista exige aprovação do usuário: não é lugar para esconder teste quebrado pela mudança em curso. Sem segredo, senha ou URL com credencial.
