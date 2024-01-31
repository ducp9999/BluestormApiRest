# importar Flask e Criptografia
from flask import Flask, request
from flask_bcrypt import Bcrypt
# importar Biblioteca Banco de Dados
import sqlite3
import pyodbc
# importar bibliotecas gerais
import pandas as pd

app = Flask(__name__) # cria o site
bcrypt = Bcrypt(app)

# Transformar mensagem e erro em um dicionário do Pandas e retornar o dicionário
def error(error_message):
    error_data = {"UUID": error_message}
    error_df = pd.DataFrame(error_data, index=[0])
    error_dic = error_df.to_dict('index')
    return error_dic

# Criar ID e criptografar a senha do novo usuário, gravar no BD e retornar o ID criado
def create_user(user_name, user_password):
    # gerar a Hash da senha para gravar a senha criptografada no BD. Boas Práticas.
    hashed_key = bcrypt.generate_password_hash(user_password).decode('utf-8') 
    dados_conexao = ("Driver={SQLite3 ODBC Driver};Server=localhost;Database=./backend_test.db")
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()
    # Verificar qual o maior ID gravado no BD
    sql_next_key = "SELECT uuid FROM users ORDER BY uuid DESC LIMIT 1;"
    cursor.execute(sql_next_key)
    dados = cursor.fetchall()
    if dados:  # Somar 1 ao maior ID
        var_next_key = int(dados[0][0][-4:]) + 1
        var_next_key = "USER{:04d}".format(var_next_key) 
    else:  # Se o BD estiver vazio, usar este ID como primeiro ID
        var_next_key = "USER0001"    
    var_sql = f'''INSERT INTO users(uuid, username, password) VALUES("{var_next_key}", "{user_name}", "{hashed_key}"); '''
    cursor.execute(var_sql)
    cursor.commit()
    cursor.close()
    conexao.close()
    return var_next_key  # Retornar o ID criado para o novo usuário.

# Verificar se a senha do usuário está correta
def verify_key(user_key, user_password):
    # Buscar Username e Password no DB
    dados_conexao = ("Driver={SQLite3 ODBC Driver};Server=localhost;Database=./backend_test.db")
    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()
    var_sql = f'''SELECT username, password FROM users WHERE uuid = "{user_key}"; '''
    cursor.execute(var_sql)
    dados = cursor.fetchall()
    if dados:  # Caso seja encontrado Usuário para o ID fornecido no request
        db_user_name = dados[0][0]
        db_user_password = dados[0][1]
        cursor.close()
        conexao.close()
        # Verificar se a senha fornecida confere com a senha Hash do BD
        is_valid = bcrypt.check_password_hash (db_user_password, user_password)
        return is_valid
    else: # Caso o ID fornecido não seja encontrado no BD, retornar falso
        return False

# Informações básicas no caso de digitarem o endereço da API em um navegador
@app.route("/") # decorator -> diz em qual link a função vai rodar
def root(): # função
    informacao = '''
        <h1 style="text-align:center">Informações Importantes</h1>
        <h2 style="text-align:center">Esta API contém informações privadas</h2>
        <p style="text-align:center">Utilize seu usuário e chave de acesso.<p>
        <p style="text-align:center">endpoints disponíveis:</p>
        <p style="text-align:center">patients</p>
        <p style="text-align:center">pharmacies</p>
        <p style="text-align:center">transactions</p>
    '''
    return informacao

# Criar novo usuário a partir do nome e senha
# localhost:5000/create?user=YYYY&senha=ZZZZ
@app.route("/create", methods=['GET']) # decorator -> diz em qual link a função vai rodar
def create(): # função
    usuario = request.args.get('user')
    senha = request.args.get('senha')

    if usuario and senha: # Caso tenham fornecido usuário e senha, criar o usuário
        # create_user(id, usuario, senha)
        var_next_key = create_user(usuario, senha)
        # Transformar novo ID em dicionário do Pandas
        users_data = {"UUID": var_next_key}
        users_df = pd.DataFrame(users_data, index=[0])
        users_dic = users_df.to_dict('index')
        return users_dic
    else: # Se não forneceram usuário ou senha, criar mensagem de erro
        return error("Informacoes incompletas")

# Consultar dados do Paciente
# localhost:5000/patients?chave=XXXX&senha=YYYY&codigo=ZZZZ código é opcional &codigo=ZZZZ
@app.route("/patients", methods=['GET']) 
def id_patient(): 
    chave = request.args.get('chave')
    senha = request.args.get('senha')
    codigo = request.args.get('codigo')
    if chave and senha: # Verificar se forneceram ID e senha do usuário
        if verify_key(chave, senha):
            if codigo: # Verificar se forneceram ID de algum paciente específico
                var_sql = f'''SELECT * FROM patients WHERE uuid = "{codigo}" '''
            else: # Opção de consultar todos os pacientes
                var_sql = f'''SELECT * FROM patients'''    
            db_cnx = sqlite3.connect("./backend_test.db")
            df_patients = pd.read_sql_query(var_sql, db_cnx, index_col=None)
            print(df_patients)    
            dic_patients = df_patients.to_dict('index')
            # print(dic_patients)
            if dic_patients: # Caso o paciente tenha sido encontrado no BD
                return dic_patients
            else: # Mensagem de Erro - Paciente não encontrado
                return error("Inexistente")
        else: # Mensagem de erro para falha na autenticação do usuário
            return error("Falha na Autenticacao")

