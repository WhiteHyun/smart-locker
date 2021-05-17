from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

# pip install coolsms_python_sdk


class SMS():
    """
    sms 발송을 위한 class
    """

    @classmethod
    def mms(cls, to, text, image_path):
        """MMS를 보내기 위한 객체 생성 메소드입니다.

        Parameter
        ---------
        to: str
            수신인 번호
        text: str
            보낼 메시지

        image_path: str
            보낼 이미지 경로 + 이미지 명

        Returns
        -------
        SMS
            객체생성된 SMS

        Example
        -------
        >>> SMS.mms("01012345678", "메시지 내용", "./image/test.png")
        <class 'sms.SMS'>
        """
        return cls(to=to, text=text, type="mms", image_path=image_path)

    @classmethod
    def sms(cls, to, text):
        """SMS를 보내기 위한 객체 생성 메소드입니다.

        Parameter
        ---------
        to: str
            수신인 번호
        text: str
            보낼 메시지

        Returns
        -------
        SMS
            객체생성된 SMS

        Example
        -------
        >>> SMS.sms("01012345678", "메시지 내용", "./image/test.png")
        <class 'sms.SMS'>
        """
        return cls(to=to, text=text, type="sms")

    def __init__(self, to, text, type, image_path=None):
        """SMS 객체를 만드는 메소드입니다.

        Warnings
        --------
        `classmethod`인 `SMS`나 `MMS`를 사용하여 객체를 만드는 방법을 추천합니다.

        Parameter
        ---------
        to: str
            수신인 번호

        text: str
            보낼 메시지

        type: str
            SMS의 타입

        image_path: str
            보낼 이미지 경로 + 이미지 명

        Returns
        -------
        SMS
            객체생성된 SMS

        Example
        -------
        >>> SMS(to="01012345678", text="test message", type="sms")
        <class 'sms.SMS'>

        >>> SMS(to="01012345678", text="test message", type="mms", image_path="./image/test.png")
        <class 'sms.SMS'>
        """
        self.__api_key = "NCSGCXJCYRFYIHHE"
        self.__api_secret = "7PROMFEBKFN3TXMO7RPKALAWW63DCYK6"
        self.__params = dict()
        self.__params["to"] = to  # Recipients Number "01000000000,01000000001"
        self.__params["from"] = "01026147660"  # Sender number
        self.__params["text"] = text  # Message
        self.__params["type"] = type  # Message type ( sms, lms, mms, ata )

        if type == "mms":
            self.__params["subject"] = "[QR코드 발급 안내]"
            self.__params["image"] = image_path

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
