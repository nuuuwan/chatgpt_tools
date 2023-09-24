import math
from functools import cached_property

from gpttools.core.Chat import ChatWrapper

CHARS_PER_BULLET = 1_000

CMD_PREAMBLE = '''
The following is a part from a document:
'''

CMD_POSTAMBLE = '''
You will be asked a set of questions about the part.
'''


def get_cmd_summarize(n_bullets: int):
    return f'''
Summarize into {n_bullets} unnumbered bullet points,
including a space after each bullet paragraph.
        '''


CMD_PRETTIFY = '''
In your summary, append emojis next to words,
replace each bullet with an emoji that represents the bullet's content,
and replace words with hashtags and handles
        '''


MAX_BATCH_LEN = 15_000


class DocChat(ChatWrapper):
    def __init__(self, content: str):
        self.content = content

    def __len__(self):
        return len(self.content)

    @cached_property
    def chunks(self) -> list[str]:
        content_size = len(self)
        n_batches = math.ceil(content_size / MAX_BATCH_LEN)
        avg_batch_size = int(content_size / n_batches)
        chunks = ['']
        for line in self.content.splitlines():
            if len(child[-1]) > avg_batch_size:
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
