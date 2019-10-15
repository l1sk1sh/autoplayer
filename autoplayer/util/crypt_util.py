"""Includes functions that encrypt and decrypt provided string with secret
"""

import base64
import hashlib
import binascii
from Crypto import Random
from Crypto.Cipher import AES

secret = "fatAssPass"
key = hashlib.sha256(secret.encode('utf-8')).digest()
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-s[-1]]


def encrypt_string(raw):
    """Encrypts message with stored password"""
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode('utf8')))


def decrypt_string(enc):
    """Decrypts provided string. Error unsafe"""
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))


def is_encrypted(raw):
    """Verifies if provided string is encrypted"""
    try:
        decrypt_string(raw)
        return True
    except binascii.Error:
        return False
