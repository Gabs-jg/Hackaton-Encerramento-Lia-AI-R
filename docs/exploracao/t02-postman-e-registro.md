# T02 — Preparação do Postman e padrão de evidências

Trello: https://trello.com/c/mlQrpA0X
Branch deste trabalho: `test/t02-t05-t06-exploracao-camile`.

## Escopo e estado

Preparação das coleções e padrão de registro para a exploração. As coleções incluem somente categorias das tarefas 05 e 06. A exploração da Camille foi executada e está documentada nos registros [T05](../../results/exploracao/t05-registro-camille.md) e [T06](../../results/exploracao/t06-registro-camille.md). A tarefa 02 ainda depende da validação do uso por todos os integrantes.

Preparação realizada em 14/10/2026: duas coleções importadas no workspace pessoal da Camille; Postman Desktop Agent 0.5.2 instalado e iniciado; segredo `lia_api_key` configurado pelo usuário no Vault e piloto executado. T05 foi executada no Postman e T06 por curl, após autorização da Camille, sem chamadas paralelas. A chave local para curl ficou em `.env`, ignorado pelo Git.

O [padrão acordado no Trello](https://trello.com/c/3NH4HOUA) foi aplicado: **caso → T1/T2**, com respostas reais salvas como exemplos. A [coleção consolidada e o JSON de resultados](../../artifacts/camille/README.md) reúnem apenas as tasks da Camille, com origem da evidência identificada.

## Configuração

1. Importar os arquivos de `tests/postman/t05-exploracao-camille.postman_collection.json` e `t06-exploracao-camille.postman_collection.json` no Postman.
2. As coleções adaptadas ao template usam `{{api_key}}` no header: configurar o valor somente localmente. Quem já usa **Local Vault** pode manter `{{vault:lia_api_key}}` no header de sua cópia local. Se houver restrição de domínio, usar o domínio da API fornecida. Não salvar a chave como valor compartilhado ou exportá-la.
3. Conferir a variável de coleção `lia_url`: endpoint oficial extraído do PDF, com POST, `Content-Type: application/json` e `x-api-key`.
4. Usar **Send** manualmente, um turno por vez. Coordenar no máximo quatro chamadas simultâneas na squad; sem Runner de carga, monitors ou repetição automática.
5. Na primeira configuração de cada integrante, enviar um piloto antes dos demais casos e conferir acesso, resposta e gravação da evidência. Os exemplos salvos permitem ler a exploração da Camille sem executar outra vez.

## Sessões e julgamento

- Primeiro turno omite `sessao` e limpa a variável do caso. Turnos seguintes usam a sessão retornada; o script interrompe o envio se ela não estiver disponível.
- Cada caso possui variável de sessão própria. Para repetir uma conversa, recomeçar pelo turno 1.
- Os scripts apenas apoiam a continuidade. Não decidem aprovação funcional nem substituem os avaliadores futuros da tarefa 16.
- Salvar a resposta de cada turno antes de enviar o seguinte. HTTP 200 sozinho não aprova o caso.
- Usar a base oficial/massa como referência. Não adaptar a expectativa para corresponder à resposta da Lia.
- Registrar `resposta`, `sessao`, `versao` quando disponível, `ferramentas` e todos os itens de `metricas`. Nesta exploração a API não retornou `versao`: a omissão está documentada e não foi preenchida artificialmente. Não solicitar CPF, endereço completo ou cartão; usar somente dados fictícios.

## Evidência e classificação

Para T05, salvar JSON em `results/exploracao/t05/evidencias/<ID>/exec-01-turno-01.json`; para T06, no caminho equivalente `t06/`. Acrescentar turno/execução no nome; nunca sobrescrever uma tentativa anterior.

Preencher o registro da tarefa com esperado/fonte, observado, evidência e a legenda da squad: **SEVERIDADE** crítico/alto/baixo quando houver falha; **RESULTADO** passou/falhou/instável/inconclusivo; **DESCRIÇÃO** com o ocorrido, erro, impacto e hipótese de correção (prompt, base etc.). Separar hipótese de causa de fato observado. Usar instável somente quando houver respostas válidas divergentes em repetições. Timeouts deliberados ficam como ambiente inconclusivo. Para resultado sem JSON, registrar o erro sem headers com segredo.

Proteger evidências antes de publicar: chave e credenciais não podem aparecer no corpo salvo, console, imagens ou exports. Se uma resposta expuser um segredo real, manter o bruto somente local e publicar trecho sanitizado com indicação da remoção.

## Rastreabilidade e colaboração

- Casos e arquivos pessoais usam prefixos T05/T06 e Camille. A nomenclatura das próximas branches e PRs deve incluir os IDs das tarefas e links dos cartões.
- Esta preparação está ligada a T02/T05/T06. Não alterar arquivos de catálogo, cupons, adversarial, vários turnos gerais, golden consolidado, avaliadores ou correção de prompt sem discutir a tarefa correspondente.
- O padrão será revisado com os outros integrantes antes de declarar T02 concluída para a squad.
- O registro detalhado e os achados locais não substituem a consolidação de defeitos da tarefa 20.

Referências de configuração: [segredos do Vault](https://learning.postman.com/docs/use/postman-vault/use-vault-secrets), [variáveis de coleção](https://learning.postman.com/docs/tests-and-scripts/write-scripts/postman-sandbox-reference/pm-variables/), [interrupção de requisição](https://learning.postman.com/docs/tests-and-scripts/write-scripts/postman-sandbox-reference/pm-execution/). Contrato da Lia: enunciado oficial, páginas 4–7.
