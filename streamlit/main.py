import streamlit as st

def main():
    st.title("Multi-Page Streamlit App")

    # Initialize session state for page tracking
    if 'page' not in st.session_state:
        st.session_state.page = "Home"

    # Define page selection and navigation
    if st.session_state.page == "Home":
        home()
    elif st.session_state.page == "Page 1":
        page_1()
    elif st.session_state.page == "Page 2":
        page_2()

def home():
    st.header("Home Page")
    st.write("Welcome to the Home Page!")

    # Navigation buttons
    if st.button("Go to Page 1"):
        st.session_state.page = "Page 1"
        st.experimental_rerun()  # Refresh to update the page

    if st.button("Go to Page 2"):
        st.session_state.page = "Page 2"
        st.experimental_rerun()

def page_1():
    st.header("Page 1")
    st.write("This is Page 1.")

    # Navigation buttons
    if st.button("Go to Home"):
        st.session_state.page = "Home"
        st.experimental_rerun()

    if st.button("Go to Page 2"):
        st.session_state.page = "Page 2"
        st.experimental_rerun()

def page_2():
    st.header("Page 2")
    st.write("This is Page 2.")

    # Navigation buttons
    if st.button("Go to Home"):
        st.session_state.page = "Home"
        st.experimental_rerun()

    if st.button("Go to Page 1"):
        st.session_state.page = "Page 1"
        st.experimental_rerun()

if __name__ == "__main__":
    main()
