import os
import requests
import streamlit as st
from datetime import datetime
from Home import home
from Login import login

# Initialize the session state attributes
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False  # Default to not logged in

if 'page' not in st.session_state:
    st.session_state.page = 'register'  # Default to 'register'

if 'token' not in st.session_state:
    st.session_state.token = None  # Default to no token

# Redirect to home page if the user is logged in
if st.session_state.logged_in:
    st.session_state.page = 'home'

# Functions for handling registration
def register_user(username, password, email, bio, location, birth_date):
    # Backend URL
    BACKEND_ADDRESS = os.getenv("BACKEND_ADDRESS", "http://127.0.0.1")
    PORT = os.getenv("PORT", "8000")
    url = f"{BACKEND_ADDRESS}:{PORT}/api/register/"
    
    data = {
        "username": username,
        "password": password,
        "email": email,
        "profile": {
            "bio": bio,
            "location": location,
            "birth_date": birth_date.isoformat() if birth_date else None
        }
    }

    response = requests.post(url, json=data)

    if response.status_code == 201:
        st.success("Registration successful! You can now log in.")
        st.session_state.page = 'login'
    elif response.status_code == 400:
        st.error("Registration failed. Username or email may already be taken.")
    else:
        st.error("Registration failed. Please try again later.")

def register():
    st.title("Register")
    
    username = st.text_input("Username", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")
    
    st.write("### Profile Information")
    bio = st.text_area("Bio", key="register_bio")
    location = st.text_input("Location", key="register_location")
    birth_date = st.date_input("Birth Date", key="register_birth_date")

    if password != confirm_password:
        st.warning("Passwords do not match.")
    elif st.button("Register", key="register_button"):
        register_user(username, password, email, bio, location, birth_date)
        
    if st.button("Already have an account? Login", key="go_to_login"):
        st.session_state.page = 'login'


if __name__ == '__main__':
    if st.session_state.page == 'register':
        register()
    elif st.session_state.page == 'login':
        # You would have your login page logic here instead.
        login()
    elif st.session_state.page == 'home':
        home()
