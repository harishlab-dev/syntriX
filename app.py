import streamlit as st
from device import send_request
import requests
from utils import hash_data
from device import replay_attack

st.set_page_config(page_title="SentriX Dashboard", layout="wide")

st.title("🔐 SentriX - IoT Security Dashboard")

# Input
device_secret = st.text_input("Enter Device Secret", "key123")

st.markdown("---")

# Layout
col1, col2 = st.columns(2)

# -----------------------
# DEVICE PANEL
# -----------------------
with col1:
    st.subheader("📱 IoT Device Panel")

    st.write("Device ID: Smart Lock #A12")
    st.write("Status: 🟢 Connected")

    device_log = st.empty()

# -----------------------
# SERVER PANEL
# -----------------------
with col2:
    st.subheader("🖥️ Server Panel")

    server_log = st.empty()

st.markdown("---")

# Buttons
c1, c2, c3 = st.columns(3)

# -----------------------
# NORMAL
# -----------------------
with c1:
    # NORMAL
    if st.button("🔵 Normal Authentication", key="normal_btn"):
        device_log.info("Device → Sending authentication request...")

        result, nonce = send_request(device_secret)

        server_log.success("Server → Verifying request...")

        if "Successful" in result["status"]:
            server_log.success(result["status"])
        else:
            server_log.error(result["status"])

        device_log.success(f"Nonce Generated: {nonce}")

# -----------------------
# REPLAY
# -----------------------
with c2:
    # REPLAY
    if st.button("🟡 Replay Attack", key="replay_btn"):
        device_log.warning("Device → Sending initial request...")

        result, nonce = replay_attack()

        if "Replay" in result["status"]:
            server_log.error(result["status"])
        else:
            server_log.warning(result["status"])

        device_log.error(f"Reused Nonce: {nonce}")

# -----------------------
# IMPERSONATION
# -----------------------
with c3:
    # IMPERSONATION
    if st.button("🔴 Impersonation Attack", key="impersonation_btn"):
        device_log.warning("Fake Device → Trying to authenticate...")

        result, nonce = send_request("wrongkey")
        server_log.error(result["status"])
        device_log.error(f"Fake Nonce: {nonce}")

st.markdown("---")

st.info("💡 This dashboard simulates a real IoT system with device-server communication and attack detection.")