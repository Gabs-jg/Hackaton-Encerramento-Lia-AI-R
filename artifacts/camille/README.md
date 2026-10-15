# Exploração da Camille · T02, T05 e T06

Material das tarefas [T02](https://trello.com/c/mlQrpA0X), [T05](https://trello.com/c/BtnvbbkL) e [T06](https://trello.com/c/RRrFl88I). Revisão: João Gabriel (`Gabs-jg`), conforme [DIS-12](https://trello.com/c/8xuncMAC).

- [`t02-t05-t06-exploracao.postman_collection.json`](t02-t05-t06-exploracao.postman_collection.json): coleção única importável, organizada em **tarefa → caso → T1/T2**, seguindo a estrutura do template da squad. Cada requisição inclui a resposta real como exemplo salvo. T05 foi executada pelo Postman; T06, por curl. A coleção foi montada a partir dessas evidências, não exportada integralmente pela interface do Postman.
- [`t05-t06-resultados.json`](t05-t06-resultados.json): todos os casos com esperado, fontes, obtido, classificação, descrição e registros completos por turno. É o arquivo consolidado para análise e produção do Markdown.
- [Relatório T05](../../results/exploracao/t05-registro-camille.md) e [relatório T06](../../results/exploracao/t06-registro-camille.md): tabelas caso × esperado × obtido, legenda da squad, descrição e evidências.
- Os JSONs individuais permanecem em `results/exploracao/t05/evidencias/` e `t06/evidencias/`, com rastreabilidade por caso, execução e turno.

O arquivo já salvo pela Camille em [`../response`](../response) foi preservado. Seu conteúdo foi comparado à captura MC01; não conta como execução adicional.

## Usar a coleção

1. Importar o JSON consolidado, ou usar as coleções individuais de `tests/postman/`.
2. O header segue o template: `x-api-key: {{api_key}}`. Configurar `api_key` somente em ambiente local, sem publicar seu valor. Quem já configurou o Vault pode usar diretamente `{{vault:lia_api_key}}` no header em sua cópia local.
3. Enviar **T1** primeiro e depois **T2**, quando existir, no mesmo caso. O script mantém uma variável de sessão exclusiva por caso e impede T2 sem T1 válido. Caso novo começa sem sessão.
4. Ler o exemplo salvo para consultar a execução anterior sem reenviar. Reenviar é uma nova execução: preservar a anterior com novo número, sem sobrescrever a evidência.
5. Julgar pela base oficial e massa, nunca pelo exemplo de resposta da Lia. Os exemplos incluem respostas que **falharam**.

Não executar carga, Runner em paralelo ou repetição automática. Timeouts deliberados e erros de ambiente são inconclusivos, não defeitos da Lia. O uso de curl muda o cliente, não reduz necessariamente tokens ou custo de inferência da Lia.

## Legenda combinada

**SEVERIDADE:** crítico, alto ou baixo quando houver falha; — quando não se aplica.

**RESULTADO:** passou, falhou, instável ou inconclusivo. Instável exige repetições válidas divergentes; um único envio não permite essa conclusão.

**DESCRIÇÃO:** o que aconteceu, a divergência perante a referência, o impacto e a hipótese de correção. Hipótese não é diagnóstico confirmado. Correções de prompt/base e consolidação do golden pertencem às frentes posteriores.

Este material cobre a exploração das categorias da Camille; não declara o projeto completo nem T02 validada pelos quatro integrantes.
