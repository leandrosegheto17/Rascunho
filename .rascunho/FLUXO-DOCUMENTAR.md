# Fluxo de documentação de projeto existente

O projeto roda, mas ninguém sabe explicá-lo por escrito, nem a IA que vai trabalhar nele. A regra central: **documentar o que o código faz de fato, verificado no código e em execução, e não o que se acha que ele faz**. Cada fase termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Objetivo e público** | Para quem documentar e para quê? | Definir leitores (você, novo dev, IA, cliente) e usos (onboarding, manutenção, auditoria, contexto para agentes) | Público e profundidade definidos |
| 2 | **Inventário** | O que existe? | Mapear estrutura de pastas, linguagens, dependências, scripts, pipelines, ambientes, e documentos já existentes (alguns desatualizados) | Mapa geral pronto |
| 3 | **Execução** | Roda? Como? | Instalar do zero seguindo só o que está escrito, rodar testes e a aplicação. Anotar cada tropeço, pois ele vira instrução. | Ambiente reproduzível |
| 4 | **Arquitetura** | Como as partes se encaixam? | Módulos, camadas, fluxo de dados, integrações externas, banco, autenticação. Diagrama simples e fiel ao código. | Visão estrutural validada |
| 5 | **Comportamento** | O que o sistema faz para o usuário? | Principais fluxos de ponta a ponta, regras de negócio importantes, estados, erros. Confirmar rodando, não só lendo. | Fluxos principais descritos |
| 6 | **Convenções** | Como o código é escrito aqui? | Nomes, organização, padrões repetidos, estilo de testes, tratamento de erros, e as inconsistências | Convenções registradas |
| 7 | **Riscos e dívidas** | Onde está o perigo? | Áreas frágeis, sem testes, segredos expostos, dependências desatualizadas, partes mortas, armadilhas | Riscos listados |
| 8 | **Contexto para IA** | O que um agente precisa saber ao abrir o projeto? | Arquivo de instruções do projeto: como rodar, testar e publicar, estrutura, convenções, o que não mexer. Curto e direto. | Arquivo de contexto pronto |
| 9 | **Validação e manutenção** | Está correto e vai continuar? | Pedir a alguém (ou a uma sessão nova de IA) para seguir a documentação e registrar onde falha. Definir quando revisar. | Documentação validada |

## Princípios

- **Verificar, não presumir.** Documento que descreve o que o código "deveria" fazer engana.
- **Seguir o próprio guia do zero** é o melhor teste de qualidade.
- **Curto e específico vence completo e genérico.** Quem lê quer achar a resposta rápido.
- **Registrar o porquê quando for descoberto.** O quê o código mostra, o porquê se perde.
- **Nada de segredo na documentação.** Referenciar onde ficam, sem copiar valores.
- **Documentação viva.** Ficar junto do código, no repositório, e ser atualizada na mesma mudança que a torna falsa.
- **Este fluxo costuma ser o pré-requisito** de [FLUXO-FEATURE.md](FLUXO-FEATURE.md) e [FLUXO-FEATURE-LEGADO.md](FLUXO-FEATURE-LEGADO.md) quando o projeto não tem contexto.

Outros fluxos: [FLUXO-REFATORACAO.md](FLUXO-REFATORACAO.md), [FLUXO-AVALIACAO-TERCEIROS.md](FLUXO-AVALIACAO-TERCEIROS.md).
