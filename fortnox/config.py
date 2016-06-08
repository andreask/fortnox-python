# coding=utf-8


class Config:
    def __init__(self):
        self.access_token = None
        self.client_secret = None
        self.content_type = 'application/json'
        self.accept = 'application/json'

    def to_dict(self):
        return {
            "Access-Token": self.access_token,
            "Client-Secret": self.client_secret,
            "Content-Type": self.content_type,
            "Accept": self.accept
        }

fortnox_config = Config()
