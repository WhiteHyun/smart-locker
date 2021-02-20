from socket import *


class Client():
    """
    Client model
    """
    INSERT = 0
    SELECT = 1
    UPDATE = 2

    def __init__(self, serv_addr: str, serv_port: int = 12000) -> None:
        self.serv_addr = serv_addr
        self.serv_port = serv_port
        self.client_socket = None

    def connect(self) -> None:
        """
        서버와 통신하기 위해 사용되는 함수입니다.
        """
        try:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(
                (self.serv_addr, self.serv_port))  # 3-way handshake
        except Exception as e:
            print(f"connect Error, {e}")
            self.close() if self.client_socket is not None else None

    def sendAndRecv(self, data: str, command_type: int):
        """
        서버와 통신하기 위해 사용되는 함수입니다.
        보내고자 하는 값을 서버에 전달하며 그 결과에 따른 값을 리턴받습니다.

        Attribute:
            data (str): 서버에 보낼 데이터
            command_type (int): 서버가 동작하는 방식

        Returns:
            message (str): 서버로부터 받아온 결과값

        Example:
            >>> sendAndRecv("'1, '", Client.INSERT)
            True

            >>> sendAndRecv("Amugeona", Client.SELECT)
        """
        try:
            recv_msg = ""
            self.client_socket.send(data.encode())
            recv_msg = self.client_socket.recv(1024)
        except Exception as e:
            print(
                f"Error! {e}\nYou must close the client socket, Call close() method")
        finally:
            return recv_msg.decode() if recv_msg else recv_msg

    def close(self) -> None:
        """
        서버와 연결을 종료시켜줍니다. 서버와 데이터 주고받는 것을 끝내고 난 후 반드시 불러와야합니다.
        """
        try:
            if self.client_socket is None:
                raise TypeError
            elif self.client_socket._closed:
                print("Already closed socket!!!!!!!")
                raise ValueError
            else:
                self.client_socket.close()

        except Exception as e:
            print(f"Close Error, {e}")


class Server():
    """
    Server Model
    """

    def __init__(self, serv_port: int = 12000) -> None:
        self.serv_port = serv_port
        self.serv_socket = None
        self.conn_socket = None

    def init_server(self) -> None:
        """
        서버를 사용하기위해 세팅되는 메소드입니다.
        """
        try:
            self.serv_socket = socket(AF_INET, SOCK_STREAM)
            self.serv_socket.bind(("", self.serv_port))
            self.serv_socket.listen()
        except Exception as e:
            print(f"connect error, {e}")
        finally:
            self.serv_socket

    def communicate(self) -> None:
        """
        client와 통신합니다.
        """
        try:
            self.conn_socket, addr = self.serv_socket.accept()
            sentence = self.conn_socket.recv(1024).decode()
            print(f"Received from ({addr[0]}), Message: '{sentence}'")

            """
            codes to communicate
            """

            self.conn_socket.send()
        except Exception as e:
            print(f"Error! {e}")
            self.close()

    def __close_conn_socket(self) -> None:
        """
        accept된 connection socket을 종료합니다.
        """
        try:
            if self.conn_socket is None:
                raise TypeError
            elif self.conn_socket._closed:
                print("Already closed socket!!!!!!!")
                raise ValueError
            else:
                self.conn_socket.close()

        except Exception as e:
            print(f"Close Error, {e}")

    def __close_serv_socket(self) -> None:
        """
        연결을 종료합니다. 데이터 주고받는 것을 끝내고 난 후 반드시 불러와야합니다.
        """
        try:
            if self.serv_socket is None:
                raise TypeError
            elif self.serv_socket._closed:
                print("Already closed socket!!!!!!!")
                raise ValueError
            else:
                self.serv_socket.close()

        except Exception as e:
            print(f"Close Error, {e}")

    def close(self) -> None:
        """
        모든 소켓을 닫습니다.
        """
        self.__close_conn_socket()
        self.__close_serv_socket()
