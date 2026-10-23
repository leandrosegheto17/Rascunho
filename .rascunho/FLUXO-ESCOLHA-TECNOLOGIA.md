# Fluxo de escolha de tecnologia

Decidir stack, banco de dados, framework, fornecedor ou construir versus comprar. A regra central: **decidir por critérios explícitos e registrar o porquê**, porque a decisão será questionada depois e quem decidiu pode não estar lá. Cada fase termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Decisão a tomar** | O que exatamente estou escolhendo e por quê? | Descrever o problema e o que a escolha afeta. Separar decisões difíceis de reverter (banco, linguagem principal) das fáceis (biblioteca de datas). | Decisão delimitada? |
| 2 | **Critérios** | O que importa nessa escolha? | Listar requisitos obrigatórios (eliminatórios) e desejáveis, com pesos: custo, curva de aprendizado, desempenho, maturidade, comunidade, segurança, licença, hospedagem, equipe | Critérios definidos antes de olhar as opções |
| 3 | **Opções** | Quais são as alternativas reais? | Levantar de 3 a 5, incluindo "não fazer nada" e "construir sozinho". Buscar em fontes confiáveis, não só na moda. | Lista curta |
| 4 | **Eliminação** | Quais não servem? | Descartar as que falham em requisito obrigatório: licença incompatível, projeto abandonado, fora do orçamento | Finalistas (2 ou 3) |
| 5 | **Avaliação** | Como cada uma se sai? | Comparar por critério, com evidência: documentação, atividade do projeto, vulnerabilidades conhecidas, casos de uso reais, limites do plano gratuito, custo ao longo do tempo | Tabela comparativa |
| 6 | **Teste prático** | Funciona no meu caso? | Spike curto com cada finalista nos pontos de maior incerteza ([FLUXO-SPIKE.md](FLUXO-SPIKE.md)) | Evidência de campo |
| 7 | **Riscos e saída** | E se der errado? | Dependência do fornecedor, custo de migrar depois, o que acontece se o projeto morrer, plano B | Risco de reverter aceitável? |
| 8 | **Decisão** | Qual escolho? | Escolher, com a justificativa em poucas linhas. Se ficou empatado, preferir a mais simples e a mais reversível. | Decisão tomada |
| 9 | **Registro (ADR)** | Como o futuro entende essa escolha? | Registro curto: contexto, opções, decisão, consequências, e quando revisar. Salvar no repositório. | Decisão registrada |

## Princípios

- **Critérios antes de opções.** Do contrário se escolhe a favorita e se montam critérios para ela.
- **Tecnologia chata costuma ganhar.** Madura, conhecida e bem documentada reduz risco.
- **Reversibilidade pesa.** Quanto mais difícil de desfazer, mais cuidado.
- **Custo total, não preço de entrada.** Contar manutenção, aprendizado e custo de sair.
- **Testar nas partes incertas**, não em tudo.
- **Evitar a moda.** Novidade tem custo de maturidade que alguém paga.
- **Construir versus comprar:** construir só o que diferencia o produto, e comprar o que é comum.

Outros fluxos: [FLUXO-SPIKE.md](FLUXO-SPIKE.md), [FLUXO-AVALIACAO-TERCEIROS.md](FLUXO-AVALIACAO-TERCEIROS.md), [FLUXO-PROJETO-NOVO.md](FLUXO-PROJETO-NOVO.md).
