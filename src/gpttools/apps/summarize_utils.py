import math

from utils import Log

from gpttools.core.Chat import ChatWrapper

log = Log('summarize_utils')

MIN_BATCH_LEN = 10
MAX_BATCH_LEN = 15_000

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


def summarize_text(text: str):
    n_bullets = math.ceil(len(text) / CHARS_PER_BULLET)
    log.debug(f'{n_bullets=:,}')
    chat = ChatWrapper()

    chat.append_system_message(CMD_PREAMBLE)
    chat.append_user_message(text)
    chat.append_system_message(CMD_POSTAMBLE)

    chat.append_system_message(get_cmd_summarize(n_bullets))
    chat.send()
    chat.append_system_message(CMD_PRETTIFY)
    return chat.send()


def summarize_content(content):
    n_content = len(content)
    e_batches = int(n_content / MAX_BATCH_LEN)
    max_batch_len = int(n_content / (e_batches + 1)) + 500
    log.debug(f'{max_batch_len=:,}, {MAX_BATCH_LEN=:,}')

    batches = batch_content(content, max_batch_len)
    n_batches = len(batches)

    summarized_content = ''
    for i_batch, batch in enumerate(batches):
        if len(batch.strip()) < MIN_BATCH_LEN:
            continue
        summarized_batch = summarize_text(batch)
        log.debug(
            f"Summarized batch {i_batch + 1}/{n_batches}:"
            + f" {len(batch):,}B -> {len(summarized_batch):,}B"
        )

        summarized_content += summarized_batch + '\n...\n'

    return 'Summary (by #ChatGPT)\n\n' + summarized_content


def batch_content(content: str, max_batch_len: int):
    paragraphs = content.split("\n")
    batches = ['']
    for paragraph in paragraphs:
        if len(batches[-1]) + len(paragraph) < max_batch_len:
            batches[-1] += paragraph + "\n"
        else:
            batches.append('')
            batches[-1] = paragraph + "\n"
    return batches
