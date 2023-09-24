import os
import re

import openai
from utils import Log

from gpttools.core.ChatRole import ChatRole
from gpttools.core.Message import Message

log = Log('ChatWrapper')


def clean(x):  # TODO: Move
    x = x.replace('\n', ' ')
    x = re.sub(r'\s+', ' ', x)
    return x.strip()


DEFAULT_OPTIONS = dict(
    temperature=0.1,
)
DEFAULT_MODEL = 'gpt-4'


class Chat:
    def __init__(self, model: str = DEFAULT_MODEL, options: dict = {}):
        openai.api_key = os.getenv("OPENAI_API_KEY")  # noqa
        self.model = model
        self.options = DEFAULT_OPTIONS | options
        log.debug(f'{self.model=}, {self.options=}')
        self.messages = []

    @property
    def n_messages(self):
        return len(self.messages)

    def append_message(self, role: ChatRole, content: str):
        self.messages.append(Message(role=role, content=content).todict())

    def append_system_message(self, content: str):
        content = clean(content)
        self.append_message(ChatRole.system, content)

    def append_user_message(self, content: str):
        len(content)
        self.append_message(ChatRole.user, content)

    def append_assistant_message(self, content: str):
        self.append_message(ChatRole.assistant, content)

    def send(self) -> str:
        log.debug(f'{self.n_messages=}')

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            **self.options,
        )
        response_content = response['choices'][0]['message']['content']
        n_response_content = len(response_content)
        log.debug(f'{n_response_content=:,}')
        self.append_assistant_message(response_content)
        return response_content
