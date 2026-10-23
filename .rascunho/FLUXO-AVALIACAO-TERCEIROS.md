# Fluxo de avaliação de projeto de terceiros

Avaliar um código ou produto de outra pessoa antes de comprar, herdar, contratar, adotar ou contribuir. A regra central: **descobrir o que realmente se está levando**, incluindo o que o vendedor ou autor não mencionou. Cada fase termina com uma decisão (seguir, renegociar ou recusar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Objetivo** | Por que avaliar e o que decidirá o resultado? | Definir o motivo (comprar, herdar, adotar como dependência, contratar quem fez) e o que seria um bom resultado | Critérios de decisão definidos |
| 2 | **Acesso e escopo** | O que posso examinar? | Obter o código, o ambiente, a documentação e o histórico. Limitar o que não for compartilhável e registrar o que não foi visto. | Material suficiente? |
| 3 | **Legal e propriedade** | O que é permitido fazer com isso? | Licença do código e das dependências, titularidade (quem escreveu, contratos), marcas, dados pessoais envolvidos, obrigações de uso | Situação legal clara? |
| 4 | **Execução** | Funciona do jeito que dizem? | Instalar do zero, rodar, testar os fluxos principais. Comparar com o prometido. | Funciona como anunciado? |
| 5 | **Qualidade do código** | Em que estado está? | Estrutura, legibilidade, duplicação, tamanho de arquivos, cobertura e qualidade dos testes, consistência. Amostra representativa se for grande. | Estado de qualidade avaliado |
| 6 | **Segurança** | Que riscos vêm junto? | Dependências vulneráveis, segredos no código e no histórico, autenticação e autorização, configuração ([FLUXO-SEGURANCA.md](FLUXO-SEGURANCA.md)) | Riscos mapeados |
| 7 | **Dependências e infraestrutura** | Do que depende? | Bibliotecas abandonadas, versões antigas, serviços pagos de terceiros, contas necessárias, custo mensal de rodar, bloqueio por fornecedor | Dependências avaliadas |
| 8 | **Saúde e sustentabilidade** | Dá para manter? | Atividade recente do projeto, quem mantém, histórico de correções, documentação, dependência de uma pessoa só ("fator ônibus") | Custo de manter estimado |
| 9 | **Custo total e decisão** | Vale a pena? | Somar o preço, o custo de corrigir os problemas encontrados e de manter. Comparar com construir do zero. Decidir: adotar, adotar com condições, renegociar ou recusar. | Decisão fundamentada |
| 10 | **Relatório** | Como registrar? | Resumo, achados por gravidade, custo estimado, riscos e condições. Guardar para negociação e para o futuro. | Relatório entregue |

## Princípios

- **Verificar, não confiar.** Demonstração e apresentação mostram o melhor caso.
- **Executar do zero.** Se ninguém além do autor consegue rodar, isso é um achado.
- **O histórico do git conta a história real**: quem mexe, com que frequência, quando parou.
- **Licença e titularidade primeiro.** Um código excelente que não se pode usar não vale nada.
- **Estimar o custo de corrigir**, não só listar problemas.
- **Registrar o que não foi visto.** Uma limitação do escopo é parte do resultado.

Outros fluxos: [FLUXO-ESCOLHA-TECNOLOGIA.md](FLUXO-ESCOLHA-TECNOLOGIA.md), [FLUXO-DOCUMENTAR.md](FLUXO-DOCUMENTAR.md), [FLUXO-SEGURANCA.md](FLUXO-SEGURANCA.md).
