from enum import StrEnum


class ChatRole(StrEnum):
    user = 'user'
    system = 'system'
    assistant = 'assistant'
    # function = 'function'
