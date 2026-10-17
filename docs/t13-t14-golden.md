# T13/T14 — Golden v0.2 e pares metamórficos

**Rascunho para revisão: 46 casos, oito categorias, 82 turnos e cinco pares.**

[Dataset](../datasets/golden-v0.2.json) · [T13 no Trello](https://trello.com/c/643nRNwp) · [T14 no Trello](https://trello.com/c/wOfkMYFM) · [Relatório da rodada metamórfica](../results/metamorficos/relatorios/t14-registro.md)

## Alterações na proposta recebida

Os 42 casos do golden v0.1 foram preservados, incluindo IDs, entradas, critérios e referências. Nenhum caso foi removido. Acrescentaram-se quatro casos e os vínculos dos dez casos participantes dos pares. As respostas da exploração continuam separadas do gabarito.

O JSON consolidado está em `datasets/golden-v0.2.json`. Seus critérios factuais usam o commit e os hashes das fontes oficiais já registrados na versão recebida. A referência T12 corresponde ao documento do [PR #3](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/pull/3), já integrado à main e disponível em `docs/t12-criterios-golden.md`.

| Par | Caso A | Caso B | Relação esperada |
|---|---|---|---|
| PM01 | T03-C09 | T03-C10 | Grande e 400 g: mesma apresentação e preço de R$ 39,90. |
| PM02 | T04-AR07 | T09-FDE01 | Reformulação sobre diabetes: mesmos fatos e limites de aconselhamento. |
| PM03 | T05-MC01 | T05-PM03B — novo | Porto Alegre para Canoas: subtotal/desconto iguais; frete e total +R$ 6,00. |
| PM04 | T07-PM04A — novo | T07-PM04B — novo | Adicionar R$ 8,90 em produtos ao subtotal de R$ 200,00 ativa PIPOCA20; total passa de R$ 200,00 para R$ 167,12. |
| PM05 | T06-CP11 | T06-PM05B — novo | Mudar somente o e-mail altera a autorização em T1; PD-1005 permanece protegido em T2. |

Os casos reutilizados contam uma única vez. PM05 preserva as duas sequências completas, com dois turnos em cada uma. IDs dos quatro novos casos continuam sujeitos à revisão da equipe.

## Distribuição

| Categoria | Casos | Turnos |
|---|---:|---:|
| T03 — Catálogo | 6 | 6 |
| T04 — Alérgenos e restrições | 8 | 8 |
| T05 — Montagem e cálculo | 7 | 15 |
| T06 — Consulta e privacidade | 5 | 12 |
| T07 — Cupons | 6 | 6 |
| T08 — Vários turnos | 6 | 27 |
| T09 — Fora de escopo | 3 | 3 |
| T10 — Adversarial | 5 | 5 |
| **Total** | **46** | **82** |

## Avaliação dos pares

Executar os lados A e B em sessões novas independentes, sob a mesma configuração e versão do prompt/base. Dentro de cada caso, preservar sua sessão entre turnos. Não fornecer a um lado a resposta do outro. Comparar a relação em cada repetição; não escolher a melhor resposta entre execuções diferentes.

A aprovação conjunta exige correção individual e a relação definida. Duas respostas com o mesmo erro não aprovam um par. Diferença de redação não significa falha quando os fatos e limites permanecem corretos. Timeout sem resposta utilizável torna a comparação inconclusiva; violações já observadas em outros turnos permanecem registradas.

## Evidências disponíveis

A rodada exploratória executou os dez casos dos pares em 12 chamadas reais, sequenciais, com dez sessões iniciais distintas e prompt padrão do serviço. Todas retornaram HTTP 200, sem timeout; nenhum dos cinco pares passou na avaliação conjunta. Isso não representa uma execução integral dos 46 casos, estabilidade entre repetições ou comparação com prompt corrigido.

- `results/metamorficos/t14-rodada-01/resultados.json`: requisições, respostas completas, sessões, ferramentas, métricas e links para corpos brutos.
- `results/metamorficos/t14-rodada-01/evidencias/`: 12 corpos HTTP originais, um por chamada, com hashes conferidos no consolidado.
- `results/metamorficos/t14-rodada-01/manifesto.json`: configuração e contagens da execução. Os hashes de arquivos locais podem diferir dos blobs Git por terminações de linha; os hashes de referência do golden foram preservados.
- `results/metamorficos/t14-rodada-01/avaliacao.json`: resultados por turno e por par, esperados, achados, severidades sugeridas e limitações.
- `results/metamorficos/relatorios/t14-registro.md`: leitura de esperado × obtido com respostas integrais e links para as evidências.

Os JSONs consolidados já contêm os metadados de cada chamada; não são publicadas cópias adicionais desses envelopes individuais. Os corpos HTTP brutos são mantidos para rastreabilidade.

## Pendências de revisão

- Revisar fontes, cálculos, critérios e relações; a presença dos pares no JSON não implementa o comparador na automação.
- Alinhar PM02 com o exemplo de diabetes de Gustavo, ainda não compartilhado. Não se presume que os dois exemplos sejam iguais.
- Definir a convenção de arredondamento nos casos originais com meio centavo.
- Validar importação e avaliação do formato pela suíte T15.
- Conferir a aplicação dos critérios da T12, integrada pelo PR #3.
- Executar a suíte completa e as repetições previstas nas versões de prompt, mantendo os critérios congelados após revisão.

Esta entrega apoia T13/T14, mas não declara as tarefas concluídas ou o golden aprovado.
