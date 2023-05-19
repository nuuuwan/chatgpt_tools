from utils import Log

from gpttools.core.ChatWrapper import ChatWrapper

log = Log('summarize_utils')

MIN_BATCH_LEN = 5
MAX_BATCH_LEN = 3_000

BULLETS_PER_SUMMARY = 5


def summarize_text(text):
    chat = ChatWrapper()
    system_command = f'''
You are a summarization assistant.

Given  a long article, you do ALL of the following:
- list the {BULLETS_PER_SUMMARY} most important takeaways in short sentences,
- mark bullets with a 💡icon.
- replace ALL relavent words with their twitter handle
    (e.g. replace "IMF" with "@IMF")
    or hashtags (e.g. replace "China" with "#China").

Do you understand?
        '''
    chat.send_system(system_command)
    return chat.send_user(text)


def summarize_batch(batch):
    summarized_batch = summarize_text(batch)
    n_batch = len(batch)
    n_summarized_batch = len(summarized_batch)
    log.debug(f"Summarizing batch of {n_batch}B -> {n_summarized_batch}B")
    return summarized_batch


def summarize_content(content):
    batches = batch_content(content)
    summarized_content = ''
    for batch in batches:
        if len(batch.strip()) < MIN_BATCH_LEN:
            continue
        summarized_batch = summarize_batch(batch)
        summarized_content += summarized_batch + '\n...\n'
    return summarized_content


def batch_content(content: str):
    paragraphs = content.split("\n")
    batches = ['']
    for paragraph in paragraphs:
        if len(batches[-1]) + len(paragraph) < MAX_BATCH_LEN:
            batches[-1] += paragraph + "\n"
        else:
            batches.append('')
            batches[-1] = paragraph + "\n"
    return batches
