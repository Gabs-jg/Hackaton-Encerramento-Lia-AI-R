# *Hackathon* de Encerramento – Desafio 3 

<div align="center">

**Chatbot Lia do e-commerce fictício Pop & Doce**
> **STATUS:** Projeto de *Quality Engineering (QE)* em desenvolvimento ativo. As etapas de exploração e refinamento do *prompt* estão em execução para fundamentar o parecer técnico do grupo.

</div>

## Sobre o projeto

### *"Como podemos garantir a exatidão, a segurança e a conformidade de um assistente de vendas baseado em IA generativa antes da sua implementação para a rodução?"* 

A partir deste desafio, a nossa **Squad** estruturou uma campanha de QE voltada para a avaliação da assistente virtual **Lia**, um agende de vendas da loja fictícia **Pop & Doce**. 

O projeto tem como premissa principal submeter a assistente a baterias de testes exploratórios e de segurança (*Red Teaming*), para identificação de alucinações, *jailbreaks* e outras vulnerabilidade / inconsistências que poderiam gerar impacto reputacional negativo para o negócio em diversos âmbitos. A partir dos achados do grupo, foram propostas melhorias no *prompt* de sistema, comparando os resultados entre a *baseline* e a versão final para embasar, em fatos e dados, a decisão do parecer de produção ou impedimento de produção (**Go / No-Go**). 

Para isso, a estratégia adotada leva em consideração a pasta `base-de-conhecimento-oficial` e as massas de testes fornecidas como referência para funcionarem como **oráculo** do projeto, visto que a base interna do *chatbot* pode ter divergências intencionais como parte do *Hackaton* dos estagiários. 

--- 

## Por Onde Começar? 

