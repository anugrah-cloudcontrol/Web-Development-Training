import streamlit as st

# Initialize the session state attributes
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False  # Default to not logged in

if 'page' not in st.session_state:
    st.session_state.page = 'Login'  # Default to 'Login'

if 'token' not in st.session_state:
    st.session_state.token = None  # Default to no token

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

# Page rendering
render_page()

# In your Home page (pages/Home.py)
def home():
    st.title("Home Page")
    st.write("Welcome to the home page!")
    if st.button("Logout", key="home_logout"):
        logout_user()
