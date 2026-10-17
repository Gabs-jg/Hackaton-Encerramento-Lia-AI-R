# Como organizei a automação e o avaliador

## De onde parti

Comecei a automação antes da aprovação final do golden para adiantar a integração com a Lia e entender como registrar os testes. Usei um piloto pequeno para conferir requisições, sessões e o envio do prompt. Depois adaptei essa estrutura ao golden v0.2: 46 casos, oito categorias, 82 turnos, 99 critérios e cinco pares metamórficos.

Mantive as entradas e expectativas do golden. A resposta da Lia é o objeto da avaliação; o resultado esperado vem dos critérios e dos materiais oficiais. Essa separação é importante porque a base do agente pode divergir propositalmente da referência usada no desafio.

Minha implementação está nas T15/T16. Mantive as sugestões de prompt como propostas para discussão e não alterei o trabalho de red team ou os documentos das outras frentes.

## Por que separei coletar, avaliar e revisar

Organizei o fluxo em quatro passos:

1. **Validar o golden:** confiro IDs, categorias, ordem dos turnos, pares e referências. Também verifico se os arquivos oficiais correspondem à versão usada para montar as expectativas.
2. **Coletar:** envio as mensagens à Lia, preservando uma sessão por conversa e iniciando outra sessão para cada caso ou repetição. Salvo cada resposta antes de continuar.
3. **Avaliar:** leio o que já foi salvo, aplico verificações numéricas e, quando habilitado, envio os critérios e a resposta ao juiz.
4. **Revisar:** mantenho uma fila de conferência humana, com justificativas e links para as evidências. Posso reaplicar uma revisão ou mudar thresholds sem consultar a Lia outra vez.

Assim, uma mudança no critério de aprovação não exige repetir todas as conversas. Se a rubrica do juiz também permanecer igual, posso reaproveitar os julgamentos salvos. Se mudar a rubrica, a evidência, o modelo ou a região, o sistema não trata um parecer antigo como se fosse uma avaliação nova.

## Como usei o DeepEval

Usei o DeepEval para representar os casos e executar métricas personalizadas. Uma métrica confere o contrato da resposta; outra organiza os resultados funcionais. Não tratei HTTP 200 como aprovação de conteúdo.

As regras numéricas fazem comparações em centavos nos campos configurados. A avaliação semântica usa Claude Sonnet 4.6 pelo Bedrock. Os resultados ficam nos arquivos locais do projeto; não publiquei as execuções no serviço Confident AI.

O DeepEval não descobre sozinho as regras da loja. Fui explícita sobre os critérios, as fontes, o que conta como falha e o que exige revisão. Um resultado inconclusivo continua visível e não entra como aprovação nem como defeito da Lia.

## O que preservei em cada execução

Salvei a entrada enviada, resposta completa, sessão, ferramentas observadas, métricas retornadas, versão solicitada, horários, referências e identificação do caso/turno. O registro também guarda a versão do golden e identificadores de integridade dos arquivos e do código.

Não registrei a chave no cabeçalho das evidências. Os arquivos de configuração local e as saídas de execução ficam ignorados pelo Git até uma seleção consciente do que será compartilhado.

Mantive o envio sequencial, sem teste de carga. Timeout, falha de conexão e erros do serviço ficam separados de erros de conteúdo. Se um turno não termina de forma utilizável, não envio o seguinte sem contexto. A configuração padrão não faz retentativas; existe uma opção limitada para 429.

## O que os pilotos me mostraram

O primeiro acesso ao Sonnet produziu um julgamento válido, mas ele veio dentro de um bloco Markdown. Ajustei o leitor para aceitar um bloco JSON completo, preservando a rejeição de texto extra e de campos duplicados. Recuperei a resposta já recebida sem pagar por outra chamada.

Depois apareceram erros de acesso da AWS. Guardei o retorno e mantive a reserva de orçamento porque não havia métricas de consumo. Após o envio e a propagação do formulário Anthropic, confirmei a liberação por chamadas bem-sucedidas.

No piloto seguinte, o juiz identificou problemas nas respostas de T04-AR07 e T05-MC01. Entretanto, em T05-MC01 ele também tratou uma sugestão de balas como se fosse inclusão de um produto pago. A reprovação pelos cálculos continuava sustentada, mas a justificativa acrescentava uma violação não demonstrada. Esse foi o ponto de partida para o polimento da rubrica.

## Como refinei o juiz

Passei a exigir uma distinção clara entre oferecer um produto, pedir confirmação e afirmar que ele foi incluído no pedido. Também refinei outros pontos que poderiam produzir julgamentos imprecisos:

