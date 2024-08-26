import os
import requests
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from datetime import datetime

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

if 'token' not in st.session_state:
    st.session_state.token = cookies.get('token', default=None)

# Get backend address and port from environment variables
BACKEND_ADDRESS = os.getenv("BACKEND_ADDRESS", "http://127.0.0.1")
PORT = os.getenv("PORT", "8000")

def fetch_user_data():
    # Ensure the user is logged in
    if not st.session_state.logged_in:
        st.write("You are not logged in.")
        return None
    
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }
    
    # Backend URL to get user profile
    url = f"{BACKEND_ADDRESS}:{PORT}/api/profile/"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch user data.")
        return None

def update_user_data(data):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }
    # print("Update data ",data)
    url = f"{BACKEND_ADDRESS}:{PORT}/api/profile/"
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        st.success("Profile updated successfully!")
        return response.json()
    else:
        st.error("Failed to update profile.")
        return None

def home():
    st.title("User Dashboard")

    # Fetch user data from the Django backend
    user_data = fetch_user_data()

    if user_data:
        st.write("### Edit User Details")
        
        # Create input fields for user data
        username = st.text_input("Username", value=user_data.get('username', ''))
        email = st.text_input("Email", value=user_data.get('email', ''))
        
        # Check if profile data exists
        profile = user_data.get('profile', None)
        st.write("### Edit Profile Information")
        bio = st.text_area("Bio", value=profile.get('bio', '') if profile else '')
        location = st.text_input("Location", value=profile.get('location', '') if profile else '')

        # Convert birth_date string to a datetime.date object if it exists
        birth_date_str = profile.get('birth_date', None) if profile else None
        if birth_date_str:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        else:
            birth_date = None

        birth_date = st.date_input("Birth Date", value=birth_date)
        # print("User details :: ",birth_date,location,bio)
        if st.button("Save Changes"):
            # Prepare data for update
            data = {
                'username': username,
                'email': email,
                'profile': {
                    'bio': bio,
                    'location': location,
                    'birth_date': birth_date.isoformat() if birth_date else None  # Convert date to string
                }
            }
            update_user_data(data)
    else:
        st.write("No user data available.")

if __name__ == "__main__":
    home()
