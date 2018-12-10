from client import Client
from imports import help_string
import threading
import socket
import sys
import re


PORT = 8000


class ChatServer(threading.Thread):
    def __init__(self, port, host='localhost'):
        super().__init__(daemon=True)
        self.port = port
        self.host = host
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP,
        )
        self.client_pool = []

        try:
            self.server.bind((self.host, self.port))
        except socket.error:
            print(f'Bind failed. {socket.error}')
            sys.exit()

        self.server.listen(10)

    def run_thread(self, user_id, username, connection, address):
        end_state = 'close'
        print(f'{username} connected at {address[0]}:{address[1]}')
        data = bytes(username + ' has joined\n', 'utf-8')
        [client.connection.sendall(data) for client in self.client_pool if len(self.client_pool)]
        for client in self.client_pool:
            if client.user_id == user_id:
                client.connection.sendall(bytes('Type in !help to get help or !quit to quit.\n', 'utf-8'))

        while True:
            try:
                data = connection.recv(4096).decode()
                if data:
                        end_state = self.parse(data, user_id)
                else:
                    for client in self.client_pool:
                        if client.user_id == user_id:
                            self.client_pool.remove(client)
                            client.connection.sendall(bytes('Bye', 'utf-8'))
                            client.connection.close()
                            break
                if end_state == 'close':
                    for client in self.client_pool:
                        if client.user_id == user_id:
                            self.client_pool.remove(client)
                            client.connection.sendall(bytes('Bye', 'utf-8'))
                            client.connection.close()
                            break
            except OSError:
                break

    def parse(self, data, user_id):
        hit = False
        for client in self.client_pool:
            if client.user_id == user_id:
                sender = client
                break

        if not sender.validated:
            import pdb; pdb.set_trace()
            if data != 'catsrcoolmeow\n':
                sender.connection.sendall(bytes('Please enter the right password.', 'utf-8'))
                sender.connection.close()
                return 'close'
            else:
                sender.validated = True

        if data[0] == '!' and data[1] != ' ':
            user_command = re.search(r'!.+?\b', data).group()

            if user_command == '!quit':
                hit = True
                self.client_pool.remove(sender)
                data = bytes(sender.username + ' has left.\n', 'utf-8')
                [client.connection.sendall(data) for client in self.client_pool if len(self.client_pool)]
                sender.connection.close()

            if user_command == '!help':
                hit = True
                sender.connection.sendall(bytes(help_string, 'utf-8'))

            if user_command == '!list':
                hit = True
                sender.connection.sendall(bytes('Users:\n', 'utf-8'))
                for client in self.client_pool:
                    sender.connection.sendall(bytes(client.username + '\n', 'utf-8'))

            if user_command == '!username':
                hit = True
                username = data.split(' ')
                if len(username) == 2:
                    everyone_but_sender = []
                    old_username = sender.username
                    sender.username = username[1].strip()
                    sender.connection.sendall(bytes(f'Your username is now {sender.username}\n', 'utf-8'))
                    data = bytes(f'User {old_username} has changed their name to {sender.username}\n', 'utf-8')
                    for client in self.client_pool:
                        if client is not sender:
                            everyone_but_sender.append(client)
                    [client.connection.sendall(data) for client in everyone_but_sender if len(everyone_but_sender)]
                else:
                    sender.connection.sendall(bytes('Please enter !username <username>.\n', 'utf-8'))

            if user_command == '!dm':
                hit = True
                message = data.split(' ')
                if len(message) < 3:
                    sender.connection.sendall(bytes('Please enter !dm <username> <message>.\n', 'utf-8'))
                else:
                    for client in self.client_pool:
                        if message[1] == client.username:
                            client.connection.sendall(bytes('Message from ' + sender.username + ': ' + ' '.join(message[2:]), 'utf-8'))
                            return
                    sender.connection.sendall(bytes('User not found.\n', 'utf-8'))

        if not hit:
            data = bytes(sender.username + ': ' + data, 'utf-8')
            everyone_but_sender = []
            for client in self.client_pool:
                if client is not sender:
                    everyone_but_sender.append(client)
            [client.connection.sendall(data) for client in everyone_but_sender if len(everyone_but_sender)]

    def run(self):
        print(f'Server running on {self.host}:{self.port}.')

        while True:
            connection, address = self.server.accept()
            client = Client(connection=connection, address=address)
            self.client_pool.append(client)
            threading.Thread(
                target=self.run_thread,
                args=(client.user_id, client.username, client.connection, client.address),
                daemon=True,
            ).start()


if __name__ == '__main__':
    server = ChatServer(PORT)

    try:
        server.run()
    except KeyboardInterrupt:
        [client.connection.close() for client in server.client_pool if len(server.client_pool)]
        sys.exit()
