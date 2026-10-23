---
name: mockup-visual
description: Mockup visual enxuto de um projeto com interface — 2 ou 3 direções visuais de uma tela-chave para escolher, depois um guia de estilo (tokens.css, componentes base, padrões de vazio/carregando/erro) e 2 a 3 telas-chave em PC e celular, publicados numa galeria para aprovação; na validação, coloca prints do app ao lado do mockup. Use na fase 7 do projeto novo, depois do desenho (design.md), e na fase 10 para a comparação. Não desenha todas as telas e não implementa o código do produto. Pule em projetos sem interface.
model: opus
effort: high
---

# Mockup visual (fase 7, e comparação na fase 10)

O objetivo é **o produto final não sair diferente do que foi aprovado**, sem desenhar todas as telas. Quem garante isso é um conjunto único de cores, fontes e componentes (o guia de estilo), que todas as telas reutilizam. Depois de aprovado, o mockup é a **fonte de verdade da aparência**: mudança visual começa nele, não no código.

Rende melhor em **Opus** nas direções e no guia. Se a sessão estiver em outro modelo, avise: "O mockup rende melhor em Opus: use `/model opus`."

## Pré-requisitos

- `.specs/features/<mvp>/spec.md` (requisitos) e `design.md` (telas e fluxos, se o desenho os listou).
- Projeto sem interface (API, CLI, automação): diga que a fase não se aplica e pare.
- Use a skill `frontend-design` como apoio de qualidade visual (sem estética genérica).

## Etapa 1: Direções → `.specs/mockup/direcoes/`

1. Escolha **uma tela-chave**: a mais usada ou a mais densa do MVP. Diga qual e por quê.
2. Produza **2 ou 3 direções** dessa tela, cada uma com paleta, tipografia e densidade próprias, em PC e celular (a mesma página responsiva). Detalhes em [references/estrutura.md](references/estrutura.md).
3. Toda direção já respeita o contraste mínimo: o usuário escolhe entre opções válidas.
4. Publique a galeria das direções (ver "Publicação") e peça a escolha. Misturas são aceitas ("cores da A, densidade da B").

**Pare para aprovação.** As direções não escolhidas ficam como histórico e nunca são referência de implementação.

## Etapa 2: Guia de estilo e telas-chave → `.specs/mockup/`

1. `tokens.css`: **única** definição de cores, fontes, tamanhos de texto, espaçamentos, raios, sombras e pontos de quebra, como variáveis CSS.
2. `guia.html`: os componentes base (botão em seus estados, campo com erro e ajuda, cartão, lista ou tabela, aviso, navegação) e os padrões de **vazio, carregando e erro**, desenhados uma vez. Inclua a tabela de contraste dos pares texto/fundo.
3. `telas/<tela>.html`: **2 ou 3 telas-chave** do MVP (a da direção e as mais importantes do fluxo principal), responsivas, com dados de exemplo realistas no próprio HTML.
4. Confira o checklist de [references/estrutura.md](references/estrutura.md) e publique a galeria.

**Pare para aprovação.** Ajustes mudam `tokens.css` e as páginas e republicam no mesmo link.

As demais telas **não são desenhadas**: a implementação as monta com os componentes do guia.

## Etapa 3: Comparação (fase 10)

Chamada pelo orquestrador na validação, com o app rodando localmente:

1. Tire prints das telas-chave do app em PC (1440 × 900) e celular (390 × 844), com a skill `playwright-skill` ou `chrome-devtools`, em `.specs/mockup/comparacao/<data>/`.
2. Acrescente à galeria uma seção "Mockup × app", com cada tela lado a lado, e republique.
3. Rode `python .claude/scripts/checar-tokens.py <pasta do código>` e informe o resultado.
4. Liste as diferenças que você nota. **Quem decide se está aceitável é o usuário.** Diferença aceita vira registro; diferença rejeitada vira tarefa de correção.

## Publicação

A galeria é `.specs/mockup/index.html` (ou `direcoes/index.html` na etapa 1). Publique-a como Artifact (carregue antes a skill `artifact-design`), com `tokens.css`, `guia.html`, as telas e as imagens como arquivos de apoio. Cada rodada republica no mesmo link. Diga o link ao usuário.

## Ao terminar cada etapa

Responda só com o link da galeria, 3 a 5 linhas do que foi decidido e as opções **seguir / ajustar / parar**.

## Regras

- Nenhum valor de cor, fonte ou espaçamento fora de `tokens.css`. Precisou de um valor novo, ele vira token.
- Mesma fonte no mockup e no app (mesma origem, mesmos pesos).
- HTML semântico e classes com nome de componente (`cartao-resumo`, `botao-primario`): é o que a implementação vai copiar.
- Tudo em português.

Simplificado a partir da skill `visual-mockup-drafting` do `.claude_legado`.
