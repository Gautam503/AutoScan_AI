import socket
import requests
from requests.auth import HTTPBasicAuth

# Server Configuration
host = "0.0.0.0"  # Accept connection from any IP
port = 6101       # Port to listen for scanner data

# --- SAP Configuration ---
SAP_URL = "https://sap.company.com/api/engine"  # Replace with your actual SAP API URL
SAP_USERNAME = "your_sap_user"                  # Replace with actual SAP username
SAP_PASSWORD = "your_sap_password"              # Replace with actual SAP password

# --- Add prefix and suffix to scanned data ---
def process_barcode(data):
    prefix = "GN-"
    suffix = "-X"
    return f"{prefix}{data}{suffix}"

# --- Send the modified barcode to SAP ---
def send_to_sap(modified_data):
    payload = {
        "engine_number": modified_data  # Change the key as per SAP API
    }

    try:
        response = requests.post(
            SAP_URL,
            json=payload,  # Send JSON dictionary, not a plain string
            auth=HTTPBasicAuth(SAP_USERNAME, SAP_PASSWORD),
            headers={"Content-Type": "application/json"}
        )

        if response.status_code in [200, 201]:
            print("Data sent successfully to SAP.")
            print("SAP Response:", response.json())
        else:
            print("Failed to send data to SAP.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

    except Exception as e:
        print("Error sending data to SAP:", e)

# --- Start the TCP server to listen to scanner triggers ---
def start_server():
    print(f"📡 Starting TCP Server on {host}:{port} ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))  # bind port and host with socket
        server_socket.listen()
        print("Waiting for scanner connection...")

        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            with conn:
                while True:
                    data = conn.recv(1024)  # Receive up to 1024 bytes
                    if not data:
                        break
                    barcode = data.decode().strip()
                    print(f"[Scanner] Received: {barcode}")

                    modified_data = process_barcode(barcode)
                    print(f"[Processed] Final Engine Number: {modified_data}")

                    send_to_sap(modified_data)

# --- Entry Point ---
if __name__ == "__main__":
    start_server()
