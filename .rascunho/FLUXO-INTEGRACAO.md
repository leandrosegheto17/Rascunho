# Fluxo de integração com terceiros

Conectar o sistema a uma API, pagamento ou serviço externo. O terceiro muda sem avisar, cai, limita o uso e cobra. A regra central: **tratar o serviço externo como um componente que vai falhar** e isolá-lo do resto do sistema. Cada fase termina com uma decisão (seguir, ajustar ou parar).

| # | Fase | Pergunta que responde | Como se responde | Decisão |
|---|---|---|---|---|
| 1 | **Necessidade** | Por que integrar e o que se espera obter? | Descrever o caso de uso, dados trocados, volume esperado | Integrar é o caminho certo? |
| 2 | **Escolha do serviço** | Qual fornecedor, e a que custo e risco? | Comparar opções: custo, limites, SLA, qualidade da documentação, termos, dependência do fornecedor, rota de saída | Fornecedor escolhido |
| 3 | **Contrato** | Como o serviço se comporta de fato? | Ler a documentação, testar em sandbox, mapear autenticação, erros, limites de taxa, paginação, versões e webhooks | Contrato entendido e testado? |
| 4 | **Segurança e legal** | Que dados saem e quem responde por eles? | Dados pessoais envolvidos, base legal (LGPD), onde ficam armazenados, gestão de chaves e segredos, escopo mínimo de permissões | Risco aceitável? |
| 5 | **Desenho** | Como isolar o terceiro do resto? | Camada própria (adaptador) atrás de uma interface, tratamento de falhas (tentar de novo, timeout, disjuntor), fila para chamadas não críticas, plano para o caso de o serviço sair do ar | Desenho aprovado |
| 6 | **Implementação** | Funciona contra o sandbox e contra falhas simuladas? | Testes com serviço simulado (mock), testes de contrato, casos de erro e de lentidão, idempotência | Passa nos testes, inclusive nas falhas |
| 7 | **Verificação** | Funciona de verdade e sem vazar nada? | Teste ponta a ponta no sandbox, revisão de segredos e de logs, checagem de limites de uso e de custo | Pronto para produção |
| 8 | **Liberação** | Como ligo sem risco? | Chaves de produção em cofre de segredos, feature flag, liberação gradual, plano de reversão | No ar e estável |
| 9 | **Monitoramento** | Percebo quando o terceiro falha ou muda? | Métricas de erro, latência e custo, alertas, acompanhamento do aviso de mudanças do fornecedor | Monitoramento ativo |

## Princípios

- **Interface própria entre o sistema e o terceiro.** Trocar de fornecedor vira mexer num só lugar.
- **Falha é o caso normal.** Timeout, nova tentativa e degradação elegante vêm no desenho e não depois do primeiro incidente.
- **Nunca confiar na entrada externa.** Validar o que o terceiro devolve e autenticar webhooks.
- **Custo é requisito.** Chamadas pagas precisam de limite e alerta.
- **Saída de emergência:** se o contrato real divergir muito da documentação ou o risco legal for alto, o fluxo volta à escolha do serviço.

Outros fluxos: [FLUXO-PROJETO-NOVO.md](FLUXO-PROJETO-NOVO.md), [FLUXO-FEATURE.md](FLUXO-FEATURE.md), [FLUXO-PERFORMANCE.md](FLUXO-PERFORMANCE.md).
