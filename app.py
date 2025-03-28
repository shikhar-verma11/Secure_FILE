import os
import streamlit as st
import pyotp
import qrcode
from PIL import Image
from io import BytesIO
from auth import register, login_user, get_user_secret, verify_2fa_code
from file_manager import list_user_files, create_file, read_file, update_file, delete_file

st.set_page_config(page_title="Secure File Manager", layout="centered")

# Initialize secure directory
os.makedirs("secure_files", exist_ok=True)

def generate_qr_code(secret, username):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=username, issuer_name="SecureFileManager")
    img = qrcode.make(uri)
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)
    return buf

def registration_ui():
    st.subheader("🔐 Register New User")
    username = st.text_input("Username", key="reg_user")
    password = st.text_input("Password", type="password", key="reg_pass")
    if st.button("Register"):
        secret = register(username, password)
        if secret:
            st.success("Registered successfully!")
            st.info("Scan this QR code using Google Authenticator or Authy.")
            buf = generate_qr_code(secret, username)
            st.image(Image.open(buf))
        else:
            st.error("Username already exists!")

def login_ui():
    st.subheader("🔑 Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        success, role, secret = login_user(username, password)
        if success:
            st.session_state["temp_user"] = username
            st.session_state["secret"] = secret
            st.session_state["auth_phase"] = "2fa"
        else:
            st.error(role)

def two_fa_ui():
    st.subheader("🔒 2FA Verification")
    otp = st.text_input("Enter 2FA Code from Authenticator App")
    if st.button("Verify"):
        secret = st.session_state.get("secret")
        username = st.session_state.get("temp_user")
        if verify_2fa_code(secret, otp):
            st.success(f"✅ Welcome, {username}!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state.pop("auth_phase", None)
            st.session_state.pop("temp_user", None)
            st.session_state.pop("secret", None)
        else:
            st.error("Invalid 2FA code.")

def crud_dashboard():
    username = st.session_state["username"]
    st.title(f"📁 Secure File Dashboard ({username})")

    option = st.selectbox("Choose an Operation", ["Create File", "Read File", "Update File", "Delete File", "Logout"])

    if option == "Create File":
        file_name = st.text_input("Enter new file name (with .txt extension)")
        content = st.text_area("Enter file content")
        if st.button("Create & Encrypt"):
            create_file(username, file_name, content)
            st.success(f"File '{file_name}' created and encrypted.")

    elif option == "Read File":
        files = list_user_files(username)
        if files:
            selected = st.selectbox("Select a file", files)
            if st.button("Read"):
                content = read_file(username, selected)
                st.code(content)
        else:
            st.info("No files available.")

    elif option == "Update File":
        files = list_user_files(username)
        if files:
            selected = st.selectbox("Select a file", files)
            content = read_file(username, selected)
            new_content = st.text_area("Edit file content", value=content)
            if st.button("Update"):
                update_file(username, selected, new_content)
                st.success(f"File '{selected}' updated.")
        else:
            st.info("No files to update.")

    elif option == "Delete File":
        files = list_user_files(username)
        if files:
            selected = st.selectbox("Select a file", files)
            if st.button("Delete"):
                delete_file(username, selected)
                st.success(f"File '{selected}' deleted.")
        else:
            st.info("No files to delete.")

    elif option == "Logout":
        st.session_state.clear()
        st.success("Logged out.")

# 🌐 Front Page UI
st.title("🔐 Secure File Management System")

if "logged_in" not in st.session_state:
    choice = st.sidebar.radio("Navigation", ["Login", "Register", "Exit"])
    if choice == "Login":
        if st.session_state.get("auth_phase") == "2fa":
            two_fa_ui()
        else:
            login_ui()
    elif choice == "Register":
        registration_ui()
    elif choice == "Exit":
        st.warning("Exiting... Close the tab or choose another option.")
else:
    crud_dashboard()
