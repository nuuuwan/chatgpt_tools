import os
import re
import time

import openai
from utils import Log

from gpttools.core.ChatRole import ChatRole
from gpttools.core.Message import Message

log = Log('Chat')


def clean(x):  # TODO: Move
    x = x.replace('\n', ' ')
    x = re.sub(r'\s+', ' ', x)
    return x.strip()


DEFAULT_OPTIONS = dict(
    temperature=0.1,
)

# DEFAULT_MODEL = 'gpt-3.5-turbo'
# MAX_TOKEN_SIZE = 2**12

DEFAULT_MODEL = 'gpt-4'
MAX_TOKEN_SIZE = 2 ** 16

MAX_BATCH_LEN = 2 ** 12


class Chat:
    def __init__(self, model: str = DEFAULT_MODEL, options: dict = {}):
        openai.api_key = os.getenv("OPENAI_API_KEY")  # noqa
        self.model = model
        self.options = DEFAULT_OPTIONS | options
        log.debug(f'{self.model=}, {self.options=}')
        self.messages = []
        self.token_size = 0

    @property
    def n_messages(self):
        return len(self.messages)

    def prune_messages(self):
        while self.token_size > MAX_TOKEN_SIZE:
            message = self.messages[0]
            self.messages = self.messages[1:]
            self.token_size -= len(message['content'])
            log.debug(f'{self.token_size=:,} (pruned)')

    def append_message(self, role: ChatRole, content: str):
        self.token_size += len(content)
        self.messages.append(Message(role=role, content=content).todict())
        log.debug(f'{self.token_size=:,}')
        self.prune_messages()

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
        t = 1
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=self.messages,
                    **self.options,
                )
                break
            except Exception as e:
                log.error(e)
                log.debug(f'Sleeping😴 for {t}s...')
                time.sleep(t)
                t *= 2

        response_content = response['choices'][0]['message']['content']
        n_response_content = len(response_content)
        log.debug(f'{n_response_content=:,}')
        self.append_assistant_message(response_content)
        return response_content
