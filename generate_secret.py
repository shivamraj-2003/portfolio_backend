"""
Generate a secure secret key for JWT authentication
"""
import secrets

if __name__ == "__main__":
    secret_key = secrets.token_urlsafe(32)
    print("=" * 60)
    print("Generated Secret Key for JWT:")
    print("=" * 60)
    print(secret_key)
    print("=" * 60)
    print("\nCopy this key and update SECRET_KEY in your .env file")
