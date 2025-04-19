import bluetooth
import shared_state

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", 1))
server_sock.listen(1)

print("Bluetooth server started...")

client_sock, address = server_sock.accept()
print(f"Connected to {address}")

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        shared_state.update_message(f"Bluetooth: {message}")
        print("Received via Bluetooth:", message)
except Exception as e:
    print("Bluetooth error:", e)

client_sock.close()
server_sock.close()
