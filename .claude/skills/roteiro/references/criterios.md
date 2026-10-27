# Critérios para quebrar em features

## Fatia vertical

Uma feature está bem fatiada quando, ao terminar:

- alguém consegue **usar** o que ela entrega, do começo ao fim (dado, regra, tela ou API);
- há **critério de aceite testável** de ponta a ponta, não só testes de camada;
- ela pode ser **integrada e liberada** sozinha sem deixar o produto quebrado;
- o que falta nas outras features não a impede de funcionar.

## Anti-padrões

| Quebra ruim | Por quê | Alternativa |
|---|---|---|
| "Banco", "API", "Front" como features | Ninguém usa nada até a última terminar; o risco de integração vem no fim | Cada feature atravessa as camadas para um fluxo de valor |
| Uma feature "Geral" com tudo | `tasks.md` de 170 tarefas, sem ponto de aprovação no meio | Divida por fluxo de valor |
| Features por tela | Telas sem regra ou regras sem tela | Feche um fluxo completo por vez |
| Feature de "melhorias" ou "ajustes" | Sem critério de pronto | Distribua nas features a que pertencem |

## Ordem

1. O que **destrava** os outros (fundação, conta e acesso, isolamento de dados).
2. O que tem a **maior incerteza** técnica ou de negócio (descobrir cedo que não dá é barato).
3. O que o usuário **mais valoriza**, depois do que destrava.
4. Cobrança, notificações e extras por último, salvo se forem o negócio.

## Tamanho

| Tamanho | Tarefas (estimativa) | Observação |
|---|---|---|
| P | até 20 | Cabe em 1 ou 2 lotes de construção |
| M | até 50 | Referência: a `fundacao` do Gestão da Pelada teve 49 |
| G | até 80 | Limite do `progresso.py`; acima disso ele avisa |

A estimativa nasce do número de requisitos e componentes: cerca de 2 a 4 tarefas por requisito de comportamento, mais as tarefas de infraestrutura da feature. É uma conta de cabeça para decidir a quebra, não um compromisso: o número real sai do `tasks.md`.

## Quando **não** dividir

- Escopo de um fluxo de valor só, mesmo que tenha muitas telas.
- Projeto pessoal pequeno (fluxo 2) que o tlc classifica como Small ou Medium.
- Divisão que só cria burocracia: se duas features sempre seriam integradas juntas, são uma.