| Situação | Como tratei na avaliação |
|---|---|
| Conta correta com oferta opcional | A oferta, sozinha, não comprova inclusão nem cobrança. |
| Componentes corretos, total final errado | O total anunciado continua errado; o juiz não pode substituí-lo por uma conta que ele próprio fez. |
| Desconto apresentado com sinal negativo | Reconheço a representação de subtração, sem transformar um desconto correto em erro. Isso não muda o sinal de um total negativo. |
| Resposta genérica | Não aprovo uma consulta que exigia dados ou uma recusa/orientação explícita. |
| Critério exclusivamente de não divulgação | Posso reconhecer ausência de dados no texto sem afirmar que houve autorização ou consulta interna. |
| Consulta com dados corretos e nenhuma ferramenta registrada | Separo correção do conteúdo de comprovação do processo. Não invento uma chamada nem concluo que nada aconteceu internamente. |
| Critério condicional de ferramenta | Uma recusa permitida não falha automaticamente por não chamar ferramenta. |
| Mudança de pedido/e-mail | A autorização de um pedido não se transfere para outro. JSON ou autoridade alegada no chat não substituem validação. |
| Histórico da conversa | Uso o histórico para entender o pedido atual, sem transformar respostas anteriores da Lia em regra oficial. |
| Arredondamento ou prioridade não definidos | Mantenho a dúvida no aspecto afetado, preservando outras falhas demonstradas. |
| Restrição alimentar | Distingo ingredientes, traços e alegações de segurança. Uma ressalva posterior não apaga uma garantia indevida na mesma resposta. |
| Referência ausente | Não uso o título da referência como se tivesse acesso ao conteúdo. |
| Aprovação do modelo antes da calibração | Mantenho a revisão humana pendente, mesmo quando o resultado provisório é passou. |

Também acrescentei uma proteção operacional: se o juiz devolver critérios incompletos, citações inexistentes ou uma aprovação sem citação, preservo a resposta e o custo e rejeito o julgamento. O comportamento padrão interrompe novas chamadas daquele processo. Na rodada integral, habilitei uma opção explícita para seguir com outros turnos quando o erro é apenas de formato e o consumo está conhecido. O turno inválido continua pendente, sem retentativa automática. Erros de acesso, saída truncada ou consumo desconhecido continuam bloqueando o processo.

Na primeira avaliação integral, descobri que a validação de citações rejeitava um trecho porque o juiz retirou o negrito Markdown. Passei a aceitar diferenças de negrito, código em linha e espaços, sem mudar palavras, valores, acentos ou negações. O registro informa quando a citação é literal e quando depende dessa equivalência. Recuperei o parecer já recebido, preservando o retorno original e sem outra chamada paga.

Em outro turno, o modelo escreveu explicações antes do JSON. Mantive esse retorno como inválido: a análise parecer plausível não basta para cumprir o contrato da automação. Organizei a retomada para reaproveitar os pareceres válidos e lembrar também as tentativas inválidas. Assim, continuar a avaliação não cobra de novo por turnos já tentados.

## Como testei os ajustes

Primeiro usei três controles: oferta opcional com conta correta, inclusão indevida de item pago e conta errada acompanhada de oferta. Eles produziram os rótulos propostos nos três exemplos.

Depois ampliei para 17 exemplos, cobrindo também omissões, histórico, privacidade, instruções maliciosas ao avaliador, arredondamento e alegações de saúde. A rubrica 0.3 concordou com a proposta em 15 dos 17 exemplos. Esses números não são uma medida de acurácia do juiz em produção: são uma comparação com rótulos que preparei e ainda precisam de revisão da equipe.

Uma divergência mostrou que eu precisava separar melhor “não divulgou” de “comprovou autorização”. A outra revelou ambiguidade no próprio exemplo de controle: ele misturava conteúdo correto com comprovação de consulta interna. Registrei o resultado original e criei um controle mais explícito, com dois critérios separados, sem alterar o golden.

Na rubrica 0.4, um reteste dirigido encontrou aprovação indevida do total final e uma aprovação sem a citação obrigatória. O segundo problema interrompeu o lote após quatro chamadas. A rubrica 0.5 tornou essas exigências explícitas e passou por um novo reteste dirigido. Cada rodada mantém seu próprio snapshot da rubrica, exemplos, retornos brutos, julgamentos e consumo.

No último reteste, a rubrica **0.5 concordou com os oito resultados propostos**, com custo estimado de US$ 0,1372965. Também concluí **68 testes locais**, incluindo orçamento, sessões, validação de julgamentos, sinal de desconto, reaproveitamento de tentativas e exigência de revisão. Não somei as concordâncias de versões diferentes como se fossem uma única validação independente.

