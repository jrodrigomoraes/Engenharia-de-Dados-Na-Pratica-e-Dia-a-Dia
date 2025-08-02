## Situação Comum 3

A situação analisada envolve a transformação de dados brutos em estruturas organizadas e utilizáveis. O objetivo é tornar os dados consistentes e prontos para uso por profissionais como analistas de dados, cientistas de dados e engenheiros de machine learning. Para garantir a qualidade dessa etapa, é fundamental que a lógica do pipeline seja clara, testável e alinhada com as regras e padrões definidos pela empresa.

Neste contexto, utilizamos a biblioteca **pandas** para transformar os dados e o **boto3** para enviá-los a um *Data Lake*, como o Amazon S3. Esse tipo de operação é comum em ambientes modernos de dados.

Para que os dados cheguem até essa fase com qualidade e consistência, é necessário construir fluxos robustos que leem informações de múltiplas fontes. O formato final de armazenamento costuma ser **Parquet** ou **CSV particionado**, facilitando a escalabilidade e o consumo eficiente nas etapas seguintes do pipeline.

---

## Objetivo

- Eliminar registros com campos obrigatórios ausentes  
- Padronizar categorias  
- Criar variáveis derivadas relevantes  
- Gerar coluna "ano-mês" para particionamento futuro  
- Salvar em formato **Parquet**  
- Enviar os dados processados para o **Amazon S3** ou **Google Cloud Storage**

---

## Estrutura dos Dados

A seguir, os campos presentes no conjunto de dados utilizado:

- `id_transacao`: identificador numérico único  
- `valor`: valor da transação em reais  
- `categoria`: rótulo da transação  
- `data`: data da transação  
- `id_cliente`: identificador único do cliente  

---

## O Pipeline em Passos

1. Carrega os dados brutos a partir de arquivos **CSV**  
2. Aplica transformações utilizando a biblioteca **pandas**  
3. Enriquece os dados com base em regras de negócio  
4. Converte o resultado final para o formato **Parquet**  
   - *(As vantagens do Parquet são discutidas no Pipeline 2)*  
5. Envia o arquivo final para um bucket na nuvem (ex: **Amazon S3**)

---

## Arquitetura da Solução

- **Entrada**: Arquivos CSV contendo os dados brutos  
- **Transformação**: Uso de **pandas** para limpeza e enriquecimento  
- **Validação**: Regras de negócio aplicadas com lógica customizada  
- **Formato de saída**: Arquivo **Parquet**, otimizado para leitura e compressão  
- **Destino**: Envio para **Amazon S3** via **boto3** (Também podia ser o GCS via gcsfs)  
- **Logs & Observabilidade**: Registro de logs locais e tratamento de erros  

> Cada etapa do pipeline foi estruturada como um bloco isolado, garantindo **modularidade**, **escalabilidade** e facilitando processos de **auditoria e rastreabilidade**.

---

## Scripts Principais

- `ingestion.py` – Leitura dos dados brutos  
- `transformation.py` – Aplicação de regras e transformação dos dados  
- `validation.py` – Validação e checagem de integridade  
- `load.py` – Carga final dos dados no destino (S3)  
- `utils.py` – Funções auxiliares para logs, configuração, etc.  
- `run_pipeline.py` – Script principal de orquestração

---

## Tecnologias Utilizadas

- Python  
- pandas  
- boto3  
- CSV  
- Parquet  
- Amazon S3 / Google Cloud Storage (GCS)

---

## Automação da Execução

O pipeline pode ser executado automaticamente utilizando:

1. **CronJob** (Linux) ou **Agendador de Tarefas** (Windows)  
2. Orquestradores como **Apache Airflow** ou **GitHub Actions**

---


## Boas Práticas Adotadas nesse Pipeline

- Modularizar cada etapa do pipeline com funções independentes e tratamento dos dados
- Validar os campos, antes da transformação
- Saída com formato compatível com os objetivos do Pipeline, ou seja, garantir consistência de Schema
- Utilizar logs para rastrear volume total e status
- Trabalhar com datetime em formato nativo do pandas
- Controle de credenciais
- Manter nomes de arquivos padronizados com data ou partição

---

## Expansões

- Tarefas de Enriquecimento com dados externos (via merge)
- Criação de partições por data no Parquet
- Publicação automática em data lake, S3 ou GCP
- Agendamento com orquestradores como Apache Airflow

---

## Conclusão

A transformação de dados com Pandas e o envio para um data lake unem a preparação analítica à arquitetura distribuída. O pipeline aplica limpeza, enriquecimento e formatação antes da entrega para consumo em larga escala. O uso do formato Parquet e das bibliotecas boto3 ou gcsfs garante compatibilidade com a nuvem, enquanto validações asseguram a confiabilidade dos dados. Dominar essas técnicas é essencial para engenheiros de dados em ambientes produtivos.
