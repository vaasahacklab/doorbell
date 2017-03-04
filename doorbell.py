#!/usr/bin/python

from subprocess import call
import socket
#create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, \
                                socket.IPPROTO_TCP)
#bind the socket to a public host,
# and a well-known port
serversocket.bind(("musicbox.lan", 8080))
#become a server socket
serversocket.listen(1)


while 1:
    #accept connections from outside
    (clientsocket, address) = serversocket.accept()
    #now do something with the clientsocket
        # Clearly state that connection will be closed after this response,
    # and specify length of response body
    clientsocket.send("HTTP/1.1 200 OK\n"
         +"Content-Type: text/html\n"
         +"Content-Length: 27\n"
         +"\n" # Important!
         +"<html><body></body></html>\n");
    clientsocket.close()

    call(["aplay","/root/doorbell.wav"])
