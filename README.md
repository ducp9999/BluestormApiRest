# Rest API - Banco de Dados SQLite Servindo informações via Python e Flask

Este projeto tem por objetivo, disponibilizar informações de clientes fictícios de uma rede de farmácias atravéz de uma API privada, protegida por senha.

## 🚀 Informações Técnicas

Esta Rest API foi escrita em Python, está utilizando o framework Flask e as bibliotecas Pandas, PyOdbc, Requests e bCrypt.

Server.py é a Rest API propriamente dita.

backend_test.db é um banco de dados SQLite que contém todas as informações.

Client.py são funções que utilizam requisições request para testar e exemplificar as diferentes formas de uso e acesso aos dados.


### 📋 Pré-requisitos

Estas bibliotecas e interpretadores podem ser instalados em diversas plataformas: Servidores Linux, servidores Windows, desktops Linux, Windows e Mac. Ou seja qualquer hardware capaz de executar versões recentes destes intermpretadores, bibliotecas e um navegador de Internet moderno, conseguirá executar os códigos deste GitHub.

De que coisas você precisa para instalar o software e como instalá-lo?

Python 3 e as bibliotecas utilizadas (Flask, Pandas, PyOdbc, Requests e bCrypt). Cada sistema operacional tem pequenas variações nos comandos de instalação.

### 🔧 Instalação

Python, siga as instruções de intalação para o seu sistema operacional no www.python.org/downloads

Após a instalação do Python use o compando pip para instalar as bibliotecas:

pip install flask
pip install bcrypt
pip install pandas
pip install pyodbc
pip install requests

## ⚙️ Executando o Server.py

O server.py pode ser executado tanto da linha de comando "python server.py" como de dentro de seu editor preferido. Será exibido um link para ser usado em um navegador de Internet ou nos comandos request. Por padrão será utilizada a porta 5000 

Agora já pode testar os endpoints

## ⚙️ Criptografia das Senhas

As senhas são gravadas no banco de dados já criptografadas, mesmo que tenha acesso ao banco de dados e veja a senha gravada, não conseguirá usar a senha gravada para fazer pesquisas. Esta atitude de criptografar senhas são classificadas como "Boas Práticas" para proteção de dados.

Para proteger a senha durante as operações de pesquisa "requests" é importante que o acesso se dê atravéz de um https (site seguro) e não através de um http (este só deve ser usado em ambiente de desenvolvimento interno)

## ⚙️ Endpoint patients

Neste endpoint obterá as informações relacionadas aos pacientes

Este endpoint (todos eles) exigem autenticação. Já existe usuário Du, com ID USER0001 e senha 123456 para teste. Mas logo abaixo descreverei o endpoint usado para criar um novo usuário para utilizar a API.

Esta endpoint pode ser usada sem argumento adicional para obter um dicionário json com todos os pacientes, e ou pode ser usada fornecendo ID do paciente desejado.

Para obter o dicionário completo:
localhost:5000/patients?chave=USER0001&senha=123456

Para obter o paciente de código 0015
localhost:5000/patients?chave=USER0001&senha=123456&codigo=PATIENT0015

## ⚙️ Endpoint pharmacies

Neste endpoint obterá as informações relacionadas às farmácias

Este endpoint (todos eles) exigem autenticação. Já existe usuário Du, com ID USER0001 e senha 123456 para teste. Mas logo abaixo descreverei o endpoint usado para criar um novo usuário.

Esta endpoint pode ser usada sem argumento adicional para obter um dicionário json com todos as farmácias, e ou pode ser usada fornecendo ID da farmácia desejada.

Para obter o dicionário completo:
localhost:5000/pharmacies?chave=USER0001&senha=123456

Para obter a farmácia de código 0008
localhost:5000/pharmacies?chave=USER0001&senha=123456&codigo=PHARM0008

## ⚙️ Endpoint transactions

Neste endpoint obterá as informações relacionadas às transações financeiras dos pacientes junto às farmácias

Este endpoint (todos eles) exigem autenticação. Já existe usuário Du, com ID USER0001 e senha 123456 para teste. Mas logo abaixo descreverei o endpoint usado para criar um novo usuário.

Esta endpoint pode ser usada sem argumento adicional para obter um dicionário json com os dados de todas as transações, informações já combinadas (inner join) com as tabelas Dimension auxiliares. Este endpoint pode ser usado de forma mais flexível, permitindo filtros por código da Transação ou filtros combinados de Primeiro Nome, Sobrenome e Cidade (qualquer combinação destes 3 campos).

Para obter o dicionário completo:
localhost:5000/transactions?chave=USER0001&senha=123456

Para obter a transação de código 0003
localhost:5000/transactions?chave=USER0001&senha=123456&codigo=TRAN0003

Para obter as transações do paciente CRISTIANO TEIXEIRA
localhost:5000/transactions?chave=USER0001&senha=123456&nome=CRISTIANO&sobrenome=TEIXEIRA

Para obter as transação dos pacientes sobrenome TEIXEIRA na cidade de CAMPINAS
localhost:5000/transactions?chave=USER0001&senha=123456&sobrenome=TEIXEIRA&cidade=CAMPINAS

## ⚙️ Endpoint create

Este endpoint será usado para criar novos Usuários para acessar a API

Irá fornecer 2 informações nome do usuário (uma palavra) e senha.

Esta senha será criptografada antes de ser gravada no banco de dados.

Este endpoit retornará um ID de usuário. Este ID de usuário, junto com a senha, serão usados em todos os outros endpoints para obter os dados.

Para criar o novo usário:
localhost:5000/create?user=Du&senha=123456

## ⚙️ Explorando o Client.py

O client.py contém 4 funções (uma para cada endpoint) que podem ser usadas para testar os endpoints e também como exemplos de uso de chamadas rquests para os endpoints.

Logo abaixo das definições das funções, vai encontrar exemplos de uso das diferentes formas de passar os parâmetros que desejar.

Nas funções patients e pharmacies o terceiro parâmetro patient_code e pharm_code respectivamente, são opcionais, pode passar estes argumentos ou não.

Atenção especial para a função transactions, como existem 4 parâmetros opcionais é necesário nomear estes parâmetros

transactions(user_id, user_password, trans_first_name=trans_first_name, trans_last_name=trans_last_name, trans_city=trans_city)

Observe que existem vários exemplos de chamadas destas funções.

### 🔩 Conclusão

Python, Flask e um banco de dados robusto, permitem servir grande volume de dados com segurança, e permitindo infinitas personalizações e opções de tratamento dos dados. Entregando exatamente o que o usuário precisa e ou deseja.

