# import random
# import uuid


# class Client:
#     """
#     The Client class for connecting clients to the server.
#     """
#     def __init__(self, connection=None, address=None):
#         self.user_id = str(uuid.uuid4())
#         self.username = self.user_id
#         self.connection = connection
#         self.address = address
#         self.validated = False

#     def __str__(self):
#         return f'Client: {self.user_id}'

#     def __repr__(self):
#         return f'Client: {self.user_id}'

#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from __future__ import print_function

import random
import uuid

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver


class EchoClient(LineReceiver):
    end = b"Bye-bye!"

    def connectionMade(self):
        self.sendLine(b"Hello, world!")
        self.sendLine(b"What a fine day it is.")
        # self.sendLine(self.end)

    def lineReceived(self, line):
        print("receive:", line)
        if line == self.end:
            self.transport.loseConnection()


class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self, connection=None, address=None):
        self.user_id = str(uuid.uuid4())
        self.username = self.user_id
        self.connection = connection
        self.address = address
        self.validated = False
        self.done = Deferred()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)

    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)


def main(reactor):
    factory = EchoClientFactory()
    reactor.connectTCP('127.0.0.1', 8000, factory)
    return factory.done


if __name__ == '__main__':
    task.react(main)
