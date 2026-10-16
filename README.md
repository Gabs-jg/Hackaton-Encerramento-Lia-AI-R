# *Hackathon* de Encerramento – Desafio 3 (Pop & Doce + *chatbot* Lia)

> **STATUS:** Projeto iniciado.

Projeto de Quality Engineering para avaliar a assistente de vendas Lia, propor melhorias no prompt e fundamentar uma decisão de Go/No-Go com evidências.

## Situação Inicial

O repositório conta com os materiais oficiais (fornecidos pelo nosso instrutor [Jacques de Jesus Figueredo Schmitz Jr.](https://github.com/juniorschmitz)) e a estrutura inicial de trabalho. A exploração de T05/T06 já possui coleção importável e resultados registrados. A suíte automatizada, os critérios de aprovação e o método de avaliação ainda serão definidos pela equipe da *Squad* 2, composta por Camile Marcele P. de Araújo, Fernanda B. dos Santos, Gustavo L. Brasileiro e João Gabriel O. Magalhães.

## Arquitetura do Projeto

| CAMINHO | CONTEÚDO |
| :---: | :---: |
| `base-de-conhecimento-oficial/` | Base fornecida pelo orientador; Referência para os próximos passos e escolhas estratégicas de desenvolvimento |
| `massa-de-teste.md` | Pedidos e clientes fictícios fornecidos para os testes |
| `datasets/` | *Golden dataset* e casos metamórficos revisados |
| `tests/` | Código e configurações da suíte automatizada |
| `tests/postman/` | Coleções importáveis com casos, turnos e exemplos de respostas, sem credenciais |
| `results/` | Evidências, resultados das execuções e comparação dos *prompts* |
| `results/exploracao/` | JSON consolidado e evidências por caso, execução e turno |
| `results/exploracao/relatorios/` | Análise de esperado × obtido, classificação e conclusões da exploração |
| `results/red-team/` | Registro das tentativas adversariais e as respectivas evidências |
| `prompts/` | Versões do *prompt* de sistema, seguidas das alterações |
| `docs/` | Decisões, tabelas de regras, pareceres e materiais da apresentação |

Pastas reservadas a entregas futuras são mantidas com `.gitkeep`.

## Organização do trabalho

Responsáveis, tarefas e critérios de conclusão ficam no [quadro de execução](https://trello.com/b/M4EHkt4l). Dúvidas e decisões ficam no [quadro de planejamento](https://trello.com/b/PdUBDmTM). A [T02](https://trello.com/c/mlQrpA0X) reúne o padrão de registro e os passos para validá-lo com a equipe, com referência ao [template proposto pelo Gustavo](https://trello.com/c/3NH4HOUA).

---

## Executar a exploração T05/T06

1. Importar [t05-t06-exploracao.postman_collection.json](tests/postman/t05-t06-exploracao.postman_collection.json) no Postman.
2. Configurar `api_key` apenas no ambiente local. Como alternativa, usar `{{vault:lia_api_key}}` no header `x-api-key` da cópia local. Nunca exportar o valor da chave.
3. Escolher a tarefa e o caso. Enviar **T1** e depois **T2**, quando existir, um turno por vez. Cada caso inicia sem `sessao`; os scripts mantêm a sessão apenas nos turnos do mesmo caso.
4. Para consultar uma execução anterior sem reenviar, abrir o exemplo salvo na requisição. Esses exemplos incluem respostas incorretas; o gabarito é a base oficial e a massa de teste.

As expectativas estão nos casos [T05](docs/exploracao/t05-casos.md) e [T06](docs/exploracao/t06-casos.md). Os relatórios [T05](results/exploracao/relatorios/t05-registro.md) e [T06](results/exploracao/relatorios/t06-registro.md) registram esperado × obtido, classificação e links das evidências. O [JSON de resultados](results/exploracao/t05-t06-resultados.json) reúne os 30 casos e 32 turnos, com origem Postman/curl identificada. A coleção foi montada a partir dessas evidências, preservadas também nos JSONs individuais.

## Regras de Avaliação

- A base oficial e a massa de teste são o **oráculo**. A base interna da Lia é deliberadamente diferente; as respostas da assistente não definem o gabarito.
- Não realizar testes de carga/estresse. Coordenar no máximo quatro chamadas simultâneas no total da equipe.
- Timeout deliberado do ambiente é inconclusivo: registrar a limitação sem contar como defeito ou aprovação da Lia.
- Usar somente a API fornecida e dados fictícios. A equipe não tem acesso à AWS que hospeda a Lia.
- Nunca publicar chaves, credenciais ou arquivos de configuração com segredos. Revisar também exportações do Postman e evidências.
- Recursos próprios da AWS/modelos são opcionais, com orçamento de US$ 20 por integrante.

## Entregas Previstas

- *Golden dataset* com pelo menos 40 casos nas oito categorias e cinco pares metamórficos.
- Suíte automatizada, incluindo verificações de ferramentas em pedidos e cupons.
- Registro de pelo menos 30 tentativas de *red teaming* em cinco categorias.
- *Prompt* corrigido e comparação da mesma suíte com pelo menos três execuções por caso em cada versão, incluindo aprovação, latência e tokens.
- Repositório reproduzível, decisões registradas, parecer *Go/No-Go* de até oito páginas e apresentação de 15–20 minutos com os quatro integrantes.

As instruções da suíte automatizada serão adicionadas quando sua implementação for definida. Prazo e envio final devem ser acompanhados no Trello.

## Autoria

Este projeto foi desenvolvido pelos membros da *Squad 2*, durante o **ESTÁGIO | AWS AI FDE DRIVEN QUALITY ENGINEERING** na [Compass UOL / AI/R Company](https://aircompany.ai/pt/home/).
