import requests
import jwt  # PyJWT
from jwt.exceptions import InvalidTokenError

# API endpoints
BASE_URL = 'http://localhost:8000/api/'
REGISTER_URL = BASE_URL + 'register/'
LOGIN_URL = BASE_URL + 'login/'

# Secret key should match the one used in Django settings
SECRET_KEY = 'your-secret-key'  # Replace this with your actual secret key

def decode_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(decoded)
        return decoded
    except InvalidTokenError:
        return None

def register_user(username, password, bio, location, birth_date):
    response = requests.post(REGISTER_URL, data={
        'username': username,
        'password': password,
        'bio': bio,
        'location': location,
        'birth_date': birth_date
    })
    return response.json()

def login_user(username, password):
    response = requests.post(LOGIN_URL, data={
        'username': username,
        'password': password
    })
    return response.json()
