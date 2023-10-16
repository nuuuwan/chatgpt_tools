import math
import os
from functools import cached_property

from pdfminer.high_level import extract_text
from utils import File, Log, get_date_id, hashx

from gpttools.apps import web_utils
from gpttools.apps.DocCommands import (CMD_POSTAMBLE, CMD_PREAMBLE,
                                       CMD_PRETTIFY, get_cmd_summarize)
from gpttools.base.FileLogger import FileLogger
from gpttools.core.Chat import MAX_BATCH_LEN, Chat

CHARS_PER_BULLET = 1_000
MIN_SIZE_FOR_PREP_BIG = 10_000

log = Log('DocChat')


class DocChat(Chat, FileLogger):
    @staticmethod
    def load(file_path) -> 'DocChat':
        ext = os.path.splitext(file_path)[-1]
        if ext in ['.txt', '.md', '.log']:
            return DocChat.load_txt(file_path)
        elif ext in ['.pdf']:
            return DocChat.load_pdf(file_path)
        elif file_path.startswith('http'):
            return DocChat.load_http(file_path)
        else:
            raise ValueError(f'Unsupported file extension: {ext}')

    @staticmethod
    def load_txt(file_path) -> 'DocChat':
        content = File(file_path).read()
        log.debug(f'Loaded {file_path} ({len(content):,}B)')
        return DocChat(file_path, content)

    @staticmethod
    def load_pdf(file_path) -> 'DocChat':
        txt_file_path = file_path + '.txt'
        if not os.path.exists(txt_file_path):
            content = extract_text(file_path)
            log.debug(f'Loaded {file_path} ({len(content):,}B)')
            File(txt_file_path).write(content)

        else:
            content = File(txt_file_path).read()
            log.debug(f'Loaded {file_path} ({len(content):,}B)')
        file_path = txt_file_path
        return DocChat(file_path, content)

    @staticmethod
    def load_http(file_path) -> 'DocChat':
        domain = file_path.split('/')[2]
        h = hashx.md5(file_path)[:6]
        dir_desktop = os.getenv('DIR_DESKTOP')
        txt_file_path = os.path.join(dir_desktop, f'{domain}.{h}.txt')
        if not os.path.exists(txt_file_path):
            content = web_utils.get_url_text(file_path)
            log.debug(f'Loaded {file_path} ({len(content):,}B)')
            File(txt_file_path).write(content)
        else:
            content = File(txt_file_path).read()
            log.debug(f'Loaded {file_path} ({len(content):,}B)')
        file_path = txt_file_path
        return DocChat(file_path, content)

    def __init__(self, file_path: str, content: str):
        Chat.__init__(self)
        FileLogger.__init__(self, file_path + f'.{get_date_id()}.md')
        self.file_path = file_path
        self.content = content
        if len(self.content) > MIN_SIZE_FOR_PREP_BIG:
            self.prep_big()
        else:
            self.prep()

    @cached_property
    def short_name(self):
        return os.path.basename(self.file_path)

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

    def prep_big(self):
        SUMMARY_DELIM = '\n...\n'
        file_path_new = self.file_path + '.prep_big.txt'

        if os.path.exists(file_path_new):
            content_new = File(file_path_new).read()
            summary_list = content_new.split(SUMMARY_DELIM)
            log.info(f'Loaded {len(content_new):,}B from {file_path_new}')
        else:
            N_BULLETS_PREP_BIG = 5
            summary_list = []
            n_chunks = len(self.chunks)
            for i_chunk, chunk in enumerate(self.chunks):
                log.debug(f'Running prep_big on {i_chunk + 1}/{n_chunks} chunks')
            
                self.append_system_message(CMD_PREAMBLE)
                self.append_user_message(chunk)
                self.append_system_message(
                    get_cmd_summarize(N_BULLETS_PREP_BIG)
                )
                summary = self.send()
                summary_list.append(summary)
                self.cleanup()

            content_new = SUMMARY_DELIM.join(summary_list)
            File(file_path_new).write(content_new)
            log.info(f'Wrote {len(content_new):,}B to {file_path_new}')
            
        self.content = content_new
        self.file_path = file_path_new
        return self.prep()

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
