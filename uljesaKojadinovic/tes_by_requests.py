import requests
from requests.auth import HTTPBasicAuth
import random
import datetime

def setMembAndFeeDataByRandom(mebmOption, feeChoice):
    listOfMemberDuration = ['one-month', 'three-months', 'half-year', 'one-year']
    feeOptionsList = ['0.00', '10.00', '20.00', '30.00', '40.00', '50.00']
    mebmOption = random.choice(listOfMemberDuration)
    feeChoice = random.choice(feeOptionsList)
    return mebmOption, feeChoice

def signupFunction(email, firstName, lastName, phoneNumber):
    url = 'http://127.0.0.1:8000/signup/'
    mebmOption = ''
    feeChoice = ''
    setMembAndFeeDataByRandom(mebmOption, feeChoice)
    data = {
        'password': 'new&&12345',
        'email': f'{email}',
        'confirm_password': 'new&&12345',
        'first_name': f'{firstName}',
        'last_name': f'{lastName}',
        'phone_number': f'{phoneNumber}',
        'membership_duration': f'{mebmOption}',
        'fee': f'{feeChoice}',
    }
    r = requests.post(url, data=data)
    print(r.json())
    return r.status_code

def get_list_of_members():
    url = 'http://127.0.0.1:8000/users/'
    get_list = requests.get(url).json()
    return get_list

def update_list_of_members(session, getList, token, firstName, lastName, userId=''):
    userChoose = random.choice(getList)
    mebmOption = ''
    feeChoice = ''
    setMembAndFeeDataByRandom(mebmOption, feeChoice)
    if userId != '':
        user = userId
    else:
        user = userChoose['id']
    url = f'http://127.0.0.1:8000/users/{user}'
    dataUpdateUser = {
        'first_name': f'{firstName}',
        'last_name': f'{lastName}',
        'membership_duration': f'{mebmOption}',
        'fee': f'{feeChoice}',
    }
    headers = {'accept': 'application/json', "Authorization": f"Bearer {token['access']}"},
    updateUser = session.put(url, data=dataUpdateUser, headers=headers[0])
    return updateUser.json()


# auth with user update func
def auth_function_update_user(adminEmail, adminPassword, firstName, lastName, userId='1'):
    s = requests.Session()
    response = s.post(
        "http://localhost:8000/api/token/",
        json={"email": f"{adminEmail}", "password": f"{adminPassword}"}
    )
    tokens = response.json()
    if 'detail' in tokens:
            if tokens['detail'] == 'No active account found with the given credentials':
                return tokens['detail']
    else:
        r = update_list_of_members(s, get_list_of_members(), tokens, firstName, lastName, userId)
        if 'detail' in r:
            if r['detail'] == 'You do not have permission to perform this action':
                return r['detail']
        else:
            email = r['email']
            return f'Update of user with email {email} was successful'
        return r

print(auth_function_update_user('bogosavacm@yahoo.com', 'bogi123', 'Momir', 'Bogosavac'))

# list, create, update, delete author

def get_list_of_authors():
    url = 'http://127.0.0.1:8000/list-author/'
    get_list = requests.get(url).json()
    return get_list

def create_update_delete_author(session, token, firstName, lastName, year_of_birth, method, id=''):
    url = ''

    dataCreateAuthor = {
        'first_name': f'{firstName}',
        'last_name': f'{lastName}',
        'year_of_birth': f'{year_of_birth}',
    }
    headers = {'accept': 'application/json', "Authorization": f"Bearer {token['access']}"},
    if method == 'create':
        url = 'http://127.0.0.1:8000/list-create-author/'
        updateUser = session.post(url, data=dataCreateAuthor, headers=headers[0])
        return updateUser.json()
    elif method == 'update':
        url = f'http://127.0.0.1:8000/list-create-author/{id}'
        updateUser = session.put(url, data=dataCreateAuthor, headers=headers[0])
        return updateUser.json()
    elif method == 'delete':
        url = f'http://127.0.0.1:8000/list-create-author/{id}'
        updateUser = session.delete(url, headers=headers[0])
        return updateUser.status_code


def auth_function_update_list_author(adminEmail, adminPassword, firstName, lastName, year_of_birth, method, id=''):
    s = requests.Session()
    message = ''
    response = s.post(
        "http://localhost:8000/api/token/",
        json={"email": f"{adminEmail}", "password": f"{adminPassword}"}
    )
    tokens = response.json()
    if 'detail' in tokens:
            if tokens['detail'] == 'No active account found with the given credentials':
                return tokens['detail']
    else:
        author = create_update_delete_author(s, tokens, firstName, lastName, year_of_birth, method, id)
        if isinstance(author, int):
            return 'Author has been successfully deleted from database!'
        if 'detail' in author:
            if author['detail'] == 'You do not have permission to perform this action':
                return author['detail']
        else:
            authorName = author['first_name'] + ' ' + author['last_name']
            if method == 'create':
                return f'Author {authorName} has been successfully created in database!'
            elif method == 'update':
                return f'Update of author {authorName} was successful'
        message = author['detail']
    return f'Function have no success in {method} method! {message}'

# date = datetime.date(1942, 2, 25)
# print(auth_function_update_list_author('************', '********', 'Zil', 'Vern', date, 'create', '8'))

# get, post, put, update books

def get_book_list():
    url = 'http://127.0.0.1:8000/list-book/'
    get_list = requests.get(url).json()
    return get_list

