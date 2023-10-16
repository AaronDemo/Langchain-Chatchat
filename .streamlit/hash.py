import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['cit@123', '123456']).generate()

print(hashed_passwords)