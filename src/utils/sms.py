from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

# pip install coolsms_python_sdk


class SMS():
    """
    sms 발송을 위한 class
    """

    def __init__(self, to, text, imagePath):
        """
        to : 수신인 번호 "01012345678"
        text : 보낼 메시지
        imagePath : 보낼 이미지 경로 + 이미지 명 "./imgage/test.png"
        """
        self.__api_key = "NCSGCXJCYRFYIHHE"
        self.__api_secret = "7PROMFEBKFN3TXMO7RPKALAWW63DCYK6"
        self.__params = dict()
        self.__params["subject"] = "[QR코드 발급 안내]"
        self.__params["type"] = "mms"  # Message type ( sms, lms, mms, ata )
        self.__params["to"] = to  # Recipients Number "01000000000,01000000001"
        self.__params["from"] = "01026147660"  # Sender number
        self.__params["text"] = text  # Message
        self.__params["image"] = imagePath

        self.cool = Message(self.__api_key, self.__api_secret)

    def sendMessage(self):
        """
        메시지 발송, 성공이면 True, 실패면 False
        """
        try:
            response = self.cool.send(self.__params)
            if response["success_count"] == 1:
                return True
            else:
                return False
        except CoolsmsException as e:
            return False
