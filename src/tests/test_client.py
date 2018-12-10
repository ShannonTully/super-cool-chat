from ..client import Client


def test_clients_are_unique():
    client_one = Client()
    client_two = Client()
    assert client_one.user_id != client_two


def test_client_str():
    client_one = Client()
    assert str(client_one).split()[1] == client_one.user_id
