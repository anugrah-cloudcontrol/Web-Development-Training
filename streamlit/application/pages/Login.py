import os
import requests
import streamlit as st
import jwt  # PyJWT to decode the token
from Home import home

# Initialize the session state attributes
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False  # Default to not logged in

if 'page' not in st.session_state:
    st.session_state.page = 'login'  # Default to 'login'

if 'token' not in st.session_state:
    st.session_state.token = None  # Default to no token

if 'is_staff' not in st.session_state:
    st.session_state.is_staff = False  # Default to not staff

# Get backend URL from environment variable, with a default value
BACKEND_URL = os.getenv("BACKEND_ADDRESS", "http://127.0.0.1")
PORT = os.getenv("PORT", "8000")

# Secret key used to decode the JWT token (this should match the key in your Django settings)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
# print(f"SECRET_KEY being used: {SECRET_KEY}")  # Debugging line to check if the correct secret key is used

# Functions for handling authentication
def login_user(username, password):
    url = f"{BACKEND_URL}:{PORT}/api/login/"
    response = requests.post(
        url,
        json={"username": username, "password": password},
    )

    if response.status_code == 200:
        st.session_state.token = response.json().get('access')
        st.session_state.logged_in = True
        st.session_state.page = 'home'

        try:
            # Decode the JWT token
            decoded_token = jwt.decode(st.session_state.token, SECRET_KEY, algorithms=["HS256"])
            # print(f"Decoded Token: {decoded_token}")  # Debugging line to check the decoded token
            st.session_state.is_staff = decoded_token.get('is_staff', False)
        except jwt.ExpiredSignatureError:
            st.error("Token expired. Please log in again.")
            st.session_state.logged_in = False
            st.session_state.page = 'login'
        except jwt.InvalidSignatureError:
            st.error("Invalid token signature. Please log in again.")
            st.session_state.logged_in = False
            st.session_state.page = 'login'
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.logged_in = False
            st.session_state.page = 'login'
    else:
        st.error("Login failed. Check your username and password.")

def login():
    st.title("Login")
    if st.session_state.logged_in:
        st.write("You are already logged in!")
        if st.button("Go to Home", key="login_go_to_home"):
            st.session_state.page = 'home'
        return

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        login_user(username, password)
    if st.button("Register", key="login_register"):
        st.session_state.page = 'Register'

def register():
    st.title("Register")
    st.write("Registration page (placeholder).")

def logout_user():
    if st.session_state.token:
        headers = {
            "Authorization": f"Bearer {st.session_state.token}"
        }
        url = f"{BACKEND_URL}:{PORT}/api/logout/"  # Replace with your logout endpoint
        response = requests.post(url, headers=headers)

        if response.status_code == 205:
            st.success("Successfully logged out.")
        else:
            st.error("Failed to log out.")

    st.session_state.logged_in = False
    st.session_state.page = 'login'
    st.session_state.token = None
    st.session_state.is_staff = False

# Main function to handle navigation between pages
def main():
    if st.session_state.page == 'login':
        login()
    elif st.session_state.page == 'home':
        home()
    elif st.session_state.page == 'Register':
        register()

    # You can display staff-specific content based on the 'is_staff' flag
    if st.session_state.is_staff:
        st.sidebar.success("You have staff access!")

if __name__ == '__main__':
    main()
