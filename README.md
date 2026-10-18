# *Hackathon* de Encerramento – Desafio 3 
*Chatbot* Lia do *e-commerce* fictício Pop & Doce

> **STATUS:** Projeto de *Quality Engineering (QE)* em desenvolvimento ativo. As etapas de exploração e refinamento do *prompt* estão em execução para fundamentar o parecer técnico do grupo. 

## Sobre o projeto

### *"Como podemos garantir a exatidão, a segurança e a conformidade de um assistente de vendas baseado em IA generativa antes da sua implementação para a rodução?"* 

A partir deste desafio, a nossa **Squad** estruturou uma campanha de QE voltada para a avaliação da assistente virtual **Lia**, um agende de vendas da loja fictícia **Pop & Doce**. 

O projeto tem como premissa principal submeter a assistente a baterias de testes exploratórios e de segurança (*Red Teaming*), para identificação de alucinações, *jailbreaks* e outras vulnerabilidade / inconsistências que poderiam gerar impacto reputacional negativo para o negócio em diversos âmbitos. A partir dos achados do grupo, foram propostas melhorias no *prompt* de sistema, comparando os resultados entre a *baseline* e a versão final para embasar, em fatos e dados, a decisão do parecer de produção ou impedimento de produção (**Go / No-Go**). 

Para isso, a estratégia adotada leva em consideração a pasta `base-de-conhecimento-oficial` e as massas de testes fornecidas como referência para funcionarem como **oráculo** do projeto, visto que a base interna do *chatbot* pode ter divergências intencionais como parte do *Hackaton* dos estagiários. 

--- 

## Por Onde Começar? 

* [Regras de Campanha de Qualidade]()
* [Caso e Relatórios da Fase Exploratória]()
* [Quadro de Planejamento e Decisões da Squad (Trello)](https://trello.com/b/PdUBDmTM)
* [Quadro de Execução de Tarefas (Trello)](https://trello.com/b/M4EHkt4l)
* [Passo-a-passo para validação da equipe (Trello)](https://trello.com/c/mlQrpA0X)

## Arquitetura e Estrutura do Repositório 

O repositório foi organizado de maneira modular para preservar a identificação ágil das informações, mantendo a rastreabilidade entre fontes, casos de teste e as evidências colectadas:

```
Hackaton-Encerramento-Lia-AI-R/
├── README.md
├── massa-de-teste.md                  # Pedidos, perfis e clientes fictícios fornecidos para execução
├── base-de-conhecimento-oficial/      # Oráculo de dados oficiais fornecidos pelo orientador
│   ├── 01-catalogo-pipocas.md
│   ├── 02-catalogo-balas.md
│   ├── 03-kits-e-presentes.md
│   ├── 04-politicas.md
│   ├── 05-perguntas-frequentes.md
│   └── 06-sobre-a-empresa.md
├── datasets/                          # Golden dataset (40 casos) e testes metamórficos
├── prompts/                           # Iterações e versões do prompt de sistema da Lia
├── docs/                              # Decisões arquiteturais, matrizes de regras e pareceres
│   └── exploracao/                    # Detalhamento dos casos
├── tests/                             # Suíte automatizada e coleções de teste
│   └── postman/                       # Coleções importáveis (turnos e cenários sem chaves)
└── results/                           # Evidências, logs de execução e comparações
    ├── exploracao/                    # JSONs consolidados, capturas por caso e relatórios
    │   └── relatorios/                # Análise comparativa esperado × obtido
    └── red-team/                      # Registros e evidências dos ataques adversariais
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
