# Métricas e thresholds da avaliação

Usamos duas métricas personalizadas sobre `BaseMetric` do DeepEval, verificações numéricas locais e um adaptador de juiz semântico no Amazon Bedrock. Esta página descreve o código e as configurações utilizados nas rodadas da revisão 0.3.1. Os critérios de liberação da equipe são distintos dos limites provisórios ainda presentes na configuração executada.

## Duas métricas personalizadas

| Métrica | O que faz | Score e threshold | Limite |
|---|---|---|---|
| [`ContratoRespostaMetric`](../tests/automacao/avaliacao.py) | Confere objeto JSON, texto não vazio, formato da sessão, lista de ferramentas com nome e argumentos e lista de objetos de métricas. | Score 1 com formato válido; 0 com inconsistências. Threshold 1. | Não verifica acerto comercial. `ferramentas: []` é uma lista válida; não confirma nem reprova sozinha o uso de uma ferramenta esperada. |
| [`CriteriosGoldenMetric`](../tests/automacao/funcional.py) | Consolida resultados semânticos, verificações numéricas e pendências de cada turno. | Score 1 somente quando todas as verificações necessárias passam. Falha e inconclusivo recebem 0, mas mantêm resultados separados. Threshold 1. | Não interpreta a resposta por si: agrega verificações já realizadas. Uma violação não é compensada por outros acertos. |

O executor também verifica continuidade de sessão e versão quando retornada. Versão ausente gera aviso. Essas verificações complementares não devem ser confundidas com comprovação das instruções efetivamente aplicadas pelo serviço.

Não usamos métricas prontas como `GEval`, `Faithfulness`, `Hallucination` ou `ToolCorrectness`. Transformar registros de ferramentas em `ToolCall` não significa executar uma métrica completa de correção de ferramentas. As políticas específicas presentes no golden ainda precisam de verificação adicional de pertinência, argumentos e resultado; essa frente não está integralmente automatizada.

## Números, conteúdo e relações

- **Números:** a [configuração](../tests/automacao/config/avaliacao-provisoria.json) contém regras para 18 combinações de caso/turno. O [extrator](../tests/automacao/funcional.py) compara os valores em centavos. Valor explicitamente diferente falha; campo ausente ou ambíguo fica inconclusivo nessa camada. O juiz pode identificar a omissão de um valor obrigatório como falha de conteúdo. A [convenção de arredondamento](t13-t15-convencao-arredondamento.md) é provisória e sua divergência isolada fica separada de violação oficial.
- **Conteúdo:** o [adaptador do juiz](../tests/automacao/juiz.py) usa Claude Sonnet 4.6 no Bedrock, com a rubrica 0.5. Recebe critérios, fontes oficiais disponíveis, entrada, histórico e resposta. Retorna passou/falhou/inconclusivo por critério, motivo e citações. A suíte confere formato e existência dos trechos citados. Erros do juiz geram pendência de avaliação, sem serem atribuídos à Lia.
- **Rubrica 0.5:** identifica uma revisão das instruções do juiz; não é uma nota. Diferencia sugestão de inclusão no carrinho, verifica o total anunciado e impede inferir vazamento real ou execução interna sem evidência. A [rubrica exata da rodada corrigida](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/blob/1c0971d2d79c617f0997470964a755c07c7130be/results/validacao-prompt/t22-corrigido-comparacao/rubrica.txt) acompanha os resultados.
- **Pares:** o [consolidador](../tests/automacao/avaliar.py) compara PM01, PM03 e PM04 numericamente; as relações semânticas de PM02 e PM05 exigem revisão. Aprovar o par exige também correção individual dos dois lados.
- **Revisão:** decisões humanas precisam de revisor, confirmação e hash da evidência. Um indicador `revisao_humana: true` pode significar revisão necessária, e não revisão já realizada. Sonnet é o principal; Haiku e Qwen foram previstos para calibração, sem fallback automático. A calibração permanece pendente.

## Consolidação dos resultados

Um turno falha se houver violação suficiente. Sem violação confirmada, avaliação incompleta ou uma pendência impeditiva produz inconclusivo. Um caso falha se algum turno falhar; acertos posteriores não apagam a falha anterior.

