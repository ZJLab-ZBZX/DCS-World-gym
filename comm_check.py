import socket, time, json
import numpy as np

from geopy import distance

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Enable the socket to receive broadcast messages
# Bind the socket to all interfaces and a specific port
server_address = ('', 10010)  # Listen on all available interfaces, port 12345
sock.bind(server_address)

sock.listen(1)
connection, client_address = sock.accept()

print("Listening for broadcast messages...")


def coordinate(pt):
    x = distance.distance(pt[:2], [0,pt[1]]).km
    y = distance.distance(pt[:2], [pt[0],0]).km
    h=pt[2]/1000
    return np.array([x,y,h])

while True:
    # Receive a message (buffer size 1024)
    try:
        t = time.time()
        data = connection.recv(8192)
        message = data.decode('utf-8')
        print(f"Received message: {message}")
        try:
            message = message.split('\n\n')[0]
            json_data = json.loads(message)
            # lla1 = json_data['self']['LatLongAlt']
            # pt1 = coordinate( lla1 )
            # print(f'Position in km: {pt1}')
            response = "{[1]= true}\n"
        except:
            if 'game start' in message:
                response = "{[52]= true}\n"
            else:
                response = "{[1]= true}\n"
            pass

        # Send a response to the sender
        connection.sendall(response.encode())

    except KeyboardInterrupt:
        break