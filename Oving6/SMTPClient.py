from socket import *
import argparse as ap
import getpass as gp


#Get sender_email and recipient_email as arguments to the program
parser = ap.ArgumentParser(description='A test SMTP client without authentication')
parser.add_argument('-f', '--from', dest='fromMail', required=True, metavar='<sender_email>')
parser.add_argument('-t', '--to', dest='toMail', required=True, metavar='<recipient_email>')
#parser.add_argument('-u', '--username', dest='username', required=True, metavar='<username>')


args = parser.parse_args()
fromMail = args.fromMail #Sender's email address
toMail = args.toMail #Recipient's email address


# You can run a local simple SMTP server such as "Fake SMTP Server" and communicate with it without authentication.
mailServer = 'localhost'
# (use the appropriate port) with mailserver
mailPort = 1337


# Create socket called clientSocket and establish a TCP connection
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, mailPort))

recv0 = clientSocket.recv(1024)
print(recv0)
if recv0[:3] != b'220':
	print('0 220 reply not received from server.')


# Create a helper function for the sending and receiving
def comms(cmd, id):
	clientSocket.send(cmd.encode())
	recv = clientSocket.recv(1024)
	print(recv)
	if recv[:3] != id:
		print(str(id)," reply not received from server.")


# Send HELO command and print server response.
heloCommand = "EHLO Hey\r\n"
comms(heloCommand,b'250')


# Send MAIL FROM command ... and print server response.
mailFromCmd= "MAIL FROM: <" + str(fromMail) + ">\r\n"
comms(mailFromCmd, b'250')


# Send RCPT TO command ... and print server response.
rcptToCmd = "RCPT TO: <" + str(toMail) + ">\r\n"
comms(rcptToCmd,b'250')


# Send DATA command ... and print server response.
dataCmd = "DATA\r\n"
comms(dataCmd,b'354')


# Message to send
msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
# Send message data ... and print server response.
clientSocket.send(msg.encode())
comms((endmsg),b'250')


# Send QUIT command ... and print server response.
quitCmd = "QUIT\r\n"
comms(quitCmd,b'221')
