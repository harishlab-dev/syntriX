import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


# -------------------------------
# KEY NORMALIZATION (IMPORTANT)
# -------------------------------
def normalize_key(key):
    # Ensure 16 bytes (AES-128)
    return key.encode().ljust(16, b'\0')[:16]


# -------------------------------
# ENCRYPTION
# -------------------------------
def encrypt(message, key):
    key = normalize_key(key)

    iv = get_random_bytes(16)   # secure IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))

    # Convert to base64 for JSON transmission
    return (
        base64.b64encode(iv).decode(),
        base64.b64encode(ciphertext).decode()
    )


# -------------------------------
# DECRYPTION
# -------------------------------
def decrypt(iv, ciphertext, key):
    key = normalize_key(key)

    try:
        iv = base64.b64decode(iv)
        ciphertext = base64.b64decode(ciphertext)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        return plaintext.decode()

    except Exception as e:
        raise Exception("Decryption error") from e