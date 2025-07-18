## Situação Comum 2

A situação agora analisada é a integração com APIs REST: É uma prática comum em engenharia de dados, especialmente para ingestão de dados de fontes externas. Muitas vezes, essas APIs fornecem informações em tempo real ou atualizadas periodicamente, e é fundamental que o engenheiro de dados saiba consumir, tratar e armazenar esses dados de forma eficiente e confiável.

### 1\. Leitura

O Script geral de leitura é o ` ingestion.py `

### 2\. Transformação

O Script geral de transformação é o ` transformation.py `

### 3\. Validação

O Script geral de Validação é o ` validation.py `

### 4\. Carga

O Script geral de leitura é o ` load.py `

- A escolha pelo formato Parquet não é aleatória. É uma escolha popular de armazenamento de dados em pipelines de engenharia de dados por ser um formato colunar e altamente otimizado para grandes volumes de dados. Oferecendo vantagens como:  
1. Eficiência: Armazena dados de forma compactada e eficiente, reduzindo o espaço necessário
2. Desempenho em Leitura e Processamento: Ele permite a leitura seletiva de colunas, o que acelera operações de consulta
3. Compatibilidade com Ferramentas Big Data: Suportado em ferramentas como Apache Spark, Hive, Hadoop, AWS Athena e BigQuery
4. Tipagem Rígida: Oferece tipagem de dados, o que ajuda a garantir consistência e integridade nos dados 

## 5\. Outras Funções

` utils.py ` funções para logs, configs, etc...
` run_pipeline.py ` script principal de orquestração


A abordagem segue uma lógica que prioriza consistência e rastreabilidade.

## Contexto

Vamos assumir como origem uma API REST pública que entrega dados em formato JSON. Cada chamada retorna uma lista de objetos estruturados, representando registros de usuários. A estrutura é a seguinte:

id: identificador numérico único  
nome: nome completo  
email: email do usuário  
telefone: idade do usuário
website: site ou URL pessoal

Vamos salvar esse arquivo e processa-lo automaticamente, realizando as etapas acima. O objetivo é que o arquivo final, esteja livre de inconsistências.

* Nenhum campo pode estar vazio
* O campo idade deve conter um valor numérico válido
* Os registros com falhas devem ser descartados automaticamente sem comprometer a carga dos dados válidos
* Apenas os dados íntegros devem ser persistidos na base

## Tecnologias

* Python
* Pandas
* json
* Parquet
* APIs

## Arquitetura da Solução

1. Automatizar a chamada à API
2. Validar as respostas e salvar em um DataFrame
3. Aplicar filtros e Verificações
4. Conversão de tipos com segurança
5. Armazenar o resultado no formato Parquet
6. Log de execução e verificação da integridade

Cada um é um bloco isolado para garantir modularidade e escalabilidade. Pensando também, em auditorias fáceis de se realizar.


## Código Principal

` run\_pipeline.py  `

## Formas de executar automaticamente

1. CronJob ou Agendador de Tarefas (Task Scheduler)
2. Apache Airflow ou GitHub Actions

## Boas Práticas Adotadas nesse Pipeline

- Modularizar cada etapa do pipeline com funções independentes
- Validar os campos, antes da transformação
- A mesma execução irá gerar os mesmos resultados
- Utilizar logs para rastrear volume total, descartes e registros persistidos
- Caminhos dinâmicos para evitar hardcoded

## Expansões

- Detectar e armazenar registros inválidos em uma tabela separada
- Enviar alertas por e-mail em caso de alta taxa de erro
- Inserir apenas novos registros com base em comparação de IDs

## Performance

Caso seja uma base muito grande de registros, adote passos como:
- Utilizar leitura em chunks
- Utilizar métodos vetorizados sempre que possível
- Fazer persistência em lote com transações controladas
- Evitar operações inplace e preferir atribuições diretas
