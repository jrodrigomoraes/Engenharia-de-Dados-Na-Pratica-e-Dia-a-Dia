# Logs do Pipeline

## Importância do arquivo de log

O arquivo `pipeline.log` é essencial para auditar e rastrear o andamento do pipeline de dados. Abaixo, estão descritas as diferentes utilidades do log, dependendo do contexto de execução:

### 1. **No contexto de teste ou simulação**
Embora não utilizemos dados reais ou sistemas externos, o arquivo de log **ainda é gerado** para simular o comportamento real do pipeline. Esse log serve como uma verificação básica para garantir que o processo de execução do pipeline está ocorrendo conforme o esperado, mesmo sem dados reais.

- O arquivo `pipeline.log` será gerado sempre que o pipeline for executado.
- Mensagens de **info**, **erro** e **aviso** (como `logger.info()`, `logger.error()`, etc.) serão registradas para simular o comportamento do pipeline.
- Mesmo sem dados reais, você pode verificar o log para garantir que o processo está sendo seguido corretamente, como a leitura, transformação e armazenamento dos dados.

### 2. **No contexto de produção**
Em um ambiente de produção, o log **se torna crítico** para a monitoração e rastreabilidade do pipeline de dados:

- **Auditoria**: O log permite revisar o processo e verificar se os dados foram processados corretamente.
- **Detecção de falhas**: O log ajudará a identificar rapidamente falhas no pipeline (como problemas de conexão com a API, dados inconsistentes ou falhas de transformação).
- **Monitoramento em tempo real**: Durante a execução do pipeline, as mensagens de log podem ser usadas para monitorar a performance e andamento da ingestão de dados. Por exemplo, se o pipeline está demorando demais ou se um número incomum de registros foi rejeitado.
- **Alertas**: Em um ambiente de produção, é possível configurar alertas automáticos para enviar notificações caso erros críticos ocorram (por exemplo, via **Slack**, **email**, ou **sistemas de monitoramento** como **Prometheus**).

### 3. **Formato do Log**
O arquivo `pipeline.log` usa o formato de log **com timestamps** para cada evento:

YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE

`
Exemplo:
2025-07-16 10:00:00 - INFO - Início do pipeline
2025-07-16 10:05:00 - ERROR - Falha ao conectar com a API
2025-07-16 10:10:00 - INFO - Total de registros processados: 1000
`


### 4. **Análise do Log**
Em uma situação de produção, a análise do log pode ser feita de várias formas:
- **Logs localizados**: Como o arquivo `pipeline.log` é gerado localmente, ele pode ser consultado manualmente ou integrado a ferramentas de visualização (ex: ELK Stack).
- **Ferramentas de monitoramento**: Em ambientes mais avançados, podemos configurar o log para ser enviado para ferramentas como **Splunk**, **Graylog** ou **Datadog**, para rastrear o pipeline em tempo real e receber alertas de erros e falhas.

---

### Conclusão

Mesmo em um ambiente de simulação, a criação de logs ajuda a validar o funcionamento do pipeline e a garantir que a execução ocorre conforme esperado. No entanto, quando em produção, o log assume um papel mais robusto, permitindo a auditoria completa do processo, detectando falhas em tempo real e facilitando a análise dos dados processados.

