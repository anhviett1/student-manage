from cryptography.fernet import Fernet
from django.conf import settings
import base64
import hashlib
import os


def get_encryption_key():
    """
    Get or create encryption key
    """
    key = getattr(settings, "ENCRYPTION_KEY", None)
    if not key:
        key = Fernet.generate_key()
        # In production, you should store this key securely
        # and not generate it on the fly
    return key


def encrypt_data(data):
    """
    Encrypt sensitive data
    """
    if not data:
        return data

    key = get_encryption_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(str(data).encode())
    return base64.b64encode(encrypted_data).decode()


def decrypt_data(encrypted_data):
    """
    Decrypt sensitive data
    """
    if not encrypted_data:
        return encrypted_data

    key = get_encryption_key()
    f = Fernet(key)
    try:
        decrypted_data = f.decrypt(base64.b64decode(encrypted_data))
        return decrypted_data.decode()
    except Exception:
        return None


def hash_sensitive_data(data):
    """
    Hash sensitive data (one-way encryption)
    """
    if not data:
        return data

    salt = getattr(settings, "HASH_SALT", os.urandom(32))
    hashed = hashlib.pbkdf2_hmac("sha256", str(data).encode(), salt, 100000)  # Number of iterations
    return base64.b64encode(hashed).decode()


def mask_sensitive_data(data, mask_char="*"):
    """
    Mask sensitive data (e.g., credit card numbers, phone numbers)
    """
    if not data:
        return data

    data = str(data)
    if len(data) <= 4:
        return mask_char * len(data)

    return mask_char * (len(data) - 4) + data[-4:]
