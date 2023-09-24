import os

import openai
from utils import Log

from gpttools.core.Message import Message
import re

log = Log('ChatWrapper')


def clean(x):
    x = x.replace('\n', ' ')
    x = re.sub(r'\s+', ' ', x)
    return x.strip()


class ChatWrapper:
    def __init__(self, temperature=0):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.temperature = temperature
        self.messages = []

    def append_message(self, role: str, content: str):
        assert role in ['user', 'system', 'assistant']
        self.messages.append(Message(role=role, content=content).todict())

    def append_system_message(self, content: str):
        content = clean(content)
        print(f'\n💻system:\n{content}\n')
        self.append_message('system', content)

    def append_user_message(self, content: str):
        n_content = len(content)
        print(f'\n👩user:\n{content[:100]} \n({n_content=:,} chars)\n')
        self.append_message('user', content)

    def append_assistant_message(self, content: str):
        print(f'\n🤖assistant:\n{content}\n')
        self.append_message('assistant', content)

    @property
    def n_messages(self):
        return len(self.messages)

    def send(self) -> str:
        log.debug(f'{self.n_messages=}')
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=self.messages,
            temperature=self.temperature,
        )
        response_content = response['choices'][0]['message']['content']
        n_response_content = len(response_content)
        log.debug(f'{n_response_content=:,}')
        self.append_assistant_message(response_content)
        return response_content
