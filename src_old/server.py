# first of all import the socket library
from socket import *
import socket        
  
# next create a socket object 
sock = socket.socket()          
print("Socket successfully created")

tr = 1;

# kill "Address already in use" error message
if sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1):
    perror("setsockopt");
    exit(1);

  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 8001                
  
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
sock.bind(('', port))         
print("server socket binded to %s" %(port))
  
# put the socket into listening mode 
sock.listen(5)      
print("server is listening")   
  
# a forever loop until we interrupt it or  
# an error occurs 
while True: 
  
    # Establish connection with client.
    client, addr = sock.accept()      
    print('Got connection from', addr)
  
    # send a thank you message to the client.  
    client.send(b'Thank you for connecting') 

    if KeyboardInterrupt:
        [client.connection.close() for client in sock.client_pool if len(sock.client_pool)]
        # sys.exit()
        # Close the connection with the client 
        client.close() 