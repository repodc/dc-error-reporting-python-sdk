# dc_error_reporting_python_sdk
SDK para integrar o sistema de alerta de erros com Python

O sistema irá notificar os analistas da DC

## Instalação

   1. Usando o pip, adicione a seguinte linha no final do arquivo **requirements.txt**:
      
      ```
      git+https://github.com/repodc/dc_error_reporting_python_sdk.git
      ```
  2. Execute o comando pip install -r requirements.txt para instalar a dependência

  Na necessidade de atualizar o pacote, rode o seguinte comando:
  
  ```
  pip install --upgrade git+https://github.com/repodc/dc_error_reporting_python_sdk.git
  ```
   

## Passo a Passo para Integrar com Python (Flask)

1. Variáveis de ambiente (dump.py)

   É necessário adicionar o seguinte objeto no arquivo **kernel/dump.py**:
   ```python
     error_reporting = {
        "APP_ENV": "homologation", # Se o valor for "local" não será enviado as notificações
        "DC_ERROR_REPORTING_TOKEN": "token_de_acesso" # Pegue o token de acesso com o staff da DC
    }
   ```

   **IMPORTANTE:** durante o desenvolvimento local sempre deixe o valor de **APP_ENV** igual à **"local"** para não enviar notificações ao ocorrer erros.
   

2. Adicionar error handler no projeto

   No projeto Flask crie um error handler no arquivo principal (geralmente é o **app.py**) e utilize a classe **DcErrorReportingSdk**:

   ```python
    from dc_error_reporting_python_sdk.DcErrorReportingSdk import DcErrorReportingSdk
   
    @app.errorhandler(Exception)
    def handle_error(error):
        dc_error_reporting = DcErrorReportingSdk('Nome do Sistema', memory.error_reporting["APP_ENV"], memory.error_reporting["DC_ERROR_REPORTING_TOKEN"])
        dc_error_reporting.send(error, request.url)
   ```

   Ao instanciar a classe **DcErrorReportingSdk** informe o nome do sistema corretamente no primeiro parâmetro.
   Observe que o segundo parâmetro do método **send()** é a url requesitada, esse parâmetro é opcional mas é recomendado sempre incluir ele.

4. Caso haja a necessidade de reportar erros que estão contidos em um bloco de **try ... except** basta instanciar a classe novamente, ou importar de algum modulo/contexto global

   ```python
    try:
      # código...

    except Exception as e:
      dc_error_reporting.send(error, request.url)
    
      # tratamento do erro
   ```


E é isso, após configurado, qualquer erro / exceção não tratado pelo sistema será notificado aos analistas da DC

## Visualizar log de erros

Para acessar o log com os erros ocorridos, visite a url https://dc-error-reporting.dctec.dev/api/error_report/slug-sistema

Substitua slug-sistema pelo nome do sistema no formato slug (letras minúsculas, sem caracteres especiais e substituindo espaço por "-")

Exemplo: o nome do sistema é **Bablepet ERP (API)** então o slug ficará **bablepet-erp-api**

## Testes

Ao realizar os testes do SDK durante o desenvolvimento, altere o valor da variável de ambiente **APP_ENV** para "test":

Dessa forma nenhum analista será notificado quando houver erro, mas o log do erro aparecerá em https://dc-error-reporting.dctec.dev/api/error_report/slug-sistema/test

Note que ao final da url foi adicionado o **/test**, neste endpoint será mostrado apenas os erros do ambiente de teste.