* [Quadro de Planejamento e Decisões da Squad (Trello)](https://trello.com/b/PdUBDmTM)
* [Quadro de Execução de Tarefas (Trello)](https://trello.com/b/M4EHkt4l)
* [Passo-a-passo para validação da equipe (Trello)](https://trello.com/c/mlQrpA0X)

## Arquitetura e Estrutura do Repositório 

O repositório foi organizado de maneira modular para preservar a identificação ágil das informações, mantendo a rastreabilidade entre fontes, casos de teste e as evidências colectadas:

```
Hackaton-Encerramento-Lia-AI-R/
├── README.md
├── massa-de-teste.md                  # Pedidos, perfis e clientes fictícios fornecidos
├── requirements-juiz.txt
├── requirements-t15.txt
├── base-de-conhecimento-oficial/      # Oráculo de dados oficiais da empresa
│   ├── 01-catalogo-pipocas.md
│   ├── 02-catalogo-balas.md
│   ├── 03-kits-e-presentes.md
│   ├── 04-politicas.md
│   ├── 05-perguntas-frequentes.md
│   └── 06-sobre-a-empresa.md
├── datasets/                          # Datasets de avaliação automatizada
│   ├── .gitkeep
│   ├── golden-v0.2.json
│   ├── golden-v0.3.json
│   ├── t15-piloto.json
│   └── pilotos/
├── prompts/                           # Iterações e versões do prompt de sistema
│   └── .gitkeep
├── docs/                              # Documentação técnica, decisões e critérios
│   ├── decisoes.md
│   ├── riscos-criterios-corrigidos.md
│   ├── t12-criterios-golden.md
│   ├── t13-t14-golden.md
│   ├── t13-t15-convencao-arredondamento.md
│   ├── t15-executor-piloto.md
│   ├── t15-t16-automacao.md
│   ├── t15-t16-processo-automacao.md
│   ├── t15-t16-sugestoes-prompt.md
│   └── exploracao/                    # Casos de exploração documentados
│       ├── t03-casos.md
│       ├── t04-casos.md
│       ├── t05-casos.md
│       └── t06-casos.md
├── tests/                             # Infraestrutura e código da suíte de testes
│   ├── .gitkeep
│   ├── __init__.py
│   ├── automacao/                     # Engine de testes automatizados e Juiz LLM
│   │   ├── __init__.py
│   │   ├── avaliacao.py
│   │   ├── avaliar.py
│   │   ├── calibrar.py
│   │   ├── casos.py
│   │   ├── cliente.py
│   │   ├── executar.py
│   │   ├── funcional.py
│   │   ├── golden.py
│   │   ├── juiz.py
│   │   ├── julgamentos.py
│   │   ├── orcamento.py
│   │   ├── registros.py
│   │   ├── test_executor.py
│   │   ├── test_golden.py
│   │   ├── test_integracao_v03.py
│   │   ├── config/
│   │   │   ├── avaliacao-golden-v0.2.json
│   │   │   └── avaliacao-provisoria.json
│   │   └── fixtures/
│   │       ├── calibracao-juiz-proposta.json
│   │       └── prompt-integracao.txt
│   ├── postman/                       # Coleções de API do Postman
│   │   ├── .gitkeep
│   │   ├── t03-t04-exploracao.postman_collection.json
│   │   ├── t05-t06-exploracao.postman_collection.json
│   │   ├── t08-t10-exploracao.postman_collection.json
│   │   └── t18-red-team.postman_collection.json
│   └── red-team/                      # Suite de segurança adversarial (Promptfoo)
│       ├── package-lock.json
│       ├── package.json
│       ├── promptfooconfig.yaml
│       ├── provider-lia.js
│       ├── assercoes/
│       │   ├── ferramentas.js
│       │   └── privacidade.js
│       └── casos/
│           ├── comercial.yaml
│           ├── extracao.yaml
│           ├── injection.yaml
│           ├── privacidade.yaml
│           └── saude.yaml
└── results/                           # Evidências, logs de execução e relatórios
    ├── .gitkeep
    ├── exploracao/                    # Resultados da fase exploratória
    │   ├── t03-t04-resultados.json
    │   ├── t05-t06-complementar-2026-10-16-resultados.json
    │   ├── t05-t06-resultados.json
    │   ├── t06-reteste-2026-10-16-manifesto.json
    │   ├── t06-reteste-2026-10-16-resultados.json
    │   ├── t07-t09-resultados.json
    │   ├── t08-t10-resultados.json
    │   ├── relatorios/                # Registros consolidados da exploração
    │   │   ├── t03-t04-registro.md
    │   │   ├── t05-registro.md
    │   │   ├── t06-registro.md
    │   │   ├── t07-t09-registro.md
    │   │   ├── t08-registro.md
    │   │   └── t10-registro.md
    │   ├── t03/evidencias/            # Evidências individuais por caso (T03-C01 a T03-C17)
    │   ├── t04/evidencias/            # Evidências individuais por caso (T04-AR01 a T04-AR13)
    │   ├── t05/evidencias/            # Evidências individuais (T05-EX, T05-MC, etc.)
    │   ├── t06/evidencias/            # Evidências individuais (T06-CP, T06-EX, etc.)
    │   ├── t08/evidencias/            # Evidências por turno (T08-MT01 a T08-MT10)
    │   └── t10/evidencias/            # Evidências adversariais (T10-ADV01 a T10-ADV08)
    ├── metamorficos/                  # Evidências e relatórios dos testes metamórficos
    │   ├── relatorios/
    │   │   └── t14-registro.md
    │   └── t14-rodada-01/
    │       ├── avaliacao.json
    │       ├── manifesto.json
    │       ├── resultados.json
    │       └── evidencias/
    └── red-team/                      # Evidências dos testes adversariais
        ├── .gitkeep
        ├── casos-reaproveitados-exploracao.md
        ├── exploracao-manual-casos.md
        ├── exploracao-manual-registro.md
        ├── log-red-team.md
        ├── plano-red-team.md
        ├── exploracao/
        │   ├── t18-exploracao-postman-2026-10-17.json
        │   └── t18/evidencias/
        └── promptfoo/
            └── validacao-original-2026-10-17.json
```
> **Nota:** Diretórios reservados às próximas entregas estão sendo mantidos com `.gitkeep`, para preservação da hierarquia das pastas.

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

## Entregas Previstas da Campanha 

Ao final do *hackaton*, a equipe disponibilizará os seguintes entregáveis: 

- [x] ***Golden dataset* Robusto:** com, pelo menos, 40 casos nas oito categorias e cinco pares de metamórficos;
- [ ] **Suíte de Testes Automatizada:** Automação contendo verificações de chamadas de ferramenta (*fuction calling*), validação de cupons e fluxo de pedidos; 
- [x] **Campanha de Red Teaming:** Mapeamento e execução de, no mínimo, 30 ataques organizados e distribuíds em cinco categorias de vulnerabilidade;
- [ ] **Análise Comparativa de *prompts:*** Avaliação da suíte (com mínimo de três execuções / caso), confrontando a *baseline* com a versão final do *prompt* atualizado. Avaliando, assim, métricas, latência e consumo de *tokens*; 
- [ ] **Repositório Reproduzível + Parecer Final:** Repositório 100% reproduzível, contendo relatório final de *Go / No-Go* de até 8 páginas e apresentação técnica de 15~20 minutos para a banca avaliadora. 

---

## Autoria e Créditos

Este projeto foi desenvolvido pela **Squad 2**, durante o **ESTÁGIO | AWS AI FDE DRIVEN QUALITY ENGINEERING** promovido pela **Compass UOL** / [AI/R Company](https://aircompany.ai/pt/home/), sob orientação do instrutor **[Jacques de Jesus Figueredo Schmitz Jr.](https://github.com/juniorschmitz)**.

### Integrantes da Squad 2: 
* **[Camile Marcele Pereira de Araujo](https://github.com/camimcl)**
* **[Fernanda Bastos dos Santos](https://github.com/codebyfernanda)**
* **[Gustavo Linkevick Brasileiro](https://github.com/gustavolkbr)**
* **[João Gabriel Oliveira Magalhães](https://github.com/Gabs-jg)**

## Golden e pares metamórficos

O [golden atual](datasets/golden-v0.3.json), revisão 0.3.1, reúne 48 casos, 86 turnos e cinco pares, pendentes de revisão. A [convenção provisória de arredondamento](docs/t13-t15-convencao-arredondamento.md) é decisão da equipe. Consulte a [documentação T13/T14](docs/t13-t14-golden.md). O [golden v0.2](datasets/golden-v0.2.json) permanece como referência histórica; suas evidências não comprovam a execução dos novos casos.

## Automação T15/T16

Consulte o [guia da automação](docs/t15-t16-automacao.md) e o [registro do processo](docs/t15-t16-processo-automacao.md). A integração local usa 48 casos e 86 turnos; a primeira run preservada corresponde à v0.2, com 46 casos e 82 turnos. A execução do golden atualizado ainda está pendente.
