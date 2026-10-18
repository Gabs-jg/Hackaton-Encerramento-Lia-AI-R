# T15/T16 — Execução e avaliação do golden

Base de automação para [T15](https://trello.com/c/Txolh6Zd) e [T16](https://trello.com/c/1css3mkO), usando o golden v0.2 do [PR #10](https://github.com/Gabs-jg/Hackaton-Encerramento-Lia-AI-R/pull/10). O golden e os critérios de Go/No-Go continuam pendentes de aprovação. Esta implementação depende da integração desse PR; não altera os casos da T13/T14.

O DeepEval registra a verificação técnica e os critérios funcionais por turno. A avaliação considera o histórico da conversa, mas usa exclusivamente o golden e os trechos oficiais como referência. O promptfoo permanece na frente de red team de Gustavo.

Expliquei as decisões, os pilotos e o polimento em [como organizei a automação e o avaliador](t15-t16-processo-automacao.md). Reuni os blocos candidatos para o agente em [propostas de correção do prompt](t15-t16-sugestoes-prompt.md).

## Fluxo

1. **Validar:** conferir o formato, IDs, pares, referências e hashes do golden, sem chamadas.
2. **Executar:** enviar as entradas à Lia e preservar as respostas completas em uma pasta nova.
3. **Avaliar:** ler essa pasta com regras numéricas, juiz e/ou revisão humana.
4. **Reavaliar:** mudar thresholds ou completar revisões e gerar outra avaliação da mesma coleta.

Reavaliar não chama a Lia novamente. Com `--juiz bedrock`, a reavaliação pode chamar o juiz e gerar custo; o modo padrão usa somente verificações locais e revisão humana. Para mudar thresholds sem repetir o juiz, usar `--juiz salvo --julgamentos CAMINHO_DO_ARQUIVO`. A reutilização exige a mesma evidência, rubrica, modelo e região; mantém a origem de modelo e as revisões humanas pendentes. Uma evidência sem julgamento compatível fica inconclusiva na avaliação semântica.

## O que está preparado

| Parte | Comportamento |
|---|---|
| Golden | Importa 48 casos, 86 turnos e 112 critérios (revisão 0.3.1) sem mudar suas entradas; mantém o piloto antigo compatível. |
| Fontes | Confere hashes de arquivos oficiais e T12, aceitando a diferença de fim de linha Windows/Linux. Extrai as seções citadas; identifica referências do enunciado que não estão disponíveis localmente. |
| Sessões | Uma sessão nova por caso/repetição; preservada entre os turnos do caso. |
| Versões | Original sem `prompt_sistema`; corrigida exige arquivo e envia o prompt em todos os turnos. |
| Evidências | Registra resposta completa, sessão, versão retornada quando disponível, ferramentas, todos os itens de métricas, tentativas e hashes. |
| Transporte | Timeout/429/5xx são inconclusivos de ambiente. Retry opcional apenas para 429; nunca para substituir resposta funcional reprovada. |
| Avaliação numérica | Comparação em centavos em 18 turnos com valores explícitos; regras adicionais ficam em configuração separada do golden. |
| Avaliação semântica | Rubrica para todos os critérios, com trecho da resposta e justificativa; integração Bedrock ou revisão humana vinculada à evidência. |
| Metamórficos | Confere resultados individuais e relação. PM01/03/04 têm comparação numérica; PM02/05 possuem revisão da relação semântica. |
| Resultados | JSON, Markdown, fila de revisão, numerador/denominador, cobertura e instabilidade. Inconclusivos ficam visíveis. |

O extrator de números é conservador: reconhece campos como `Subtotal: R$ 64,80`, `Frete: grátis` e `Total: R$ 73,56`. Um número isolado no texto não aprova o caso. Redação não reconhecida ou valores contraditórios geram inconclusivo para extração, permitindo revisão. O resultado numérico não substitui a avaliação de todas as regras comerciais. Falhas detectadas também entram para conferência humana.

Se um turno válido falhar e um turno seguinte tiver timeout, a falha anterior é preservada. Em repetições, a combinação de passou/falhou indica instabilidade; nunca se escolhe somente a melhor resposta.

## Preparação

Na raiz desta branch, usando Python 3.12:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-t15.txt
python -m tests.automacao.executar --dataset datasets/golden-v0.3.json --validar --repeticoes 3
```

O plano completo atual tem **258 chamadas por versão**, ou **516 nas duas versões**, antes de retentativas. A validação não envia nenhuma delas. A execução é sequencial; combinar janelas com a squad para manter o limite global de quatro chamadas. Este processo não controla os computadores dos outros integrantes e não realiza carga.

## Demonstração sem custo

```powershell
python -m tests.automacao.executar --dataset datasets/golden-v0.2.json --modo replay --pares --replay-resultados results/metamorficos/t14-rodada-01/resultados.json --fase-base historica_nao_confirmada
```

O terminal informa a pasta criada. Copiar esse caminho para avaliar:

```powershell
python -m tests.automacao.avaliar CAMINHO_DA_EXECUCAO --config tests/automacao/config/avaliacao-golden-v0.2.json
```

O replay dos dez casos/12 turnos reutiliza evidências históricas. Não comprova estabilidade, latência atual nem efeito de prompt corrigido. Replay só aceita versão original e uma leitura.

No teste local desta estrutura, os verificadores numéricos sinalizaram seis casos como falhou e quatro como inconclusivo. Os quatro restantes exigem avaliação semântica; isso não contradiz a análise humana anterior dos pares. Nenhum caso foi automaticamente aprovado.

## Chamadas reais à Lia

Configurar `LIA_API_KEY` no ambiente ou no `.env` ignorado pelo Git. Começar selecionando poucos casos:

```powershell
python -m tests.automacao.executar --dataset datasets/golden-v0.3.json --modo api --caso T05-MC01 --caso T06-CP11 --fase-base nao_confirmada
```

Versão corrigida, quando o prompt dessa frente estiver disponível:

```powershell
python -m tests.automacao.executar --dataset datasets/golden-v0.3.json --modo api --caso T05-MC01 --versao corrigida --prompt CAMINHO_DO_PROMPT --fase-base nao_confirmada
```

O [prompt técnico do piloto](../tests/automacao/fixtures/prompt-integracao.txt) serve apenas para testar o envio do campo; não é a correção oficial. A API sem `versao` gera aviso, não confirmação inventada. A fase da base é declaração da equipe.

## Juiz AWS e orçamento

O piloto utiliza `us.anthropic.claude-sonnet-4-6` em `us-east-2`. **O acesso foi confirmado por duas chamadas bem-sucedidas no lote 02**, após o envio e a propagação do formulário Anthropic. Antes da liberação, houve erros `ResourceNotFoundException`; seus registros e reservas de orçamento foram preservados. A configuração local ignorada pelo Git contém esse ID e região. A presença do perfil no catálogo, isoladamente, não comprova que a invocação funciona.

Conforme o [DIS-06](https://trello.com/c/rNIi1TWF) e o alinhamento de implementação: **Claude Sonnet 4.6 principal; Haiku 4.5 e Qwen como alternativas na calibração**. O ID/perfil de inferência e a região devem corresponder ao acesso disponível na conta; não há fallback automático para outro modelo.

```powershell
aws sso login --profile academy
$env:AWS_PROFILE = "academy"
python -m pip install -r requirements-juiz.txt
if (-not (Test-Path avaliacao.local.json)) {
    Copy-Item tests/automacao/config/avaliacao-provisoria.json avaliacao.local.json
}
```

Editar somente a seção `juiz` de `avaliacao.local.json`:

- `model_id` e `region`: modelo/perfil de inferência e região verificados na própria conta. Também podem vir de `LIA_JUDGE_MODEL_ID` e `AWS_REGION`.
- `usd_por_milhao_entrada` e `usd_por_milhao_saida`: preços vigentes para o modelo, região/modalidade. Permanecem vazios até conferência; não são valores presumidos.
- `gasto_externo_usd`: gasto anterior da conta que NÃO está no registro local desta automação, incluindo red team/outros projetos. Conferir antes de cada lote para evitar dupla contagem ou omissão.
- `conta_orcamento` e `arquivo_orcamento`: identificar a própria conta e manter o mesmo arquivo entre rodadas. Não compartilhar o saldo de outra pessoa nem reiniciar o arquivo para liberar chamadas.
- `limite_usd` e `max_chamadas`: limites desta execução. Padrão **US$ 1** e **três chamadas** para piloto.
- `lote_id`, `limite_usd_lote` e `max_chamadas_lote`: limites persistentes do mesmo lote, acumulados mesmo ao reiniciar o processo. O lote 01 tinha três tentativas/US$ 1; o lote 02, autorizado separadamente, tinha três tentativas/US$ 0,25. Ambos encerraram nas três tentativas; não alterar o identificador para contornar o limite. Um lote seguinte precisa de orçamento e quantidade definidos antes de executar.
- `casos_piloto` (opcional): IDs que podem chegar ao juiz neste piloto. Os demais continuam disponíveis para avaliação local e revisão.

```powershell
python -m tests.automacao.avaliar CAMINHO_DA_EXECUCAO --config avaliacao.local.json --juiz bedrock
```

O registro local acumula reservas/custos estimados entre execuções. Antes de cada chamada, verifica **registro acumulado + gasto externo informado + reserva ≤ US$ 16**. Os **US$ 4 restantes** são margem, não verba de execução. Erros sem uso conhecido mantêm a reserva; ausência de métricas de consumo interrompe novas chamadas. Há bloqueio local para evitar duas escritas simultâneas no saldo.

Os valores são estimativas com os preços configurados, não uma consulta à fatura nem garantia de limite de cobrança AWS. A conta precisa ser acompanhada também no serviço. Gastos feitos em outro computador ou por outras ferramentas precisam ser conciliados em `gasto_externo_usd`. As quatro contas não formam um único saldo transferível.

O juiz recebe critérios, referências oficiais e histórico como dados. Pedidos de “ignore as regras” contidos nas respostas não são instruções para o juiz. A saída exige JSON válido, todos os critérios, motivos e citações existentes na resposta. Isso reduz erros de julgamento, mas não elimina a necessidade de calibração e revisão de segurança/ambiguidades. Erro ou truncamento do juiz não vira defeito da Lia.

O piloto usou respostas históricas: **nenhuma chamada nova à Lia**. No lote 01, o julgamento de T03-C09 confirmou a divergência entre R$ 28,90 retornados e R$ 39,90 da referência oficial. O JSON veio delimitado por Markdown e foi recuperado localmente após ajustar o leitor, sem repetir a chamada. As duas outras tentativas desse lote não produziram julgamentos. No lote 02, houve uma falha durante a propagação do cadastro e dois julgamentos válidos, de T04-AR07 e T05-MC01.

Nos dois lotes, o consumo retornado corresponde a **US$ 0,0239844 estimados**. As três tentativas sem consumo conhecido mantêm **US$ 0,1138665 de reserva**, que não comprova cobrança. O registro total é **US$ 0,1378509**, deixando **US$ 15,8621491** do teto operacional, considerando o gasto externo informado de zero. A fatura AWS não foi consultada. O preço usado foi US$ 3,30/16,50 por milhão de tokens de entrada/saída para a modalidade geográfica, conforme a [tabela oficial da Anthropic](https://www-cdn.anthropic.com/files/4zrzovbb/website/3684c2faafb97418665782cea0001f439f74b1d2.pdf); conferir a tabela vigente antes de outro lote.

A avaliação de T05-MC01 identificou cálculos incorretos, mas também confundiu sugestão comercial com inclusão de item no pedido em sua justificativa. Esse achado iniciou o polimento documentado da rubrica, atualmente na versão **0.5**. Os pareceres antigos permanecem preservados, mas não são compatíveis com a nova rubrica para reutilização automática. A nova versão distingue oferta, inclusão, total final, omissão, autorização, observabilidade e regras indefinidas; a calibração humana continua pendente.

Os valores do parágrafo anterior descrevem somente os dois pilotos de acesso. O saldo corrente também inclui os testes posteriores da rubrica e deve ser consultado no registro local antes de qualquer lote. Não usar os valores históricos deste guia como saldo atualizado.

Para regularizar o acesso, selecionar o modelo Anthropic no catálogo do Amazon Bedrock e preencher **Submit use case details**, conforme a [documentação AWS](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html). Não é necessário recriar as credenciais SSO para corrigir esse formulário.

## Configuração e revisão

[avaliacao-provisoria.json](../tests/automacao/config/avaliacao-provisoria.json) concentra as regras numéricas, severidades sugeridas e os thresholds. Os valores **90% de aprovação, 100% de cobertura conclusiva, zero falhas críticas, zero casos instáveis e três repetições** servem somente para exercitar a estrutura. Não representam decisão da T11 nem aprovação do PR de thresholds.

Regras individuais usam cumprimento integral do critério, não uma média que compensa violação com acertos. Alterar o limite global não afrouxa os valores oficiais de preço, privacidade ou alérgenos.

Cada avaliação cria `revisao-template.json`. Manter somente as entradas que foram efetivamente revisadas, preencher revisor, motivos, resultados, trechos literais e `confirmado: true`. Preservar os hashes; uma revisão de outra resposta é rejeitada. Ao confirmar um turno, conferir também os achados numéricos, referências ausentes e ressalvas. Critérios ainda não definidos podem continuar inconclusivos.

```powershell
python -m tests.automacao.avaliar CAMINHO_DA_EXECUCAO --config avaliacao.local.json --revisao CAMINHO_DA_REVISAO
```

Para reaplicar o julgamento do modelo sem outra chamada paga:

```powershell
python -m tests.automacao.avaliar CAMINHO_DA_EXECUCAO --config avaliacao.local.json --juiz salvo --julgamentos CAMINHO_DA_AVALIACAO/julgamentos.json
```

Esse comando também aceita `--revisao` para aplicar revisões humanas confirmadas. Uma alteração na rubrica ou na evidência impede reutilizar pareceres antigos. Os valores de consumo dentro do julgamento são da chamada original; o resumo da nova avaliação registra zero chamadas e zero custo novo.

Para continuar uma avaliação parcial, é possível combinar os julgamentos salvos com o Bedrock:

```powershell
python -m tests.automacao.avaliar CAMINHO_DA_EXECUCAO --config avaliacao.local.json --juiz bedrock --julgamentos CAMINHO_DOS_JULGAMENTOS_SALVOS
```

Somente evidências sem registro chegam ao modelo. Manter o mesmo `lote_id` e o mesmo arquivo de orçamento preserva o teto acumulado. O cache pode guardar `erro_julgamento` para preservar uma tentativa inválida sem repeti-la; isso não cria uma aprovação nem uma revisão humana.

Por padrão, uma saída inválida interrompe o juiz. A opção local `continuar_apos_formato_invalido: true` permite avaliar outros turnos quando a resposta chegou completa e o consumo foi contabilizado, mantendo aquele julgamento inválido. Erros de acesso, truncamento e consumo desconhecido continuam interrompendo as chamadas. Esta opção não aumenta os limites nem faz retentativas.

A validação de citações aceita equivalência de negrito Markdown, código em linha e espaços. Palavras, números, acentos e negações continuam obrigatórios; cada citação recebe a indicação de comparação literal ou por formatação.

Os arquivos antigos ficam preservados; cada reavaliação ganha uma pasta nova. Um par só passa quando os casos individuais e a relação passam. Duas respostas igualmente erradas não aprovam o par. PM02/PM05 ainda precisam da revisão da relação no campo `pares`.

## Organização das saídas

Para entender o código, começo pelos arquivos abaixo. Cada arquivo Python também tem uma explicação no início.

| Arquivo em `tests/automacao/` | Para que serve |
|---|---|
| `casos.py` / `golden.py` | Carregar o dataset, validar suas fontes e adaptar os turnos. |
| `executar.py` | Organizar casos, sessões, repetições e gravação após cada tentativa. |
| `cliente.py` | Enviar a requisição HTTP ou reler evidências históricas. |
| `avaliacao.py` | Conferir o contrato técnico e representar o teste no DeepEval. |
| `registros.py` | Gravar os JSONs e o resumo da coleta. |
| `funcional.py` | Comparar números, validar julgamentos e decidir o resultado por turno. |
| `avaliar.py` | Consolidar casos e pares, aplicar revisões e gerar o relatório. |
| `juiz.py` | Definir a rubrica e conversar com o modelo no Bedrock. |
| `julgamentos.py` | Reutilizar avaliações salvas e combinar cache com novas chamadas. |
| `orcamento.py` | Preservar reservas e limites entre processos. |
| `calibrar.py` | Comparar o juiz com exemplos e rótulos propostos. |
| `test_executor.py` / `test_golden.py` | Verificar o funcionamento local, sem chamadas pagas. |
| `config/avaliacao-provisoria.json` | Valores esperados, thresholds e limites do juiz. |
| `fixtures/` | Exemplos controlados para verificar a automação e a rubrica. |

```text
results/automacao/<execucao>/
├── dataset.json                 # snapshot adaptado para a execução
├── manifesto.json               # hashes, versão, modo, repetições e fase da base
├── resumo.json / resumo.md      # integração técnica
├── <caso>/r01/t01-a01.json       # cada tentativa com dados completos
└── avaliacoes/<avaliacao>/
    ├── config.json
    ├── rubrica.txt               # instrução exata usada nesta avaliação
    ├── avaliacao.json / resumo.md
    ├── turnos-parciais.json
    ├── julgamentos.json         # pareceres válidos do modelo, reutilizáveis
    ├── revisao-template.json
    ├── revisao-aplicada.json     # quando fornecida
    └── juiz-parcial.json         # quando Bedrock estiver ativo
```

As saídas são ignoradas pelo Git até seleção/revisão. Logs não registram o cabeçalho da chave da Lia; eventuais reflexões da chave são removidas na coleta.

## Limites e próximos ajustes

- O acesso AWS foi regularizado. Após os pilotos e o polimento, a primeira coleta integral e suas 82 tentativas de avaliação foram concluídas. O [histórico do processo](t15-t16-processo-automacao.md) registra os números e as pendências; não repetir o lote apenas para recuperar saídas inválidas.
- Submeter exemplos corretos/incorretos e a rubrica à revisão da equipe. Testes de código com respostas controladas não equivalem a calibração humana do juiz.
- Resolver a convenção de arredondamento e a referência temporal dos casos. `data_referencia` chega ao avaliador, mas não altera o relógio da API. O manifesto registra essa limitação; nenhuma mensagem é acrescentada silenciosamente ao golden.
- Aprovar o golden e os thresholds. O resumo sempre mantém o parecer oficial pendente; ele não substitui o parecer da equipe.
- T17 continua separada: esta base captura ferramentas/argumentos e oferece os dados à rubrica, mas não implementa o contrato específico de cada ferramenta. Não conclui ausência de chamada interna a partir de `[]`.
- Na API atual, a comprovação de uma chamada de ferramenta observável e a confirmação de versão retornada continuam pendentes, conforme o piloto anterior.
- Os dois pilotos de acesso usaram somente respostas históricas. Os testes controlados posteriores e as novas coletas do golden possuem pastas separadas; não misturar esses resultados nem contabilizar exemplos sintéticos como respostas da Lia.

## Conferência controlada do juiz

Validar os exemplos propostos sem gastar:

```powershell
python -m tests.automacao.calibrar --exemplos tests/automacao/fixtures/calibracao-juiz-proposta.json
```

Para chamar Bedrock, é necessário informar `--bedrock --config CAMINHO_DA_CONFIG_LOCAL` com modelo, preços, seleção e limites de um lote previamente planejado. O comando interrompe o lote quando encontra erro de contrato ou acesso, preservando os retornos. Cada saída inclui rubrica, exemplos, rótulos propostos, julgamento recebido, divergências e custo. Concordância com esses rótulos não marca `calibracao_aprovada` automaticamente.

## Verificação local

**68 testes locais passaram**, incluindo 246 chamadas simuladas para três repetições dos 82 turnos, preservação de sessões/prompt, erro de ambiente, comparação de pares, citações do juiz, reutilização de julgamentos, desconto com sinal negativo, revisão pendente e limite persistente de chamadas/orçamento. As dependências também passaram em `pip check`.

```powershell
python -m unittest tests.automacao.test_executor tests.automacao.test_golden -v
python -m pip check
```

Referências técnicas: [métricas personalizadas DeepEval](https://deepeval.com/docs/metrics-custom), [LLMTestCase](https://deepeval.com/docs/evaluation-test-cases), [AWS Bedrock Converse](https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-runtime/client/converse.html). A implementação usa `BaseMetric.measure()` local e os próprios registros, sem publicar execuções no Confident AI.

## Integração do golden atualizado

A revisão 0.3.1 deriva do golden 0.3.0 enviado pelo Gabriel. Adiciona a convenção provisória de arredondamento e separa o critério correspondente no ramo Pix de MT04. São 48 casos, 86 turnos, 112 critérios e cinco pares. PM02 agora usa T04-PM02A/B, com dois turnos por caso. Os dois casos do PM02 anterior continuam no golden, sem aquele vínculo.

O executor usa `datasets/golden-v0.3.json` por padrão. A configuração padrão corresponde ao hash dessa revisão; suas 18 regras numéricas anteriores e os thresholds não mudaram. A configuração histórica `avaliacao-golden-v0.2.json` continua disponível para avaliar coletas antigas. Não basta trocar o hash de uma configuração local: copiar a estrutura atual e transferir apenas os dados já conferidos da seção `juiz`, preservando o arquivo de orçamento existente. Não sobrescrever credenciais nem reiniciar o saldo.

O resultado da convenção aparece em `resultado_convencao` e `convencao_equipe` nos JSONs da avaliação. A divergência isolada fica inconclusiva no resultado funcional e pede justificativa humana, sem ser contada automaticamente como violação oficial. Não há tolerância geral de um centavo. A consulta ao orientador continua pendente.

Respostas HTTP 200 com texto utilizável podem ser avaliadas mesmo com contrato técnico incompleto. As falhas de conteúdo permanecem visíveis; um conteúdo correto não aprova o contrato incompleto. Timeout, ausência de texto e divergências de sessão/versão não são recuperados dessa forma. O executor continua interrompendo a sequência em erro de contrato, sem inventar continuidade nem ferramentas.

Verificação desta integração: **76 testes locais passaram**, incluindo oito novos testes de contagens, PM02, compatibilidade do hash, cálculos, classificação da convenção e texto com contrato incompleto. São testes simulados, não uma nova execução da Lia.

A primeira run permanece como resultado da **v0.2: 46 casos e 82 turnos**. Seus arquivos não foram reescritos e não cobrem o PM02 novo. Após revisão do golden, serão necessárias novas rodadas da mesma versão contra os dois prompts; planejar o custo antes das 258 chamadas por versão. Não houve consumo de API ou AWS nesta atualização.