def create_update_delete_book(session, token, book_name, release_year, pages, genresSlice, method, id=''):
    url = ''
    GANRES = ['Academic & Education', 'Art', 'Biography', 'Business & Career', 'Environment',
              'Fiction & Literature','Health & Fitness','Lifestyle','Personal Growth','Politics & Laws', 'Religion',
              'Science & Research','Technology',]
    genre = GANRES[genresSlice]
    dataCreateUpdateBook = {
        'book_name': f'{book_name}',
        'release_year': f'{release_year}',
        'pages': f'{pages}',
        'ganres': f'{genre}',
        'author':[
            3,
        ],
        'quantity': 25
    }
    headers = {'accept': 'application/json', "Authorization": f"Bearer {token['access']}"},
    if method == 'create':
        url = 'http://127.0.0.1:8000/create-book/'
        updateBook = session.post(url, data=dataCreateUpdateBook, headers=headers[0])
        return updateBook.json()
    elif method == 'update':
        url = f'http://127.0.0.1:8000/list-create-book/{id}'
        updateBook = session.put(url, data=dataCreateUpdateBook, headers=headers[0])
        return updateBook.json()
    elif method == 'delete':
        url = f'http://127.0.0.1:8000/list-create-book/{id}'
        updateBook = session.delete(url, headers=headers[0])
        return updateBook.status_code

def auth_function_update_list_book(adminEmail, adminPassword, book_name, release_year, pages, genresSlice, method, id=''):
    s = requests.Session()
    message = ''
    response = s.post(
        "http://localhost:8000/api/token/",
        json={"email": f"{adminEmail}", "password": f"{adminPassword}"}
    )
    tokens = response.json()
    if 'detail' in tokens:
            if tokens['detail'] == 'No active account found with the given credentials':
                return tokens['detail']
    else:
        book = create_update_delete_book(s, tokens, book_name, release_year, pages, genresSlice, method, id)
        print(book)
        if isinstance(book, int):
            return 'Book has been successfully deleted from database!'
        if 'detail' in book:
            if book['detail'] == 'You do not have permission to perform this action':
                return book['detail']
        else:
            bookName = book['book_name']
            if method == 'create':
                return f'Book {bookName} has been successfully created in database!'
            elif method == 'update':
                return f'Update of book {bookName} was successful'
        message = book['detail']
    return f'Function have no success in {method} method! {message}'

date = datetime.date(1915, 8, 15)
# print(auth_function_update_list_book('mateja@yahoo.com', 'mateja$$1977', 'Moja prica', date, 321, 0, 'create'))
# # chek if user has permissionss
# print(auth_function_update_list_book('********', '********', '20000 milja po morem', date, 289, 4, 'update', '5'))

def get_borrower_list():
    url = 'http://127.0.0.1:8000/list-borrower-book/'
    get_list = requests.get(url).json()
    return get_list


def create_update_delete_borrower_book(session, token, borrowerId, bookId, method, id=''):
    url = ''

    dataCreateUpdateBorrower= {
        'borrower': f'{borrowerId}',
        'book': f'{bookId}',
    }
    headers = {'accept': 'application/json', "Authorization": f"Bearer {token['access']}"},
    if method == 'create':
        url = 'http://127.0.0.1:8000/create-borrower-book/'
        updateBorrower = session.post(url, data=dataCreateUpdateBorrower, headers=headers[0])
        return updateBorrower.json()
    elif method == 'update':
        url = f'http://127.0.0.1:8000/create-borrower-book/{id}'
        updateBorrower = session.put(url, data=dataCreateUpdateBorrower, headers=headers[0])
        return updateBorrower.json()
    elif method == 'delete':
        url = f'http://127.0.0.1:8000/create-borrower-book/{id}'
        updateBorrower = session.delete(url, headers=headers[0])
        return updateBorrower.status_code

def auth_function_update_list_borrower_book(adminEmail, adminPassword, borrowerId, bookId, method, id=''):
    s = requests.Session()
    message = ''
    response = s.post(
        "http://localhost:8000/api/token/",
        json={"email": f"{adminEmail}", "password": f"{adminPassword}"}
    )
    tokens = response.json()
    if 'detail' in tokens:
            if tokens['detail'] == 'No active account found with the given credentials':
                return tokens['detail']
    else:
        borrower = create_update_delete_borrower_book(s, tokens, borrowerId, bookId, method, id)
        if isinstance(borrower, int):
            return 'Borrower has been successfully deleted from database!'
        if 'detail' in borrower:
            if borrower['detail'] == 'You do not have permission to perform this action':
                return borrower['detail']
        else:
            if 'borrower' in borrower:
                borrowerName = borrower['borrower']
                if method == 'create':
                    return f'Borrower {borrowerName} has been successfully created in database!'
                elif method == 'update':
                    return f'Update of borrower {borrowerName} was successful'
            elif 'non_field_errors' in borrower:
                return borrower['non_field_errors'][0]
        message = borrower['detail']
    return f'Function have no success in {method} method! {message}'

# print(auth_function_update_list_borrower_book('***********', '**********', 3, 2, 'create', '2'))

url = 'http://127.0.0.1:8000/celery/'
year_of_birth = datetime.date(1896, 8, 8)
dataCreateAuthor = {
        'first_name': 'Ivo',
        'last_name': 'Andric',
        'year_of_birth': f'{year_of_birth}',
    }

r = requests.post(url, data=dataCreateAuthor)
# print(r.status_code)



url = 'http://127.0.0.1:8000/frak/'
p = requests.get(url)
print(p)
