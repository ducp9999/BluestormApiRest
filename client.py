# API
import requests

def new_user(user_name, user_password):
    var_url = 'http://localhost:5000/create'
    if user_name and user_password :
        var_url += f'?user={user_name}&senha={user_password}'
    users = requests.get(var_url)
    users_dic = users.json()
    return users_dic

def patients(user_id, user_password, patient_code=''):
    var_url = 'http://localhost:5000/patients'
    if user_id and user_password :
        var_url += f'?chave={user_id}&senha={user_password}'
        if patient_code:
            var_url += f'&codigo={patient_code}' 
    patients = requests.get(var_url)
    patients_dic = patients.json()
    return patients_dic

def pharmacies(user_id, user_password, pharm_code=''):
    var_url = 'http://localhost:5000/pharmacies'
    if user_id and user_password :
        var_url += f'?chave={user_id}&senha={user_password}'
        if pharm_code:
            var_url += f'&codigo={pharm_code}' 
    pharmacies = requests.get(var_url)
    pharmacies_dic = pharmacies.json()
    return pharmacies_dic

def transactions(user_id, user_password, trans_code='', trans_first_name='', trans_last_name='', trans_city=''):
    var_url = 'http://localhost:5000/transactions'
    if user_id and user_password :
        var_url += f'?chave={user_id}&senha={user_password}'
        if trans_code:
            var_url += f'&codigo={trans_code}' 
        if trans_first_name:
            var_url += f'&nome={trans_first_name}' 
        if trans_last_name:
            var_url += f'&sobrenome={trans_last_name}' 
        if trans_city:
            var_url += f'&cidade={trans_city}' 
    transactions = requests.get(var_url)
    transactions_dic = transactions.json()
    return transactions_dic

user_id = "USER0001"
user_password = "123456"
patient_code = "PATIENT0015"
pharm_code = "PHARM0008"
trans_code = "TRAN0003"

# Filtros Extras para Pesquisa de transações
trans_first_name = "CRISTIANO"
trans_last_name = "TEIXEIRA"
trans_city = "CAMPINAS"

# Consultar Pacientes ( totos ou código específico )
print(patients(user_id, user_password))
# print(patients(user_id, user_password, patient_code))

# Consultar Farmácia ( todas ou código específico )
# print(pharmacies(user_id, user_password))
# print(pharmacies(user_id, user_password, pharm_code))

# Consultar transação ( todas ou código específico )
# print(transactions(user_id, user_password))
# ID da Transação é um argumento opicional da função. Mas como é o primeiro argumento opcional pode ser passado sem referencial o nome do argumento
# print(transactions(user_id, user_password, trans_code)) # sem o nome do arqumento
# print(transactions(user_id, user_password, trans_code=trans_code)) # com o nome do argumento
# Os outros argumentos opcionais da função que estão mais à direita, precisam ser referenciados com o nome do argumento
# print(transactions(user_id, user_password, trans_first_name=trans_first_name)) # passar o primeiro nome com o nome do argumento
# print(transactions(user_id, user_password, trans_last_name=trans_last_name)) # passar o sobrenome com o nome do argumento
# print(transactions(user_id, user_password, trans_city=trans_city)) # passar a cidade com o nome do argumento
# print(transactions(user_id, user_password, trans_last_name=trans_last_name, trans_city=trans_city)) # exemplo de combinação de sobrenome e nome da cidade

# Criar Usuário -- Esta função retorna o ID atribuído ao novo usuário
# print(new_user("Du", "123456"))
