import streamlit as st
from auth import decode_jwt, login_user, register_user
from home import show_home
from staff_home import show_staff_home


def initialize_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'is_staff' not in st.session_state:
        st.session_state.is_staff = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'page' not in st.session_state:
        st.session_state.page = 'login'  # Default page

def main():
    # Initialize session state variables
    initialize_session_state()

    st.title("User Authentication")

    if st.session_state.logged_in:
        decoded_token = decode_jwt(st.session_state.token)
        if decoded_token:
            st.session_state.user_id = decoded_token.get('user_id')
            st.session_state.is_staff = decoded_token.get('is_staff', False)

            # Show sidebar with user info
            st.sidebar.write("Welcome!")
            st.sidebar.write(f"User ID: {st.session_state.user_id}")
            st.sidebar.write("Logged in as Staff" if st.session_state.is_staff else "Logged in as User")

            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.is_staff = False
                st.session_state.user_id = None
                st.session_state.token = None
                st.session_state.page = 'login'
                st.write("Logged out successfully!")
                # No need to force a rerun here

            # Redirect based on user type
            if st.session_state.is_staff:
                st.session_state.page = 'staff_home'
            else:
                st.session_state.page = 'home'

    # Display content based on the current page
    if st.session_state.page == 'login':
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Register":
            st.subheader("Register")
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            bio = st.text_input("Bio")
            location = st.text_input("Location")
            birth_date = st.date_input("Birth Date")

            if st.button("Register"):
                response = register_user(username, password, bio, location, birth_date)
                st.write(response)

        elif choice == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')

            if st.button("Login"):
                response = login_user(username, password)
                if 'access' in response:
                    st.session_state.token = response['access']
                    decoded_token = decode_jwt(response['access'])
                    if decoded_token:
                        st.session_state.user_id = decoded_token.get('user_id')
                        st.session_state.is_staff = decoded_token.get('is_staff', False)
                        st.session_state.logged_in = True
                        st.session_state.page = 'home' if not st.session_state.is_staff else 'staff_home'
                    st.write("Logged in successfully!")
                else:
                    st.write("Login failed:", response)

    elif st.session_state.page == 'home':
        show_home()

    elif st.session_state.page == 'staff_home':
        show_staff_home()

if __name__ == "__main__":
    main()
