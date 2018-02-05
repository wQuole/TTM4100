# Import socket module
from socket import *

# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)
# Prepare a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 12000

# Bind the socket to server address and server port
serverSocket.bind(('',serverPort))

# Listen to at most 1 connection at a time
serverSocket.listen(1)

# Server should be up and running and listening to the incoming connections
while True:
	print('Ready to serve...')
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()

	try:
		# Receives the request message from the client
		message = connectionSocket.recv(1024)

		# Setting up filepath, which is the second part of the HTTP header
		filepath = message.split()[1]

		# Open from second character since first char is '\' in HTTP req
		f = open(filepath[1:])

		# Read the file "f" and store the entire content of the requested file in a temporary buffer
		outputdata = f.readlines()
		print(outputdata)

		# Send the HTTP response header line to the connection socket
		connectionSocket.send(b"HTTP/1.1 200 OK\r\n\r\n")

		# Send the content of the requested file to the connection socket
		for i in range(0, len(outputdata)):
			connectionSocket.send(outputdata[i].encode('utf-8'))
		connectionSocket.send(b"\r\n")

		# Close the client connection socket
		connectionSocket.close()

	except IOError:
		# Send HTTP response message for file not found
		connectionSocket.send(b"HTTP/1.1 404 NOT FOUND\r\n\r\n")

		# What the page will actually display
		connectionSocket.send(b"<html><head></head><body><h1>404 ERROR Not Found!!!!!!!!!!!!</h1></body></html>\r\n")

# Close the client connection socket (is not reached in this implementation
# due to while looping over True...
serverSocket.close()

