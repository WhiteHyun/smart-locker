from socket import *


def sendDataToServer(command: str, server_address: str = 'localhost', server_port: int = 12000) -> str:
    """
    서버와 통신하기 위해 사용되는 함수입니다.
    보내고자 하는 값을 서버에 전달합니다.

    Attribute:
        command (str): 서버에 보낼 명령어
        server_address (str): 서버 주소
        server_port (int): 서버 포트

    Returns:
        message (str): 서버로부터 받아온 결과값

    Example:
        >>> sendDataToServer("SELECT * FROM 'TABLE_NAME';")
        etc

        >>> sendDataToServer("Amugeona")
        ""
    """
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_address, server_port))  # 3-way handshake
    client_socket.settimeout(0.3)  # Read timeout
    message = ""
    try:
        client_socket.send(command.encode())
        # Received the server response
        received_message = client_socket.recv(1024)
        message = received_message.decode()
    except IOError as e:
        # Server does not response
        # Assume the packet is lost
        print(f"Error! {e}")
    finally:
        # Close the client socket
        client_socket.close()
        return message


def receiveDataToClient(server_port: int = 12000) -> None:
    """
    **서버 전용** 함수

    Client에서 값을 받아옵니다. 해당 함수는 리눅스 서버에서 사용됩니다.

    Attribute:
        server_port (int): 서버 포트
    """
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("", server_port))
    server_socket.listen(1)
    print("The server is ready to receive")
    try:
        connection_socket, addr = server_socket.accept()
        sentence = connection_socket.recv(1024).decode()
        capitalized_sentence = sentence.upper()
        print(f"Received from ({addr[0]}), Message: '{sentence}'")
        connection_socket.send(capitalized_sentence.encode())
    except Exception as e:
        print(f"Error! {e}")
    finally:
        connection_socket.close()
        server_socket.close()
