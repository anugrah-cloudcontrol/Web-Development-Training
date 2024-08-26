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
    st.session_state.logged_in = cookies.get('logged_in', default=False)
    print("Cookie Value ::",cookies.get('logged_in'))

if 'page' not in st.session_state:
    st.session_state.page = cookies.get('page', default='login')

def register():
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

# Functions for handling authentication
def login_user(username, password):
    # Backend URL
    backend_url = "http://127.0.0.1:8000"  
    url = f"{backend_url}/api/login/"
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


if __name__=='__main__':
    register()
