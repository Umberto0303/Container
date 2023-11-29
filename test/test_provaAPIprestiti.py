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

# TEST-GET_LOANS
try:
    response_get_loans = requests.get('http://localhost:6000/get_loans', timeout=15)
except Exception as e:
    logging.exception("error")

print("\nTEST-GET_LOANS:")
print(f"Status code: {response_get_loans.status_code}")
print(f"Response: {response_get_loans.json()}")
