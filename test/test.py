import requests
import logging


# TEST-ADD_USER
data = {
    'name': 'John',
    'surname': 'Doe'
}
try:
    response_add_user = requests.post('http://localhost:4000/add_user',json=data,timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-ADD_USERS:")
print(f"Status code: {response_add_user.status_code}")
print(f"Response: {response_add_user.json()}")


# TEST-GET_USERS
try:
    response_get_users = requests.get(f'http://localhost:4000/get_users', timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-GET_USERS:")
print(f"Status code: {response_get_users.status_code}")
print(f"Response: {response_get_users.json()}")


# TEST-UPDATE_USER
user_id_to_update = 1
data_update_user = {'name': 'UpdatedName', 'surname': 'UpdatedSurname'}
try:
    response_update_user = requests.put(f'http://localhost:4000/update_user/{user_id_to_update}', json=data_update_user, timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-UPDATE_USER:")
print(f"Status code: {response_update_user.status_code}")
print(f"Response: {response_update_user.json()}")



# TEST-DELETE_USER
user_id_to_delete = 1
try:
    response_delete_user = requests.delete(f'http://localhost:4000/delete_user/{user_id_to_delete}', timeout=15)
except Exception as e:
    logging.exception("error")



print("\nTEST-DELETE_USER:")
print(f"Status code: {response_delete_user.status_code}")
print(f"Response: {response_delete_user.json()}")

# TEST-ADD_BOOK
data_add_book = {
    'title': 'The Great Gatsby',
    'author': 'F. Scott Fitzgerald'
}
try:
    response_add_book = requests.post('http://localhost:5000/add_book', json=data_add_book, timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-ADD_BOOK:")
print(f"Status code: {response_add_book.status_code}")
print(f"Response: {response_add_book.json()}")


# TEST-GET_BOOK
book_id_to_get = 1
try:
    response_get_book = requests.get(f'http://localhost:5000/get_books/{book_id_to_get}', timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-GET_BOOK:")
print(f"Status code: {response_get_book.status_code}")
print(f"Response: {response_get_book.json()}")


# TEST-UPDATE_BOOK
book_id_to_update = 1
data_update_book = {'title': 'UpdatedTitle', 'author': 'UpdatedAuthor'}
try:
    response_update_book = requests.put(f'http://localhost:5000/update_book/{book_id_to_update}', json=data_update_book, timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-UPDATE_BOOK:")
print(f"Status code: {response_update_book.status_code}")
print(f"Response: {response_update_book.json()}")


# TEST-DELETE_BOOK
book_id_to_delete = 1
try:
    response_delete_book = requests.delete(f'http://localhost:5000/delete_book/{book_id_to_delete}', timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-DELETE_BOOK:")
print(f"Status code: {response_delete_book.status_code}")
print(f"Response: {response_delete_book.json()}")

# TEST-ADD_LOAN
data_add_loan = {
    'IdCliente': 1,
    'IdLibro': 1
}
try:
    response_add_loan = requests.post('http://localhost:6000/add', json=data_add_loan, timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-ADD_LOAN:")
print(f"Status code: {response_add_loan.status_code}")
print(f"Response: {response_add_loan.json()}")


# TEST-GET_LOAN
loan_id_to_get = 1
try:
    response_get_loan = requests.get(f'http://localhost:6000/get_loan/{loan_id_to_get}', timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-GET_LOAN:")
print(f"Status code: {response_get_loan.status_code}")
print(f"Response: {response_get_loan.json()}")


# TEST-GET_LOANS
try:
    response_get_loans = requests.get('http://localhost:6000/get_loans', timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-GET_LOANS:")
print(f"Status code: {response_get_loans.status_code}")
print(f"Response: {response_get_loans.json()}")


# TEST-UPDATE_LOAN
loan_id_to_update = 1
data_update_loan = {'IdCliente': 2, 'IdLibro': 2, 'disponibile': True}
try:
    response_update_loan = requests.put(f'http://localhost:6000/update_loan/{loan_id_to_update}', json=data_update_loan, timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-UPDATE_LOAN:")
print(f"Status code: {response_update_loan.status_code}")
print(f"Response: {response_update_loan.json()}")


# TEST-DELETE_LOAN
loan_id_to_delete = 1
try:
    response_delete_loan = requests.delete(f'http://localhost:6000/delete_loan/{loan_id_to_delete}', timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-DELETE_LOAN:")
print(f"Status code: {response_delete_loan.status_code}")
print(f"Response: {response_delete_loan.json()}")
