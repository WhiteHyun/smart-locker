from socket import *


class Client():
    """
    Client model
    """
    INSERT = 0
    SELECT = 1
    UPDATE = 2

    def __init__(self, serv_addr: str, serv_port: int = 12000) -> None:
        self.__serv_addr = serv_addr
        self.__serv_port = serv_port
        self.__client_socket = None

    def connect(self) -> None:
        """
        서버와 통신하기 위해 사용되는 함수입니다.
        """
        try:
            self.__client_socket = socket(AF_INET, SOCK_STREAM)
            self.__client_socket.connect(
                (self.__serv_addr, self.__serv_port))  # 3-way handshake
        except Exception as e:
            print(f"connect Error, {e}")
            self.close() if self.__client_socket is not None else None

    def sendAndRecv(self, data: str, command_type: int) -> str:
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
            if command_type != self.INSERT and command_type != self.SELECT and command_type != self.UPDATE:
                raise ValueError
            recv_msg = ""
            self.__client_socket.send(f"{data}:{command_type}".encode())
            recv_msg = self.__client_socket.recv(1024)
        except ValueError as e:
            print("command type이 잘못되었습니다!")
            raise e
        except Exception as e:
            print(
                f"""Error! {e}
                소켓 이외의 개체에 작업을 시도했을 경우 소켓이 닫혀있는 경우이므로 소켓을 다시 생성하여 주세요.
                그 외일 경우 close() 메소드를 불러 종료하세요.
                """)
        finally:
            return recv_msg.decode() if recv_msg else recv_msg

    def close(self) -> None:
        """
        서버와 연결을 종료시켜줍니다. 서버와 데이터 주고받는 것을 끝내고 난 후 반드시 불러와야합니다.
        """
        try:
            if self.__client_socket is None:
                raise TypeError
            elif self.__client_socket._closed:
                print("Already closed socket!!!!!!!")
                print(self.__client_socket)
                raise ValueError
            else:
                self.__client_socket.close()

        except Exception as e:
            print(f"Close Error, {e}")


class Server():
    """
    Server Model
    """

    def __init__(self, serv_port: int = 12000) -> None:
        self.__serv_port = serv_port
        self.__serv_socket = None
        self.__conn_socket = None
        self.__init_server()

    def __del__(self) -> None:
        try:
            self.close()
        except Exception as e:
            print(f"destructor, delete Error! {e}")

    def __init_server(self) -> None:
        """
        서버 세팅 메소드입니다.
        """
        try:
            self.__serv_socket = socket(AF_INET, SOCK_STREAM)
            self.__serv_socket.bind(("", self.__serv_port))
            self.__serv_socket.listen()
        except Exception as e:
            print(f"init error, {e}")
            self.__close_serv_socket()
            raise e

    def connect(self) -> None:
        """
        client와 통신할 때 사용하며
        client로부터 받아온 데이터를 가지고 내부적으로 처리되어
        client에게 다시 보내집니다.
        """
        try:
            self.__conn_socket, addr = self.__serv_socket.accept()
            sentence = self.__conn_socket.recv(1024).decode()
            print(f"Received from ({addr[0]}), Message: '{sentence}'")

            """
            {data}:{type} 형식의 값을 받아옴



            codes to communicate
            """

            self.__conn_socket.send("Hello, Client?".encode())
        except Exception as e:
            print(f"Error! {e}")
            self.close()

    def __process(self):
        """
        클라이언트로 받아온 값을 처리합니다.


        """

    def __close_conn_socket(self) -> None:
        """
        accept된 connection socket을 닫아 연결을 종료합니다.
        """
        try:
            if self.__conn_socket is None:
                raise TypeError
            elif self.__conn_socket._closed:
                print("Already closed socket!!!!!!!")
                raise ValueError
            else:
                self.__conn_socket.close()

        except Exception as e:
            print(f"Client Socket Close Error, {e}")

    def __close_serv_socket(self) -> None:
        """
        서버 소켓을 닫아 통신을 종료합니다. 
        """
        try:
            if self.__serv_socket is None:
                raise TypeError
            elif self.__serv_socket._closed:
                print("Already closed socket!!!!!!!")
                raise ValueError
            else:
                self.__serv_socket.close()

        except Exception as e:
            print(f"Server Socket Close Error, {e}")

    def close(self) -> None:
        """
        모든 소켓을 닫습니다. 데이터 주고받는 것을 끝내고 난 후 반드시 불러와야합니다.
        """
        self.__close_conn_socket()
        self.__close_serv_socket()
