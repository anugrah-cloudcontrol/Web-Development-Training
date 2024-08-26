import os
import requests
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

# Create an instance of the cookie manager
cookies = EncryptedCookieManager(
    prefix="myapp_", 
    password="a_very_secret_key"  # Replace this with your secure key
)

if not cookies.ready():
    st.stop()

# Initialize the session state attributes
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = cookies.get('logged_in', default=False) == 'true'
    print("Cookie Value ::", cookies.get('logged_in'))

if 'page' not in st.session_state:
    st.session_state.page = cookies.get('page', default='login')

# Get backend URL from environment variable, with a default value
BACKEND_URL = os.getenv("BACKEND_ADDRESS", "http://127.0.0.1")
PORT = os.getenv("PORT", "8000")

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
        
        cookies['logged_in'] = 'true'
        cookies['page'] = st.session_state.page
        cookies['token'] = st.session_state.token
        cookies.save()

        print("Values :: ", st.session_state.token, st.session_state.logged_in, st.session_state.page)
    else:
        st.error("Login failed. Check your username and password.")

def login():
    st.title("Login")
    if st.session_state.logged_in:
        st.write("You are already logged in!")
        if st.button("Go to Home", key="login_go_to_home"):
            st.session_state['page'] = 'home'
            cookies['page'] = st.session_state.page
            cookies.save()
        return

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        login_user(username, password)
    if st.button("Register", key="login_register"):
        st.session_state['page'] = 'Register'
        cookies['page'] = st.session_state.page
        cookies.save()

def home():
    st.title("Home")
    st.write("Welcome to the Home page!")
    if st.button("Logout", key="home_logout"):
        logout_user()

def register():
    st.title("Register")
    st.write("Registration page (placeholder).")

def logout_user():
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }
    url = f"{BACKEND_URL}:{PORT}/api/logout/"  # Replace with your logout endpoint
    response = requests.post(url, headers=headers)

    if response.status_code == 205:
        st.success("Successfully logged out.")
    st.session_state.logged_in = False
    st.session_state.page = 'login'
    st.session_state.token = None
    cookies['logged_in'] = 'false'
    cookies['page'] = st.session_state.page
    cookies['token'] = ''
    cookies.save()
    
# Main function to handle navigation between pages
def main():
    if st.session_state.page == 'login':
        login()
    elif st.session_state.page == 'home':
        home()
    elif st.session_state.page == 'Register':
        register()

if __name__ == '__main__':
    main()
