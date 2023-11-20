import requests
import logging


# TEST-ADD_USER
data = {
    'name': 'John',
    'surname': 'Doe'
}
try:
    response = requests.post('http://localhost:4000/add_user',json=data,timeout=15)
except Exception as e:
    logging.exception("error")

print(response.status_code)
print(response.json())


# TEST-GET_USERS
try:
    response_get_users = requests.get(f'http://localhost:4000/get_users', timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-GET_USERS:")
print(f"Status code: {response_get_users.status_code}")
print(f"Response: {response_get_users.json()}")


# TEST-UPDATE_USER

# Supponendo che l'utente creato nel test ADD_USER abbia ID 2
user_id_to_update = 4
data_update_user = {'name': 'UpdatedName', 'surname': 'UpdatedSurname'}
try:
    response_update_user = requests.put(f'http://localhost:4000/update_user/{user_id_to_update}', json=data_update_user, timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-UPDATE_USER:")
print(f"Status code: {response_update_user.status_code}")
print(f"Response: {response_update_user.json()}")



# TEST-DELETE_USER
# Supponendo che l'utente creato nel test ADD_USER abbia ID 1
user_id_to_delete = 4
try:
    response_delete_user = requests.delete(f'http://localhost:4000/delete_user/{user_id_to_delete}', timeout=15)
except Exception as e:
    logging.exception("error")



print("\nTEST-DELETE_USER:")
print(f"Status code: {response_delete_user.status_code}")
print(f"Response: {response_delete_user.json()}")


