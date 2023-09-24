import math
from functools import cached_property

from utils import Log

from gpttools.apps.DocCommands import (CMD_POSTAMBLE, CMD_PREAMBLE,
                                       get_cmd_summarize)
from gpttools.core.Chat import Chat

CHARS_PER_BULLET = 1_000
MAX_BATCH_LEN = 15_000

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

    @cached_property
    def summary(self) -> str:
        summary = ''
        for chunk in self.chunks:
            self.append_system_message(CMD_PREAMBLE)
            self.append_user_message(chunk)
            self.append_system_message(CMD_POSTAMBLE)

            n_bullets = math.ceil(len(chunk) / CHARS_PER_BULLET)
            self.append_system_message(get_cmd_summarize(n_bullets))
            chunk_summary = self.send()
            summary += chunk_summary
        return summary
