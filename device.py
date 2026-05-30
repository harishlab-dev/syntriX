import requests
import random
from utils import hash_data
from crypto_utils import encrypt

# -------------------------------
# CONFIG
# -------------------------------
SERVER_URL = "http://127.0.0.1:5001/auth"   # must match server port
DEVICE_ID = "device1"

# -------------------------------
# GLOBAL (for replay attack)
# -------------------------------
LAST_PAYLOAD = None


# -------------------------------
# NORMAL AUTHENTICATION
# -------------------------------
def send_request(secret):
    global LAST_PAYLOAD

    # Generate nonce
    nonce = str(random.randint(1000, 9999))

    # Create message
    message = DEVICE_ID + ":" + nonce

    # Encrypt using AES
    iv, ciphertext = encrypt(message, secret)

    # Hash encrypted data
    hash_val = hash_data(ciphertext)

    # Payload
    payload = {
        "id": DEVICE_ID,
        "nonce": nonce,
        "iv": iv,
        "ciphertext": ciphertext,
        "hash": hash_val
    }

    # Store for replay attack
    LAST_PAYLOAD = payload

    try:
        response = requests.post(SERVER_URL, json=payload)
        return response.json(), nonce
    except:
        return {"status": "Server Error ❌"}, nonce


# -------------------------------
# REPLAY ATTACK
# -------------------------------
def replay_attack():
    global LAST_PAYLOAD

    # No previous request
    if LAST_PAYLOAD is None:
        return {"status": "No previous request ❌"}, None

    try:
        response = requests.post(SERVER_URL, json=LAST_PAYLOAD)
        return response.json(), LAST_PAYLOAD["nonce"]
    except:
        return {"status": "Replay Failed ❌"}, LAST_PAYLOAD["nonce"]