# Consultar os dados das Farmácias
# localhost:5000/pharmacies?chave=XXXX&senha=YYYY&codigo=ZZZZ código é opcional &codigo=ZZZZ
@app.route("/pharmacies", methods=['GET']) 
def id_pharmacies(): 
    chave = request.args.get('chave')
    senha = request.args.get('senha')
    codigo = request.args.get('codigo')
    if chave and senha: # Vericar se foram fornecidos ID e senha do usuário
        if codigo: # Verificar se foi fornecido ID de uma Farmácia específica
            var_sql = f'''SELECT * FROM pharmacies WHERE uuid = "{codigo}" '''
        else:  # Opção para consultar todas as farmácias
            var_sql = f'''SELECT * FROM pharmacies '''    
        if verify_key(chave, senha): # Vericar se ID e senha fornecidos estão corretos
            db_cnx = sqlite3.connect("./backend_test.db")
            df_pharmacies = pd.read_sql_query(var_sql, db_cnx, index_col=None)
            print(df_pharmacies)    
            dic_pharmacies = df_pharmacies.to_dict('index')
            # print(dic_pharmacies)
            if dic_pharmacies: # Caso a Farmácia desejada tenha sido encontrada
                return dic_pharmacies
            else: # Mesnagem de erro, farmácia não encontrada no BD
                return error("Inexistente")
        else: # Mensagem de erro, ID e senha do usuário não são válidos
            return error("Falha na Autenticacao")
    else: # Mensagem de erro ID ou senha do usuário não fornecidos
        return error("Falha na Autenticacao")
    
# Consultar os dados da Transação
# localhost:5000/transactions?chave=XXXX&senha=YYYY&codigo=ZZZZ&nome=AAAA&sobrenome=BBBB&cidade=CCCC 
# código, nome, sobrenome, cidade são opcionais &codigo=ZZZZ&nome=AAAA&sobrenome=BBBB&cidade=CCCC
# no caso de não usar o código, pode combinar nome, sobrenome e cidade da forma que desejar    
@app.route("/transactions", methods=['GET']) 
def id_transactions(): 
    chave = request.args.get('chave')
    senha = request.args.get('senha')
    codigo = request.args.get('codigo')
    nome = request.args.get('nome')
    sobrenome = request.args.get('sobrenome')
    cidade = request.args.get('cidade')
    if chave and senha: # Vericar se foram fornecidos ID e senha do usuário
        if verify_key(chave, senha): # Verificar se ID e senha do usuário estão corretos
            if codigo: # Verificar se for fornecido código de uma transação específica   
                var_sql = f'''SELECT
                                transactions.patient_uuid,
                                patients.first_name,
                                patients.last_name,
                                patients.date_of_birth,
                                transactions.pharmacy_uuid,
                                pharmacies.name,
                                pharmacies.city,
                                transactions.uuid,
                                transactions.amount,
                                transactions.timestamp
                            FROM transactions
                            INNER JOIN patients ON transactions.patient_uuid = patients.uuid
                            INNER JOIN pharmacies ON transactions.pharmacy_uuid = pharmacies.uuid
                            WHERE transactions.uuid = "{codigo}"
                            '''

            else: # Opção para consultar todos as transações
                var_sql = f'''SELECT
                                transactions.patient_uuid,
                                patients.first_name,
                                patients.last_name,
                                patients.date_of_birth,
                                transactions.pharmacy_uuid,
                                pharmacies.name,
                                pharmacies.city,
                                transactions.uuid,
                                transactions.amount,
                                transactions.timestamp
                            FROM transactions
                            INNER JOIN patients ON transactions.patient_uuid = patients.uuid
                            INNER JOIN pharmacies ON transactions.pharmacy_uuid = pharmacies.uuid
                            '''
                if nome: # Opção de filtrar também pelo nome
                    if "WHERE" not in var_sql:
                        var_sql += f''' WHERE patients.first_name = "{nome}"'''
                    else:    
                        var_sql += f''' AND patients.first_name = "{nome}"'''
                if sobrenome: # Opção de filtrar também pelo sobrenome
                    if "WHERE" not in var_sql:
                        var_sql += f''' WHERE patients.last_name = "{sobrenome}"'''
                    else:    
                        var_sql += f''' AND patients.last_name = "{sobrenome}"'''
                if cidade: # Opção de filtrar também pela cidade
                    if "WHERE" not in var_sql:
                        var_sql += f''' WHERE pharmacies.city = "{cidade}"'''
                    else:    
                        var_sql += f''' AND pharmacies.city = "{cidade}"'''
            db_cnx = sqlite3.connect("./backend_test.db")
            df_transactions = pd.read_sql_query(var_sql, db_cnx, index_col=None)
            print(df_transactions)    
            dic_transactions = df_transactions.to_dict('index')
            if dic_transactions: # Caso a transação desejada tenha sido encontrada
                return dic_transactions
            else: # Mensagem de erro quando a transação desejada não foi encontrada
                return error("Inexistente")
        else: # Mensagem de erro quando ID e senha do usário não estão corretos
            return error("Falha na Autenticacao")
    else: # Mensagem de erro quando ID ou senha do usário não foram fornecidos
        return error("Falha na Autenticacao")
   
app.run() #  app.run(host="0.0.0.0") 