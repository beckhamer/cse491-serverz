import sys
from apps import ChatApp

def setup():
    chat_app = ChatApp('./chat/html')
    return chat_app

def teardown():
    pass
