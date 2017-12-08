import string
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom


s = openSocket()
joinRoom(s)
readbuffer = ""
i=1

while True:
		readbuffer = readbuffer + s.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
                i=i+1
                print i, len(temp), temp
		
		for line in temp:
			print(line)
			if "PING" in line:
				s.send(line.replace("PING", "PONG") + "\r\n")
				break
			user = getUser(line)
			message = getMessage(line)

			if "You Suck" in message:
				sendMessage(s, "No, you suck!")
				break
			
