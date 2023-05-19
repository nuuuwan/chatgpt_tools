from utils import Log

from gpttools.core.ChatWrapper import ChatWrapper

log = Log('summarize_utils')

MIN_BATCH_LEN = 10
MAX_BATCH_LEN = 15_000

BULLETS_PER_SUMMARY = 10


def summarize_text(text):
    chat = ChatWrapper()
    system_command = f'''
You are a summarization assistant.

Given  a long article, you do ALL of the following:
- list the {BULLETS_PER_SUMMARY} most important ideas and numbers,
each in a short sentence,
- mark bullets with a 💡icon.
- replace ALL relavent words with their twitter handle
    (e.g. replace "IMF" with "@IMF")
    or hashtags (e.g. replace "China" with "#China").

Do you understand?
        '''
    chat.send_system(system_command)
    return chat.send_user(text)


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

    return 'TL;DR (by #ChatGPT)\n\n' + summarized_content


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
