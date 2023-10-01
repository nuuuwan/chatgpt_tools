from enum import Enum


class ChatRole(str, Enum):
    user = 'user'
    system = 'system'
    assistant = 'assistant'
    function = 'function'
