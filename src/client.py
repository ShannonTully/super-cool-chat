import random
import uuid


class Client:
    """
    The Client class for connecting clients to the server.
    """
    def __init__(self, connection=None, address=None):
        self.user_id = str(uuid.uuid4())
        self.username = self.user_id
        self.connection = connection
        self.address = address

    def __str__(self):
        return f'Client: {self.user_id}'

    def __repr__(self):
        return f'Client: {self.user_id}'
