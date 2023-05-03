## 🧑 HUBLA

## Tecnologias e bibliotecas
- [Python] - https://www.python.org
- [Django] - https://www.djangoproject.com
- [Bootstrap] - https://getbootstrap.com
- [ReactJS] - https://react.dev
- [MySql] - https://www.mysql.com/

## Instalação Backend
Para instalar o projeto e preparar seu ambiente, execute os comandos abaixo:

1. Dentro da pasta /backend use o comando `python -m venv venv` para criar o ambiente virtual.
2. Depois utilize o comando `pip install -r requirements.txt` para instalar as depedências no ambiente.
3. Utilize o comando `python env_gen.py` para gerar o .env.

## Banco de dados
O banco de dados precisa ser criado ser manualmente:

1. Criar o banco compatível com as configurações do .env
2. Após a criação do banco Utilize o comando `python manage.py migrate` para gerar as migrações.
5. Suba o servidor usando o comando `python manage.py runserver`.

## Instalação Frontend
1. No diretório /frontend use o comando `npm install` para instalar as dependências.
2. Após a instalação utilize o comando `npm run dev` para subir o servidor de do cliente.

## Responsabilidades
Em sua raíz, o projeto contém uma separação básica entre frontend e backend.

```
Frontend: Todos os arquivos necessários para a devida apresentação dos dados ao usuário. Vale lembrar que, o frontend não possui regras de negócio, sendo responsável apenas por consultar o backend, interpretar os dados e apresentar as informações consolidadas.
```
```
Backend: No quesito processamento e interação com o banco de dados, essa pasta conterá todos os arquivos responsáveis pela lógica da aplicação, inclusive, responsável por saber como receber todas as requisições do frontend e devolver num formato especifico e esperado.
```

# Fluxo dos dados
Primeiro passo que precisamos entender é sobre o fluxo dentro do sistema, como os dados se integram e como chegar no resultado esperado.

1.  A primeira tela exigirá um usuário e senha, basta informá-los para que tenha acesso ao sistema. = `login/`
2.  Caso ainda não possua um cadastro, poderá ser feito um cadastro através do link disponibilizado no formulário de login. = `register/`
3.  Uma vez logado, será feito o redirecionamento para a tela de upload de um novo contrato. = `contract/`
4.  Na tela de upload de um novo contrato, deverá ser feita a seleção de um arquivo válido e então basta clicar no botão de envio para que seja feito o cadastro no banco de dados. **"Um ponto muito importante, nesse momento, o contrato ainda não foi processado, ele foi apenas armazenado e ficará como pendente, até que o processador consiga executá-lo e gerar as transações."**
5.  Após cadastrar um contrato, será feito o redirecionamento para uma tela contendo todos os contratos salvos e seus respectivos estados, podendo ser: **PENDENTE, PROCESSANDO, FINALIZADO**. = `contract/list`
6.  Quando o contrato é processado, habilita-se um link na última coluna da listagem de contratos para que seja possível visualizar os detalhes das transações e os montantes finais. = `contract/<int:pk>`

## Processamento assíncrono
Como todos sabemos, fazer o processamento de um arquivo pode ser demorado ou pode ser rápido. Porém, é muito normal nesses cenários, utilizarmos a abordagem de fazer isso assíncronamente, ou seja, o processamento é feito em um segundo momento e não impacta no uso do sistema por parte do usuário.

Foi tomada em conta essa abordagem, sendo os arquivos responsáveis:
- https://github.com/BrunoAlz/Hubla-Transactions/blob/master/backend/api/core/management/commands/call_data_processor.py
- https://github.com/BrunoAlz/Hubla-Transactions/blob/master/backend/api/core/management/commands/get_bd_data.py


A fim de separar as responsabilidades, foram criados dois comandos, sendo: `call_data_processor` e `get_bd_data`. 

Para utilizar os comandos é necessário estar no mesmo nível hierarquico do arquivo `manage.py`. 

Para processar os dados basta utilizar o comando `python manage.py get_bd_data`.

- `get_bd_data`: responsável por buscar todos os contratos pendentes no banco de dados e enviar para o outro comando executar. Caso não existam contratos pendentes, será exibida a seguinte mensagem:
    ```
    There are no transactions to be processed
    ```
- `call_data_processor`: responsável por ler cada linha do contrato, interpretar aquela transação e então consolidar os dados para gerar um relatório no final.
    ```
    Finished processing
    # or 
    Processing error
    ```

> Ambos comandos, segundo a própria documentação do framework , podem ser executados por exemplo a partir do terminal, ou seja, podem existir diferentes tipos de gatilhos para que isso ocorra (ex: cron ou alguma tarefa agendada).

### Testes unitários
Para realizar os testes unitários, é necessário entrar na pasta backend, no mesmo nível hierarquico do arquivo `manage.py`. 
e rodar o comando `pytest` para resultados simples e `pytest --cov` para o coverage.
```

api\tests\constants.py               16      0   100%
api\tests\transactions\tests.py     100      3    97%   157-159
api\tests\user\tests.py              90      0   100%
api\transactions\models.py           56      7    88%   47, 133, 136-138, 141-142
api\transactions\serializers.py      43      5    88%   20-23, 113
api\transactions\views.py            41      9    78%   36-44, 96, 101
api\user\authentication.py           30      6    80%   44-47, 52-53
api\user\models.py                   53     18    66%   19-20, 26, 29, 35, 50-63, 96, 99    
api\user\serializers.py              31      1    97%   46
api\user\views.py                    25      0   100%

```

### Exemplo de como executar o comando para processar os contratos pendentes:
```
python manage.py get_bd_data
```

### Exemplo de um `JSON` do relatório gerado após o processamento de um contrato:
```json
[{
	"person": "ELIANA_NOGUEIRA",
	"product": "DESENVOLVEDOR_FULL_STACK",
	"total_sold_by_producer": 465000,
	"total_sold_by_affiliate": 465000,
	"total_commission_paid": 150000,
	"gross_total": 930000,
	"liquid": 780000,
	"affiliates": {
		"CARLOS_BATISTA": 50000,
		"CAROLINA_MACHADO": 50000,
		"CELSO_DE_MELO": 50000
	}
}]
```

### Exemplo de uma transação
```
12022-01-15T19:20:30-03:00CURSO DE BEM-ESTAR            0000012750JOSE CARLOS
```

### Como os dados são extraídos
Na documentação de entrada, existe um demonstrativo do tamanho de cada campo dentro de um contrato, ou seja, foi delimitado o número de caracteres para que pudesse ser feita a extração, sendo assim, foi seguida a seguinte lógica na obtenção dos dados:

https://github.com/BrunoAlz/Hubla-Transactions/blob/master/backend/api/core/management/commands/call_data_processor.py#L99

```python
type_id = validate_type_id(line[0])
type = self.get_cached_type(type_id)
date = validate_date_format(line[1:26])
product = validate_product(line[26:56])
price = validate_price(line[56:66])
seller = validate_seller(line[66:86])
```
-  Para cada campo, existe uma validação em específica, e suas regras, estão contidas em:
https://github.com/BrunoAlz/Hubla-Transactions/blob/master/backend/api/core/management/commands/data_validate.py
