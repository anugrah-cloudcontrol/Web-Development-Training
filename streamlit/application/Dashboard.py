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

if 'page' not in st.session_state:
    st.session_state.page = cookies.get('page', default='Login')  # Default to 'Login'

# Define your proxy settings
proxies = {
    "http": "http://127.0.0.1:8000",  # Replace with your actual proxy settings
}

def render_page():
    if st.session_state.page == "home":
        from pages.Home import home
        home()
    elif st.session_state.page == "Register":
        from pages.Register import register
        register()
    elif st.session_state.page == "Login":
        from pages.Login import login
        login()

def logout_user():
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.page = 'Login'
    cookies['logged_in'] = 'false'
    cookies['page'] = st.session_state.page
    cookies.save()

# Page rendering
render_page()

# In your Home page (pages/Home.py)
def home():
    st.title("Home Page")
    st.write("Welcome to the home page!")
    if st.button("Logout", key="home_logout"):
        logout_user()
