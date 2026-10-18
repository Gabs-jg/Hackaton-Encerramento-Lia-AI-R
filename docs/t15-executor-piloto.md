# T15 — Executor piloto com DeepEval

**Continuação:** para o golden v0.2, avaliação funcional e configuração do juiz, consultar [T15/T16 — Execução e avaliação do golden](t15-t16-automacao.md). O texto abaixo registra o piloto inicial.

Base para apresentar na reunião e combinar com a T13 o formato do golden. O piloto reutiliza três candidatos de T05/T06, com **3 casos e 4 turnos**. O JSON é provisório, não é o golden aprovado.

**Escopo:** executar mensagens, controlar sessões e versões e salvar evidências completas. DeepEval verifica somente o envelope técnico e recebe um `LLMTestCase` por turno, incluindo nomes e argumentos das ferramentas. Uma resposta com preço incorreto pode passar nesse contrato: a avaliação funcional continua **não realizada**, pendente das tarefas 16 e 17. Não há modelo juiz ou consumo de AWS própria nesta base.

## Arquivos

| Arquivo | Papel |
|---|---|
| [t15-piloto.json](../datasets/pilotos/t15-piloto.json) | Proposta de formato e três casos candidatos |
| [executar.py](../tests/automacao/executar.py) | Execução sequencial e coordenação dos registros |
| [cliente.py](../tests/automacao/cliente.py) | POST na API oficial ou leitura das evidências históricas |
| [casos.py](../tests/automacao/casos.py) | Leitura/validação do formato; ponto de adaptação após a call |
| [avaliacao.py](../tests/automacao/avaliacao.py) | Adaptação ao DeepEval e contrato técnico local |
| [registros.py](../tests/automacao/registros.py) | JSON por tentativa, manifesto e resumo Markdown/JSON |

## Preparação

Na raiz desta branch, com Python 3.12:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-t15.txt
.\.venv\Scripts\python.exe -m tests.automacao.executar --validar
```

Para chamadas reais, configurar `LIA_API_KEY` no ambiente ou no `.env` local ignorado pelo Git. `--env-file caminho` permite apontar outro arquivo local. Não copiar a chave para o dataset, terminal, relatório ou coleção exportada.

## Demonstração sem chamadas

```powershell
.\.venv\Scripts\python.exe -m tests.automacao.executar --modo replay
```

O replay confere o fluxo com respostas da exploração já disponíveis. Preserva o caminho e a data da evidência original; não é uma nova execução da Lia, nem comprova estabilidade, latência atual ou versão corrigida. Por isso, aceita apenas a versão original e uma leitura por caso.

## Piloto pela API

```powershell
.\.venv\Scripts\python.exe -m tests.automacao.executar --modo api --fase-base nao_confirmada
```

Cada execução gera uma pasta exclusiva em `results/piloto-t15/`, ignorada pelo Git para revisão antes de publicação. O caminho é mostrado ao iniciar. Usar `--caso T15-P03` para selecionar um caso; a opção pode ser repetida. `--repeticoes 3` prepara repetições independentes, mas o dataset piloto não substitui o golden formal.

Para verificar o envio de `prompt_sistema`, existe um [prompt técnico de integração](../tests/automacao/fixtures/prompt-integracao.txt). Ele é apenas uma entrada de teste da T15, **não o prompt corrigido da tarefa 21**:

```powershell
.\.venv\Scripts\python.exe -m tests.automacao.executar --modo api --versao corrigida --prompt tests/automacao/fixtures/prompt-integracao.txt --fase-base nao_confirmada
```

Original não envia `prompt_sistema`; corrigida exige arquivo de prompt e o envia em todos os turnos. `versao` ausente é aviso explícito; não se inventa confirmação da versão. O hash do prompt permite identificar a entrada usada no piloto.

Uma chamada por vez neste executor. Se outros integrantes ou promptfoo estiverem executando, coordenar para respeitar o total de quatro chamadas simultâneas da squad. Não há teste de carga.

## Registros e erros

```text
results/piloto-t15/<execucao>/
├── manifesto.json
├── dataset.json
├── resumo.json
├── resumo.md
└── T15-P02/r01/
    ├── t01-a01.json
    └── t02-a01.json
