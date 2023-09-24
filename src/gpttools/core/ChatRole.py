from enum import Enum


class ChatRole(str, Enum):
    user = 'user'
    system = 'system'
    assistant = 'assistant'
    function = 'function'

    @staticmethod
    def get_emoji(role: 'ChatRole') -> str:
        if role == ChatRole.user:
            return '👩'
        if role == ChatRole.system:
            return '💻'
        if role == ChatRole.assistant:
            return '🤖'
        if role == ChatRole.function:
            return '🧬'
        raise ValueError(f'Unknown role: {role}')
