"""Includes functions that encrypt and decrypt provided string with secret
"""

import binascii
from simplecrypt import encrypt, decrypt, DecryptionException
from base64 import b64encode, b64decode

password = "fatAssPass"


def encrypt_string(message):
    """Encrypts message with stored password"""
    cipher = encrypt(password, message)
    encoded_message = b64encode(cipher)
    return encoded_message


def decrypt_string(encoded_message):
    """Decrypts provided string. Error unsafe"""
    cipher = b64decode(encoded_message)
    message = decrypt(password, cipher)
    return message


def is_encrypted(message):
    """Verifies if provided string is encrypted"""
    try:
        decrypt_string(message)
        return True
    except (DecryptionException, binascii.Error):
        return False
