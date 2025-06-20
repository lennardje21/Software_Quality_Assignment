from cryptography.fernet import Fernet
from DataAccess.get_data import GetData


class Cryptography:
    @staticmethod
    def load_key() -> bytes:
        return b'2S7IoFyWfUn4L9RTV_90EX35guvJMEWBOHohIMEAuLs='
    
    def __init__(self):
        key = self.load_key()
        self.cipher = Fernet(key)
    
    def encrypt(self, plaintext: str) -> bytes:
        return self.cipher.encrypt(plaintext.encode('utf-8'))

    def decrypt(self, token: bytes) -> str:
        return self.cipher.decrypt(token).decode('utf-8')