```

- Cada tentativa salva entrada, critério esperado, fonte, horários UTC, tempo HTTP, status, resposta integral decodificada (inclusive campos extras), ferramentas, todos os itens de métricas e adaptação ao DeepEval. Corpo não JSON também fica registrado. Cabeçalhos com credenciais não são salvos; eventual reflexão da chave é substituída por `[SEGREDO_REMOVIDO]`.
- Manifesto: modo API/replay, versão solicitada, fase da base declarada, commit/alterações locais, hashes do código/dataset/prompt, dependências, concorrência e repetições. A fase da base não é detectada automaticamente.
- Sessão nova por caso/repetição; continuidade só dentro do caso. Sem T2 se T1 falhar tecnicamente. Mudança de sessão dentro do caso ou reutilização entre casos é registrada como erro de contrato.
- Timeout, conexão, HTTP 429 e 5xx são inconclusivos de ambiente. HTTP 400/401/403 indicam configuração a conferir. Resposta 200 fora do contrato é erro de contrato, sem concluir automaticamente que há defeito comercial na Lia.
- Não há retry automático por padrão. `--retentativas-429 1` permite uma nova tentativa após espera; todas as tentativas ficam salvas. Timeout/5xx não são reenviados automaticamente, pois o turno pode ter sido processado. Nunca repetir para substituir uma reprovação funcional por aprovação.
- `resultado_execucao` indica a integração; `resultado_contrato` indica a métrica técnica; `resultado_funcional: nao_avaliado` não entra numa taxa de aprovação da Lia. Ausência de `ferramentas` difere de lista vazia. Não se inventam resultados internos das ferramentas nem `retrieval_context`.

## Formato provisório para discutir com João

```json
{
  "formato": "lia-piloto-v1",
  "estado": "rascunho_para_discussao",
  "casos": [{
    "id": "T15-P01",
    "origem_exploracao": "T05-MC01",
    "categoria": "montagem_calculo",
    "revisado": false,
    "turnos": [{
      "mensagem": "Entrada do usuário",
      "criterio_esperado": "Critério independente da resposta da Lia"
    }],
    "referencias": [{
      "arquivo": "base-de-conhecimento-oficial/04-politicas.md",
      "secoes": ["Frete grátis"]
    }]
  }]
}
```

O exemplo acima ilustra campos, não é um caso funcional pronto. No arquivo piloto, `evidencia_replay` é opcional e serve apenas à demonstração histórica; não é enviado à Lia. Sessão, prompt e resposta observada ficam fora da entrada do dataset. O leitor confere IDs únicos, categorias, turnos e existência dos arquivos/seções citados.

**Decisões para a call:** nomes dos campos e categorias; critérios por turno ou conversa; vínculo às decisões da T12 e aos pares da T14; representação das verificações numéricas/semânticas e de ferramentas; responsáveis por T16/T17. O esperado continua separado do observado. Os três pilotos não cobrem as oito categorias nem os 40 casos obrigatórios.

## Estado da validação em 16 de outubro de 2026

- 25 testes locais do executor passaram; dependências conferidas sem conflitos.
- Replay dos três casos concluído, com quatro turnos históricos. A variável de sessão do Postman em T05-MC10 é resolvida apenas no replay e permanece identificada no registro, sem alterar a evidência original.
- API: três casos/quatro turnos originais e um caso/dois turnos com o prompt técnico de integração, todos com HTTP 200 e contrato técnico válido. Confirmado envio de `prompt_sistema` em ambos os turnos selecionados, com sessão nova para a nova conversa e continuidade dentro dela.
- **Limitações observadas:** os seis retornos novos têm `ferramentas: []` e não incluem `versao`. A consulta PD-1001 respondeu com uma saudação em vez dos dados solicitados. Isso não foi convertido em aprovação funcional nem usado para alterar o oráculo.
- A adaptação de ferramentas ao DeepEval foi conferida com as evidências históricas e respostas controladas. **A demonstração de uma chamada de ferramenta registrada na API atual continua pendente**, assim como confirmar a versão aplicada quando a API não retorna esse campo. Estes dados não comprovam mudança de base, ferramenta desligada ou causa interna.

O executor está disponível como base da T15; a tarefa não deve ser considerada concluída integralmente apenas por este piloto. As saídas completas ficam em `results/piloto-t15/`, com pastas distintas por execução.

## Verificação do executor

```powershell
.\.venv\Scripts\python.exe -m unittest tests.automacao.test_executor -v
```

Esses testes usam respostas controladas, sem enviar requisições à Lia. Conferem isolamento/continuidade de sessão, prompt por turno, preservação de dados, classificação de erros e proteção da chave.

Referências técnicas: [métricas personalizadas do DeepEval](https://deepeval.com/docs/metrics-custom), [LLMTestCase e ToolCall](https://deepeval.com/docs/evaluation-test-cases) e [configuração de telemetria](https://deepeval.com/docs/environment-variables). O piloto usa `measure()` local, sem serviço de avaliação externo; a telemetria e as gravações próprias do DeepEval ficam desativadas. As evidências são gravadas pelo executor.