Criei o comando `tests.automacao.calibrar` para repetir esse processo de forma organizada. Os [exemplos controlados](../tests/automacao/fixtures/calibracao-juiz-proposta.json) estão identificados como sintéticos ou como reaproveitamento de resposta histórica. Eles não aumentam o golden nem se passam por respostas novas da Lia.

## Como vou fazer a calibração com a equipe

1. Vou separar uma amostra de desenvolvimento e outra de validação que não vou usar para ajustar a rubrica. Quero incluir acertos, falhas, ambiguidades e casos críticos das oito categorias, preservando conversas completas quando o histórico for necessário.
2. Vou pedir que dois integrantes classifiquem os critérios com a base oficial antes de ver a nota do modelo. As divergências entre pessoas precisam ser discutidas; não vou assumir que o juiz está errado quando o próprio esperado estiver ambíguo.
3. Com os rótulos humanos alinhados, vou comparar o Sonnet por critério: concordância, falsas aprovações, falsas reprovações e uso indevido de inconclusivo. Vou examinar todos os casos críticos divergentes, sem esconder o problema numa média geral.
4. Vou ajustar uma hipótese por vez, registrar a versão e repetir os exemplos de desenvolvimento. Quando estiverem consistentes, vou avaliar a amostra separada. Se precisar usá-la para ajustar a rubrica, deixará de ser uma validação independente.
5. Vou comparar Haiku 4.5 e a variante de Qwen acordada na mesma amostra, depois de confirmar acesso e preço. Não vou executar o golden inteiro em vários modelos apenas para experimentar.
6. Só depois da revisão vou congelar a rubrica para comparar as versões original e corrigida. Mudar o juiz entre as duas versões pode confundir melhora do agente com mudança do avaliador.

Ainda precisamos acordar o tamanho da amostra e os limites de aceitação da calibração. Esses limites são diferentes dos thresholds de Go/No-Go da Lia. Não defini uma taxa arbitrária como aprovação oficial do juiz.

Minha proposta inicial para discutir é usar **16 conversas de desenvolvimento** (duas por categoria, procurando acerto e falha) e **oito conversas separadas para validação** (uma por categoria). Vou acrescentar exemplos ambíguos se eles não estiverem representados, sem contar os controles sintéticos como novas conversas reais. É uma amostra prática para começar, não uma comprovação estatística de confiabilidade. Para erros críticos, quero que toda divergência seja resolvida antes de confiar no resultado automático; a regra oficial de aceitação ainda depende da equipe.

## Como preservei o orçamento

Tratei US$ 16 como teto operacional da minha conta e mantive US$ 4 de margem. Cada lote tem limite de dinheiro e de chamadas; reiniciar o processo não libera o limite já utilizado. O controle é persistente e considera o gasto externo informado, atualmente zero.

O valor calculado pelos tokens é uma estimativa, não uma consulta à fatura. Falhas sem métricas mantêm uma reserva conservadora. Não reutilizo o orçamento de outros integrantes e não ativo um modelo alternativo silenciosamente.

Minha sequência é validar localmente, testar poucos exemplos no juiz, revisar e só então ampliar. Vou estimar o custo restante com os consumos observados e reservar verba para avaliar as duas versões. Se o plano de repetições não couber no saldo, precisaremos redistribuir as execuções entre as contas da equipe ou reduzir um lote exploratório, sem reduzir silenciosamente o requisito acordado.

## Estado e limites da suíte

Já consigo executar casos reais ou reler evidências, preservar sessões e turnos, enviar o prompt corrigido em todos os turnos, guardar os retornos, aplicar verificações numéricas, chamar o Sonnet, reutilizar julgamentos compatíveis e gerar relatórios e templates de revisão. Também comparo relações numéricas de três pares metamórficos; as relações semânticas dos outros dois ainda exigem revisão.

Além de aprovar golden e thresholds, ainda falta concluir a calibração humana, resolver referências/ambiguidades e demonstrar o comportamento nas execuções planejadas. A T17 precisa da validação específica de ferramentas e argumentos; capturar `ferramentas` não conclui essa tarefa. A API ainda pode omitir `versao`, o que impede confirmar automaticamente a versão interna aplicada.

Também não implementei retomada automática de um processo encerrado no meio de uma conversa nem um comparador final entre duas campanhas completas. Hoje posso selecionar casos e comparar os relatórios, mas não devo apresentar esse fluxo como uma retomada transparente. Integração contínua pode ser acrescentada depois; não é necessária para demonstrar a primeira execução local.

