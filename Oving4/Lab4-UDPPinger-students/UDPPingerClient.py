from time import time, asctime
from socket import *
from sys import argv

# Get the server hostname and port as command line arguments
address = (argv[1], int(argv[2]))
host = address[0]  # input("Hostname\n")
port = address[1]  # int(input("Port number\n"))
timeout = 1  # int(input("Timoeout:\n"))

# Create UDP client socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Set socket timeout
clientSocket.settimeout(timeout)

# Sequence number of the ping message
ptime = 0

# Declaring counter for Packets that gets received
packetsReceived = 0

# Declaring amount of packages to send
packetsSent = 10

# list for RTT's
RTT = []

# Ping for 10 times (sending 10 packets..)
while ptime < packetsSent:
	ptime += 1
	tid = asctime()
	s = str('#') +str(ptime) + " " + str(tid)
	# Format the message to be sent as in the Lab description
	data = s.encode()

	try:
		# Record the "sent time"
		print("\n##########################################",ptime,"############################################")
		print("Starting send time..")
		sentTime = time()

		# Send the UDP packet with the ping message
		print("Sending UDP packet...")
		print(" > DATA SENT: ", data.decode(),
			  "\t[Serveradress: ", argv[1], " & ", "Port: ",argv[2], "]", sep="")
		clientSocket.sendto(data, (host, port))

		# Receive the server response
		print("Receiving server response..")
		modifiedData, serverAddress = clientSocket.recvfrom(2048)

		# Record the "received time"
		print("Recording receive time...")
		receiveTime = time()

		# Display the server response as an output
		print("Printing modified data...")
		print(" > DATA RECEIVED: ",modifiedData.decode(),
			"\t[Serveraddress: ", serverAddress[0], " & Port: ", serverAddress[1], "]",sep="")

		# Round Trip Time is the difference between sent and received time
		print("Printing roundtrip..")
		roundTrip = (receiveTime - sentTime)*1000
		print(" >", round(roundTrip, 2), "ms")

		# Add RTT to list
		RTT.append(roundTrip)

		# Increment number of packets received
		packetsReceived += 1

	except IOError:
		# Server does not response
		# Assume the packet is lost
		print("\n ------------------------------ Request",ptime,"timed out ------------------------------")
		continue

# Print Packet Loss Rate
packetsLost = packetsSent - packetsReceived
packetLossRate = (packetsLost/packetsSent)*100
print("Ping statistics for ", serverAddress[0],":",sep="")
print("  > Packets: Sent = ",
	  packetsSent, ", Received = ",
	  packetsReceived,", Lost = ",
	  packetsLost, " (",round(packetLossRate,3),"% loss)",sep="")

# Print minimum, maximum and average RTT's
minimum = round(min(RTT), 2)
average = round(sum(RTT)/len(RTT), 2)
maximum = round(max(RTT), 2)

print("Approximate round trip times in milli-seconds:")
print("  > Minimum = ",minimum, "ms,", " Maximum = ", maximum, "ms,", " Average = ", average, "ms",sep="")

# Close the client socket
clientSocket.close()