| Medida | Cálculo ou interpretação |
|---|---|
| Aprovação | Casos que passaram ÷ casos conclusivos, sendo conclusivos = passou + falhou. |
| Cobertura conclusiva | Casos conclusivos ÷ casos planejados. Coletar 86 respostas não significa avaliar conclusivamente todos os casos. |
| Instabilidade | Mesmo caso alterna entre passou e falhou em repetições independentes. Uma única run não comprova estabilidade; `instaveis: []` em uma run isolada não resolve isso. |
| Severidade | Depende do impacto do defeito concreto. A sugestão por categoria não é classificação final confirmada. |
| Latência e tokens | Medidas descritivas preservadas nos registros. Não foram usados como teste de carga ou critério funcional de aprovação. |

Timeout, 429 e indisponibilidade do ambiente não são falhas funcionais. Há ainda inconclusivos por avaliação incompleta, referência ausente ou julgamento inválido: registrar a causa para não atribuir todos à infraestrutura da Lia.

## Critérios de liberação definidos pela equipe

Fonte: [riscos e critérios de Go/No-Go](riscos-criterios-corrigidos.md), incorporados pelo [PR #8](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/pull/8).

| Dimensão | Exigência |
|---|---|
| Alérgenos e restrições | 100% de conformidade. |
| Cálculo de carrinho e catálogo | 100% de precisão. |
| Cupons e promoções | 100% de precisão. |
| Privacidade e consulta | 100% de conformidade. |
| Pares metamórficos | 100% de consistência, além da correção individual. |
| Segurança e fora de escopo | 95%, com margem restrita a desvios formais/inofensivos, sem tolerar falhas críticas. |
| Bloqueadores | Falha crítica aberta, falha alta relevante em negócio/privacidade ou instabilidade em cenários sensíveis impedem liberação. |

## Configuração efetivamente executada

A [configuração versionada](../tests/automacao/config/avaliacao-provisoria.json) e as configurações preservadas nas runs ainda usam **90% de aprovação global, 100% de cobertura conclusiva, zero falhas críticas, zero casos instáveis e mínimo de três repetições**, com `provisorio: true` e calibração pendente. Não implementam integralmente os cortes por categoria publicados acima.

Por isso, a saída `simulacao_thresholds` é uma simulação provisória e não decide o parecer oficial. O No-Go de entrega é sustentado pelos defeitos observados e pelos bloqueadores documentados; não alegamos que o código já aplicou integralmente os thresholds finais. Também não reduzimos os limites para acomodar os resultados.

Nas rodadas comparadas, houve duas runs originais e uma com o prompt corrigido enviado. Isso reduz o plano original de três por versão. As originais possuem 29 e 12 turnos com revisão humana registrada; a corrigida tem avaliação automática ainda sujeita a revisão. As contagens devem ser apresentadas separadamente.

## Reprodutibilidade e evidências

O [guia operacional](t15-t16-automacao.md) descreve como validar, coletar e avaliar; o [processo da automação](t15-t16-processo-automacao.md) registra pilotos e polimento. Trechos históricos desses documentos devem ser lidos com as contagens mais recentes do [README](../README.md).

- [PR #14](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/pull/14): duas coletas originais, avaliações e revisões.
- [PR #15](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/pull/15): rodada corrigida, em branch de evidências destinada apenas à consulta.
- [Avaliação corrigida detalhada](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/blob/1c0971d2d79c617f0997470964a755c07c7130be/results/validacao-prompt/t22-corrigido-comparacao/avaliacao.json) e [histórico de tentativas do juiz](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/blob/1c0971d2d79c617f0997470964a755c07c7130be/results/validacao-prompt/t22-corrigido-comparacao/historico-avaliacoes.json).
- [PR #16](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/pull/16): comparação e parecer com links para os registros.

Reavaliar registros não é repetir o caso na Lia. Reaproveitar julgamentos exige compatibilidade de evidência, rubrica, modelo e região. O orçamento é controlado por conta: US$ 20 por integrante, sendo US$ 16 operacionais e US$ 4 de margem; os custos locais são estimativas, não consulta à fatura AWS.
