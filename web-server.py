from socket import *

# Prepare a server socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', 6789)) # Binds the socket to an address and port
server_socket.listen(1) # Listen for incoming connections (1 connection at a time)

while True:
    # Establish the connection
    print('Ready to serve...')
    connection_socket, addr = server_socket.accept() # Accepts the connection from the client
    print(f"Connected to: {addr}")

    try:
        # Handle the client's request
        message = connection_socket.recv(1024).decode() # Receives the request message from the client
        if not message:
            connection_socket.close()
            continue

        file_name = message.split()[1] # Extracts the file name from the request
        f = open(file_name[1:]) # Opens the requested file (ignoring the initial '/')

        # Send one HTTP header line into socket
        connection_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")

        # Read and send the content of the requested file to the client
        output_data = f.read()
        f.close()

        for i in range(0, len(output_data)):
            connection_socket.send(output_data[i].encode()) # Send the file content in bytes to the client

        connection_socket.close()

    except IOError:
        # Send response message for file not found and close the client socket
        connection_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        connection_socket.send(b"<html><head></head><body><h1>404 Not Found</h1></body></html>")
        connection_socket.close()

server_socket.close()

