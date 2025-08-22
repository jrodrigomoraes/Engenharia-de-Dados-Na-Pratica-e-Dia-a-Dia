## Situação Comum 4

A situação analisada neste pipeline é a necessidade comum de coletar, organizar e armazenar logs de sistemas de forma estruturada. Logs são fontes essenciais de informações para auditoria, troubleshooting e monitoramento de aplicações. No entanto, por serem geralmente gerados em formatos não estruturados (como texto simples), é necessário aplicar transformações que tornem seu conteúdo acessível e útil para análises mais aprofundadas.

Neste contexto, utilizamos a biblioteca Python (com regex e pandas) para realizar o parsing dos logs e estruturar as informações. Após a transformação, os dados são validados e salvos em formato Parquet particionado, facilitando o armazenamento e a consulta futura. Para o envio ao repositório final, utilizamos a boto3 para integração com o Amazon S3 (ou outra solução de armazenamento em nuvem, como o Google Cloud Storage).

Esse tipo de processo é comum em times de observabilidade, engenharia de dados e segurança, que precisam capturar dados de logs em tempo quase real e organizá-los de forma eficiente.

---

## Objetivo

- Coletar logs gerados por aplicações, servidores ou containers
- Aplicar parsing e extrair campos relevantes (timestamp, nível do log, mensagem, etc.)
- Validar dados críticos e descartar entradas incompletas ou corrompidas 
- Padronizar o formato dos dados (ex: campos como level, event, user_id)
- Criar coluna de ano-mês-dia a partir do timestamp para particionamento 
- Armazenar os dados processados em Parquet particionado
- Enviar os arquivos organizados para o Amazon S3 ou outro Data Lake compatível

---

## Estrutura dos Dados

A seguir, os campos presentes no conjunto de dados utilizado:
- `timestamp`: data e hora do evento registrado
- `level`: nível do log (ex: INFO, WARNING, ERROR)
- `service`: nome do serviço ou aplicação que gerou o log
- `message`: mensagem principal do log
- `user_id`: identificador do usuário
- `host`: máquina ou container que originou o log
---

## O Pipeline em Passos

1. Coleta logs brutos de arquivos .log ou .txt em diretórios definidos
2. Aplica parsing das linhas utilizando expressões regulares ou lógica personalizada
3. Transforma os logs em estrutura tabular utilizando pandas
4. Aplica validações básicas para garantir a integridade e consistência dos dados
5. Gera coluna ano-mês-dia para particionamento e salva em Parquet
6. Envia os arquivos processados para o Amazon S3 via boto3
7. Utiliza o Apache Airflow para orquestrar e agendar o pipeline

---

## Arquitetura da Solução

- **Entrada**: Arquivos de log (.log ou .txt) contendo eventos em texto 
- **Transformação**: Parsing e formatação com Python + pandas 
- **Validação**: Regras simples com lógica customizada 
- **Formato de saída**: Arquivos Parquet, organizados por data (partição ano/mês/dia) 
- **Destino**: Bucket S3 ou Data Lake local compatível (pode ser adaptado para GCS ou Azure Blob)
- **Orquestração**: Pipeline executado via Apache Airflow com DAG agendada  
- **Logs & Observabilidade**: Registro de logs locais e tratamento de erros  

> O pipeline foi projetado com foco em modularidade, permitindo fácil adaptação a diferentes formatos de log, e escalabilidade, com estrutura pronta para lidar com grandes volumes de dados. Sendo assim, o pipeline está pronto para ser executado localmente ou em produção, com adaptações simples de caminho e destino.

---

## Scripts Principais

- `ingestion.py` – Lê arquivos .log de um diretório ou endpoint configurado  
- `transformation.py` – Aplica parsing e estrutura os dados com pandas  
- `validation.py` – Validação e checagem de integridade  
- `load.py` – Carga final dos dados no destino (S3)  
- `utils.py` – Funções auxiliares: tratamento de datas, criação de diretórios, logging, etc. 
- `run_pipeline.py` – Script principal para orquestrar todas as etapas em sequência (útil fora do Airflow)
- `pipeline_coleta_logs.py`– DAG do Apache Airflow para execução programada do pipeline

---

## Tecnologias Utilizadas

- Python  
- pandas
- regex
- boto3  
- CSV  
- Parquet  
- Amazon S3 / Google Cloud Storage (GCS)
- Airflow

---

## Automação da Execução

O pipeline pode ser executado automaticamente utilizando:

1. **CronJob** (Linux) ou **Agendador de Tarefas** (Windows)  
2. Orquestradores como **Apache Airflow** ou **GitHub Actions**

---


## Boas Práticas Adotadas nesse Pipeline

- Modularização clara de cada etapa (coleta, transformação, validação, carga)
- Parsing robusto via regex ou lógica customizada, com fallback para casos fora do padrão
- Validação de campos essenciais como timestamp e level
- Geração de arquivos de saída com esquema consistente e compatível com análise
- Uso de logs para rastreamento do status de execução e volume processado
- Armazenamento de datas no formato nativo do pandas para particionamento eficiente
- Padronização de nomes de arquivos com base na data de referência
- Controle seguro de credenciais (ex: uso de variáveis de ambiente ou arquivos .env)

---

## Expansões

- Publicar logs processados em tópicos Kafka ou Pub/Sub
- Persistir em timeseries DBs como InfluxDB ou TimescaleDB
- Acoplar com dashboards para visualização contínua
- Enviar alertas em tempo real com base em padrões de erro

---

## Conclusão

A coleta e estruturação de logs é um processo essencial para garantir observabilidade e auditoria em sistemas modernos. Este pipeline transforma arquivos de log brutos em datasets estruturados, prontos para análise e armazenamento em larga escala. O uso de pandas para transformação, Parquet para persistência e boto3 para envio ao S3 cria uma solução eficiente, modular e escalável. A orquestração via Airflow garante controle e automação, enquanto as validações asseguram confiabilidade.
Esse tipo de pipeline é um alicerce fundamental para ambientes de produção orientados a dados.
