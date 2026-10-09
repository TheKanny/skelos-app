import pyrebase

from config import FIREBASE_CONFIG

class AuthManager:
    def __init__(self):
        # Initialize Firebase
        self.firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        self.auth = self.firebase.auth()

    def sign_up(self, email, password):
        """Creates a new user account in Firebase."""
        try:
            user = self.auth.create_user_with_email_and_password(email, password)
            return {"success": True, "user": user}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def login(self, email, password):
        """Authenticates a user with Firebase."""
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            return {"success": True, "user": user}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def logout(self):
        """Logs out the current user."""
        # In a Streamlit app, we usually just clear the session state
        pass
