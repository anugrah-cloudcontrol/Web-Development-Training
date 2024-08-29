import requests
import streamlit as st
import os

# Backend URL configuration
BACKEND_URL = os.getenv("BACKEND_ADDRESS", "http://127.0.0.1")
PORT = os.getenv("PORT", "8000")
USER_LIST_API = f"{BACKEND_URL}:{PORT}/api/users/"

def get_token():
    return st.session_state.get('token')

def edit_user():
    if 'selected_user' not in st.session_state or not st.session_state.selected_user:
        st.error("No user selected for editing.")
        return

    user_id = st.session_state.selected_user
    token = get_token()

    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'

    user_details_url = f"{USER_LIST_API}{user_id}/"
    
    try:
        response = requests.get(user_details_url, headers=headers)
        response.raise_for_status()
        user = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch user details: {e}")
        return

    if not user:
        st.error("User not found or invalid response.")
        return

    st.title(f"Edit User: {user.get('username', 'Unknown')}")

    with st.form(key=f"edit_form_{user_id}"):
        new_username = st.text_input("Edit Username", value=user.get('username', ''))
        new_email = st.text_input("Edit Email", value=user.get('email', ''))
        profile = user.get('profile', {})
        new_profile_bio = st.text_input("Bio", value=profile.get('bio', ''))
        new_profile_location = st.text_input("Location", value=profile.get('location', ''))
        new_profile_birth_date = st.text_input("Birth Date", value=profile.get('birth_date', ''))

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Perform the user update API request
            update_data = {
                'username': new_username,
                'email': new_email,
                'profile': {
                    'bio': new_profile_bio,
                    'location': new_profile_location,
                    'birth_date': new_profile_birth_date
                }
            }
            try:
                update_response = requests.patch(user_details_url, json=update_data, headers=headers)
                update_response.raise_for_status()
                st.success(f"User {user['username']} details updated successfully!")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to update user details: {e}")

