import os
from Login import login, logout_user
from Register import register
from Home import home
import streamlit as st
import requests

# Backend URL configuration
BACKEND_URL = os.getenv("BACKEND_ADDRESS", "http://127.0.0.1")
PORT = os.getenv("PORT", "8000")
USER_LIST_API = f"{BACKEND_URL}:{PORT}/api/users/"

def get_token():
    return st.session_state.get('token')

def view_users():
    st.title("User List")

    if not st.session_state.get('is_staff', False):
        st.error("You do not have permission to view this page.")
        return

    token = get_token()  # This should safely return None if not set

    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    else:
        st.error("Authorization token is missing.")
        return

    try:
        response = requests.get(USER_LIST_API, headers=headers)
        response.raise_for_status()
        users = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch users: {e}")
        return

    for user in users:
        st.subheader(f"Username: {user.get('username', 'N/A')}")
        st.write(f"Email: {user.get('email', 'N/A')}")

        # Safely get the profile or default to an empty dictionary
        profile = user.get('profile', {})
        if profile:
            st.write(f"Bio: {profile.get('bio', 'N/A')}")
            st.write(f"Location: {profile.get('location', 'N/A')}")
            st.write(f"Birth Date: {profile.get('birth_date', 'N/A')}")

        # Use a unique key for each button
        with st.expander(f"Edit {user.get('username', 'N/A')}", expanded=False):
            new_username = st.text_input("Edit Username", value=user.get('username', ''), key=f"username_{user.get('id', '')}")
            new_email = st.text_input("Edit Email", value=user.get('email', ''), key=f"email_{user.get('id', '')}")
            if profile:
                new_profile_bio = st.text_input("Bio", value=profile.get('bio', ''), key=f"bio_{user.get('id', '')}")
                new_profile_location = st.text_input("Location", value=profile.get('location', ''), key=f"location_{user.get('id', '')}")
                new_profile_birth_date = st.text_input("Birth Date", value=profile.get('birth_date', ''), key=f"birth_date_{user.get('id', '')}")
            else:
                new_profile_bio = st.text_input("Bio", key=f"bio_{user.get('id', '')}")
                new_profile_location = st.text_input("Location", key=f"location_{user.get('id', '')}")
                new_profile_birth_date = st.text_input("Birth Date", key=f"birth_date_{user.get('id', '')}")
            
            if st.button(f"Save Changes for {user.get('username', 'N/A')}", key=f"save_btn_{user.get('id', '')}"):
                updated_user_data = {
                    'username': new_username,
                    'email': new_email,
                    'profile': {
                        'bio': new_profile_bio,
                        'location': new_profile_location,
                        'birth_date': new_profile_birth_date
                    }
                }

                try:
                    update_response = requests.put(
                        f"{USER_LIST_API}{user.get('id', '')}/",
                        json=updated_user_data,
                        headers=headers
                    )
                    update_response.raise_for_status()
                    st.success(f"User {user.get('username', 'N/A')} details updated successfully!")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to update user: {e}")
                
        if st.button(f"Delete {user.get('username', 'N/A')}", key=f"delete_btn_{user.get('id', '')}"):
            if st.session_state.get('confirm_delete', None) == user.get('id', ''):
                try:
                    delete_response = requests.delete(
                        f"{USER_LIST_API}{user.get('id', '')}/",
                        headers=headers
                    )
                    delete_response.raise_for_status()
                    st.success(f"User {user.get('username', 'N/A')} deleted successfully!")
                    st.session_state['confirm_delete'] = None  # Reset confirmation state
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to delete user: {e}")
            else:
                st.warning(f"Are you sure you want to delete {user.get('username', 'N/A')}? Click again to confirm.")
                st.session_state['confirm_delete'] = user.get('id', '')

        st.write("---")

def main():
    st.sidebar.title("Navigation")
    menu_options = ["Home", "View Users", "Login", "Register"]
    choice = st.sidebar.radio("Go to", menu_options, key="nav_radio")

    # Initialize session state variables if not present
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'is_staff' not in st.session_state:
        st.session_state.is_staff = False
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'selected_user' not in st.session_state:
        st.session_state.selected_user = None
    if 'confirm_delete' not in st.session_state:
        st.session_state.confirm_delete = None

    # Reset page state when a different menu option is selected
    if choice == "Home":
        st.session_state.page = 'home'
    elif choice == "View Users":
        st.session_state.page = 'view_users'
    elif choice == "Login":
        st.session_state.page = 'login'
    elif choice == "Register":
        st.session_state.page = 'register'

    # Navigation based on page state
    if st.session_state.page == 'home':
        home()
    elif st.session_state.page == 'view_users':
        view_users()
    elif st.session_state.page == 'login':
        login()
    elif st.session_state.page == 'register':
        register()
    
    if st.session_state.logged_in:
        # Add a logout button at the bottom of the sidebar
        if st.sidebar.button("Logout"):
            logout_user()
            st.success("You have been logged out.")
            

if __name__ == '__main__':
    main()
