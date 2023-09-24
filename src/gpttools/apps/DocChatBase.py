import math
import os
from functools import cached_property

from utils import File, Log

from gpttools.apps.DocCommands import (
    CMD_POSTAMBLE,
    CMD_PREAMBLE,
    CMD_PRETTIFY,
    get_cmd_summarize,
)
from gpttools.core.Chat import MAX_BATCH_LEN, Chat
from gpttools.core.ChatRole import ChatRole

CHARS_PER_BULLET = 1_000


log = Log('DocChatBase')


class DocChatBase(Chat):
    def __init__(self, file_path: str):
        Chat.__init__(self)
        self.file_path = file_path
        self.content = File(file_path).read()
        log.info(f'Loaded {file_path} ({len(self):,} chars)')
        self.log_lines = []

    @cached_property
    def log_file_path(self):
        tokens = list(os.path.split(self.file_path))
        tokens[-1] = 'log.' + tokens[-1]
        return os.path.join(*tokens)

    def write_log(self):
        File(self.log_file_path).write_lines(self.log_lines)
        log.debug(
            f'Wrote to {self.log_file_path} ({len(self.log_lines):,} lines)'
        )

    def append_log(self, line: str):
        self.log_lines.append(line)
        self.log_lines.append('...')
        self.write_log()

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
        return self.send()

    def do_generic(self, input_text):
        self.append_user_message(input_text)
        return self.send()

    def finish(self, assistant_response):
        print(
            ChatRole.get_emoji(ChatRole.assistant) + ': ' + assistant_response
        )

    def run(self) -> str:
        self.append_system_message(CMD_PREAMBLE)
        for chunk in self.chunks:
            self.append_user_message(chunk)
        self.append_system_message(CMD_POSTAMBLE)

        while True:
            print()
            input_text = input('> ')
            self.append_log(input_text)
            print()

            if input_text.strip() == '':
                continue

            if input_text.strip() in ['exit', 'quit', 'x', 'q']:
                break

            if input_text.strip() in ['sum', 'summary', 'summarize']:
                assistant_response = self.do_summarize()
            else:
                assistant_response = self.do_generic(input_text)

            self.finish(assistant_response)
            self.append_log(assistant_response)
