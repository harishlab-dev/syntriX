from flask import Flask, request, jsonify
from crypto_utils import decrypt
from utils import hash_data

app = Flask(__name__)

# -------------------------------
# CONFIG
# -------------------------------
SECRET = "key123"
used_nonces = set()

# -------------------------------
# AUTH ENDPOINT
# -------------------------------
@app.route('/auth', methods=['POST'])
def auth():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["id", "nonce", "iv", "ciphertext", "hash"]
        for field in required_fields:
            if field not in data:
                return jsonify({"status": f"Missing field: {field} ❌"})

        device_id = data["id"]
        nonce = data["nonce"]
        iv = data["iv"]
        ciphertext = data["ciphertext"]
        received_hash = data["hash"]

        # -------------------------------
        # 1. REPLAY ATTACK CHECK
        # -------------------------------
        if nonce in used_nonces:
            return jsonify({"status": "Replay Attack Detected ❌"})

        # -------------------------------
        # 2. INTEGRITY CHECK (HASH)
        # -------------------------------
        expected_hash = hash_data(ciphertext)

        if expected_hash != received_hash:
            return jsonify({"status": "Integrity Check Failed ❌"})

        # -------------------------------
        # 3. DECRYPTION
        # -------------------------------
        # 3. Decrypt
        try:
            decrypted = decrypt(iv, ciphertext, SECRET)
            print("DECRYPTED:", decrypted)   # ✅ print AFTER decrypt
        except:
            return jsonify({"status": "Decryption Failed ❌"})

        # 4. Validate content
        expected = f"{device_id}:{nonce}"
        print("EXPECTED:", expected)        # ✅ print AFTER expected is created

        if decrypted == expected:
            used_nonces.add(nonce)
            return jsonify({"status": "Authentication Successful ✅"})
        else:
            return jsonify({"status": "Impersonation Detected ❌"})

    except Exception as e:
        print("Server error:", e)
        return jsonify({"status": "Server Error ❌"})


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)