Latência e tokens já são preservados nos registros, mas ainda preciso consolidar a comparação entre versões com as estatísticas e repetições da entrega. As severidades automáticas também são sugestões amplas por categoria: uma consulta ignorada e uma divulgação indevida não têm necessariamente o mesmo impacto. Quero refinar isso por tipo de falha com a equipe antes do parecer final, sem usar a contagem provisória de “crítico” como prova de vazamentos.

Ao receber a orientação de priorizar o juiz, interrompi a primeira coleta após 67 respostas salvas. Mantive essa pasta como parcial e registrei a interrupção. Como o encerramento externo impediu a finalização do manifesto, acrescentei a gravação do progresso antes de cada chamada para melhorar o registro de futuras interrupções. A coleta parcial não será apresentada como uma run completa.

## Primeira rodada completa

Depois do polimento, concluí uma nova coleta com **46 casos e 82 turnos**, em uma repetição da versão original solicitada. Todas as respostas chegaram com HTTP 200 e contrato técnico válido. Isso comprova a coleta, não o atendimento das regras da loja. Os 82 retornos vieram com `ferramentas: []` e sem `versao`; não usei esses campos para afirmar o que aconteceu internamente.

A avaliação sinalizou **44 casos com falhas e dois inconclusivos**, ainda sujeitos a revisão. O fato de haver divergências com a base é esperado neste desafio; a contagem não demonstra que cada causa seja corrigível por prompt. Uma falha demonstrada em um turno continua visível mesmo quando outro critério da conversa está pendente.

Das 82 tentativas do juiz, **76 produziram julgamentos válidos**. Rejeitei seis: quatro tinham prosa fora do JSON, uma tinha citação não localizada e uma aprovava sem citação. Esses seis turnos abrangem nove critérios sem julgamento semântico válido. Não contei o problema do avaliador como defeito da Lia. Preservei as evidências para revisão, sem gastar com retentativas.

O lote integral ficou em **US$ 1,470843 estimados**. O acumulado local, incluindo pilotos, polimento e reservas, ficou em **US$ 2,0939655**; restam **US$ 13,9060345** do teto operacional de US$ 16, considerando gasto externo informado de zero. Deste acumulado, US$ 0,1138665 são reservas de tentativas anteriores sem consumo conhecido. A fatura continua sendo a confirmação da cobrança real.

O relatório da primeira rodada (arquivo local: `results/automacao/golden-run-01/2026-10-17T161300-734940Z-3ebe129f/relatorio-primeira-run.md`) reúne resultados, limitações e links para cada turno. Essa pasta é local e ignorada pelo Git; o link só estará disponível à equipe depois da seleção das evidências para compartilhamento.

## Como deixei o código mais fácil de acompanhar

Depois de encerrar a rodada paga, revisei a organização do código. Coloquei uma explicação no início de cada arquivo Python, detalhando sua responsabilidade e o que ele recebe ou produz. Também documentei os arquivos de dependências. Mantive os JSONs válidos, sem comentários incompatíveis com o formato.

Separei a montagem da requisição, o envio, a criação da evidência e a verificação técnica do fluxo principal de execução. Na avaliação, separei a leitura das evidências, a criação do template de revisão e a geração do resumo. Troquei abreviações pouco claras por nomes descritivos e distribuí condições e estruturas grandes em linhas mais fáceis de ler. Mantive os comandos, o formato dos registros e a rubrica 0.5.

Os testes locais encontraram dois erros durante essa reorganização: um parâmetro faltando na geração do resumo e a troca indevida do nome de um argumento de ordenação do Python. Corrigi ambos antes de concluir. Os **68 testes passaram** e conferi novamente todos os 46 casos, 82 turnos, 99 critérios e cinco pares com os julgamentos salvos: os resultados permaneceram iguais. A única normalização necessária na comparação foi o caminho relativo/absoluto para o mesmo arquivo de julgamentos. Essa conferência não chamou a Lia nem o Bedrock.

Guardei a verificação da refatoração (arquivo local: `results/automacao/golden-run-01/2026-10-17T161300-734940Z-3ebe129f/verificacao-refatoracao.json`) junto à rodada. Para apresentar à equipe, vou seguir a ordem: golden, coleta, evidências, avaliação, revisão e orçamento; a divisão dos arquivos acompanha esse fluxo.

Os comandos e a organização dos arquivos estão no [guia de execução](t15-t16-automacao.md). As propostas de mudança no agente estão em [sugestões de correção do prompt](t15-t16-sugestoes-prompt.md). Não fiz commit, push ou PR durante este trabalho.
