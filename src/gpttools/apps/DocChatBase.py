import math
import os
import tempfile
from functools import cached_property

from utils import File, Log

from gpttools.apps.DocCommands import (CMD_POSTAMBLE, CMD_PREAMBLE,
                                       CMD_PRETTIFY, get_cmd_summarize)
from gpttools.core.Chat import MAX_BATCH_LEN, Chat
from gpttools.core.ChatRole import ChatRole

CHARS_PER_BULLET = 1_000


log = Log('DocChatBase')


class DocChatBase(Chat):
    def __init__(self, content: str):
        Chat.__init__(self)
        self.content = content

    def __len__(self):
        return len(self.content)

    @cached_property
    def chunks(self) -> list[str]:
        content_size = len(self)
        n_batches = math.ceil(content_size / MAX_BATCH_LEN)
        avg_batch_size = int(content_size / n_batches)
        log.debug(f'{content_size=}, {n_batches=}, {avg_batch_size=}')

        chunks = ['']
        for line in self.content.splitlines():
            if len(chunks[-1]) > avg_batch_size:
                chunks.append('')
            chunks[-1] += line + '\n'
        return chunks

    def do_summarize(self):
        n_bullets = len(self) / CHARS_PER_BULLET
        self.append_system_message(get_cmd_summarize(n_bullets))
        self.send()
        self.append_system_message(CMD_PRETTIFY)
        assistant_response = self.send()

        temp_path = tempfile.NamedTemporaryFile(suffix='.summary.txt').name
        File(temp_path).write(assistant_response)
        log.info(f'Wrote to {temp_path}')
        os.startfile(temp_path)

        return assistant_response

    def finish(self, assistant_response):
        print(
            ChatRole.get_emoji(ChatRole.assistant) + ':' + assistant_response
        )

    def run(self) -> str:
        self.append_system_message(CMD_PREAMBLE)
        for chunk in self.chunks:
            self.append_user_message(chunk)
        self.append_system_message(CMD_POSTAMBLE)

        while True:
            print()
            input_text = input('> ')
            print()

            if input_text.strip() == '':
                continue

            if input_text.strip() in ['exit', 'quit', 'x', 'q']:
                break

            if input_text.strip() in ['sum', 'summary', 'summarize']:
                assistant_response = self.do_summarize()
            else:
                assistant_response = self.append_user_message(input_text)

            self.finish(assistant_response)
