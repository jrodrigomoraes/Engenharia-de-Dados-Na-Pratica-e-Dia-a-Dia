## Situação Comum 1

Uma circunstância comum na vida de um engenheiro de dados é: Fazer a ingestão de dados(muitas vezes arquivos csv) para o SQL.

Entretanto, apesar de parecer simples, algumas etapas precisam ser seguidas para tudo ocorrer bem.

### 1\. Leitura

### 2\. Transformação

### 3\. Validação

### 4\. Carga

A abordagem segue uma lógica que prioriza consistência e rastreabilidade.

## Contexto

Temos uma aplicação que recebe diariamente um arquivo com dados de usuários provenientes de uma operação externa. O arquivo contém as colunas
id: identificador do usuário
nome: nome completo
email: email do usuário
idade: idade do usuário

Vamos salvar esse arquivo e processa-lo automaticamente, realizando as etapas acima. O objetivo é que o arquivo final, esteja livre de inconsistências.

* Nenhum campo pode estar vazio
* O campo idade deve conter um valor numérico válido
* Os registros com falhas devem ser descartados automaticamente sem comprometer a carga dos dados válidos
* Apenas os dados íntegros devem ser persistidos na base

## Tecnologias

* Python
* Pandas
* SQL

## Arquitetura da Solução

1. Leitura do arquivo CSV
2. Identificação e descarte de registros inválidos
3. Validação semântica dos campos
4. Conversão de tipos com segurança
5. Carga dos dados válidos
6. Log de execução e verificação da integridade

Cada um é um bloco isolado para garantir modularidade e escalabilidade. Pensando também, em auditorias fáceis de se realizar.





\## Código Principal

` run\_pipeline.py  `



\## Formas de executar automaticamente



1. CronJob ou Agendador de Tarefas (Task Scheduler)
2. Apache Airflow ou GitHub Actions
