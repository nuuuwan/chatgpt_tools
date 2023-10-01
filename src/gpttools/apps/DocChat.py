import math
import os
from functools import cached_property

from pdfminer.high_level import extract_text
from utils import File, Log, get_date_id

from gpttools.apps.DocCommands import (CMD_POSTAMBLE, CMD_PREAMBLE,
                                       CMD_PRETTIFY, get_cmd_summarize)
from gpttools.base.FileLogger import FileLogger
from gpttools.core.Chat import MAX_BATCH_LEN, Chat

CHARS_PER_BULLET = 1_000


log = Log('DocChat')


class DocChat(Chat, FileLogger):
    def __init__(self, file_path: str):
        Chat.__init__(self)
        FileLogger.__init__(self, file_path + f'.{get_date_id()}.log')
        self.file_path = file_path

    @cached_property
    def emoji(self):
        ext = os.path.splitext(self.file_path)[-1]
        if ext in ['.txt', '.md', '.log']:
            return '📄'
        elif ext in ['.pdf']:
            return '🅿️'
        else:
            raise ValueError(f'Unsupported file extension: {ext}')

    @cached_property
    def short_name(self):
        return self.emoji + os.path.basename(self.file_path)

    @cached_property
    def content(self) -> str:
        ext = os.path.splitext(self.file_path)[-1]
        if ext in ['.txt', '.md', '.log']:
            content = File(self.file_path).read()
        elif ext in ['.pdf']:
            txt_file_path = self.file_path + '.txt'
            if os.path.exists(txt_file_path):
                return File(txt_file_path).read()
            else:
                content = extract_text(self.file_path)
                File(txt_file_path).write(content)
                self.file_path = txt_file_path
        else:
            raise ValueError(f'Unsupported file extension: {ext}')

        log.debug(f'Loaded {self.file_path} ({len(content):,}B)')
        return content

    @cached_property
    def chunks(self) -> list[str]:
        content_size = len(self.content)
        n_batches = math.ceil(content_size / MAX_BATCH_LEN)
        avg_batch_size = int(content_size / n_batches)
        log.debug(f'{content_size=}, {n_batches=}, {avg_batch_size=}')

        chunks = ['']
        for line in self.content.splitlines():
            if len(chunks[-1]) > avg_batch_size:
                chunks.append('')
            chunks[-1] += line + '\n'
        return chunks

    def prep(self):
        self.append_system_message(CMD_PREAMBLE)
        for chunk in self.chunks:
            self.append_user_message(chunk)
        self.append_system_message(CMD_POSTAMBLE)
        log.debug('Prep done.')
        return self

    def do_prettify(self):
        log.debug('Prettifying...')
        self.append_system_message(CMD_PRETTIFY)
        return self.send()

    def do_summarize(self):
        log.debug('Summarizing...')
        n_bullets = len(self.content) / CHARS_PER_BULLET
        self.append_system_message(get_cmd_summarize(n_bullets))
        return self.send()

    def do_generic(self, input_text):
        self.append_user_message(input_text)
        return self.send()

    def finish(self, assistant_response):
        print(' ')
        print(assistant_response)
        print(' ')

    def do(self, input_text):
        for func, cmd_list in [
            (self.do_prettify, ['pretty', 'prettify']),
            (self.do_summarize, ['sum', 'summary', 'summarize']),
        ]:
            if input_text.strip() in cmd_list:
                return func()

        return self.do_generic(input_text)
