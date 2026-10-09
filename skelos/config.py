import streamlit as st

# We move the configuration to Streamlit Secrets for security.
# Local development: Uses .streamlit/secrets.toml
# Cloud deployment: Uses Streamlit Cloud Secrets dashboard

FIREBASE_CONFIG = {
    "apiKey": st.secrets.get("FIREBASE_API_KEY", "AIzaSyBGvJAdwnPkF5RWiI-mLx-Mx7pYvEbdYqg"),
    "authDomain": st.secrets.get("FIREBASE_AUTH_DOMAIN", "skelos-biomechanics.firebaseapp.com"),
    "projectId": st.secrets.get("FIREBASE_PROJECT_ID", "skelos-biomechanics"),
    "storageBucket": st.secrets.get("FIREBASE_STORAGE_BUCKET", "skelos-biomechanics.firebasestorage.app"),
    "messagingSenderId": st.secrets.get("FIREBASE_SENDER_ID", ""),
    "appId": st.secrets.get("FIREBASE_APP_ID", ""),
    "databaseURL": st.secrets.get("FIREBASE_DATABASE_URL", f"https://{st.secrets.get('FIREBASE_PROJECT_ID', 'skelos-biomechanics')}.firebaseio.com")
}
