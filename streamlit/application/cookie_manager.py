# cookie_manager.py
from streamlit_cookies_manager import EncryptedCookieManager

# Initialize the cookie manager
cookies = EncryptedCookieManager(
    prefix="myapp_", 
    password="a_very_secret_key"  # Replace this with your secure key
)

# Ensure cookies are ready before using them
def get_cookies():
    if not cookies.ready():
        return None
    return cookies