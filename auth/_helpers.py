import os
import scrypt

def salt_generator():
    return os.urandom(32)

def hashes_password(salt, plain_password):
    from binascii import hexlify, unhexlify
    encrypt_password = scrypt.hash(
        plain_password,
        unhexlify(salt),
        buflen=64
    )
    return hexlify(encrypt_password)
