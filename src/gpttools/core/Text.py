import math
import os
import tempfile

from gtts import gTTS
from pdfminer.high_level import extract_text
from utils import File, Log, hashx

from gpttools.apps import web_utils
from gpttools.core.Chat import Chat

log = Log('Text')
DIR_TEXT = os.environ.get('DIR_TEXT', tempfile.gettempdir())
MAX_BATCH_LEN = 20_000
log.debug(f'{DIR_TEXT=}, {MAX_BATCH_LEN=}')


class Text:
    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.content = content

    @property
    def n_characters(self):
        return len(self.content)

    @property
    def n_words(self):
        return len(self.content.split(' '))

    @property
    def n_lines(self):
        return len(self.content.split('\n\n'))

    @property
    def file_path_last(self):
        return self.file_path.split('/')[-1]

    def __len__(self):
        return self.n_characters

    def __str__(self):
        return f'{self.file_path_last}({self.n_characters:,}c, {self.n_words:,}w, {self.n_lines:,}l)'

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def from_txt(file_path):
        return Text(file_path, File(file_path).read())

    @staticmethod
    def from_pdf(pdf_file_path):
        txt_file_path = pdf_file_path + '.txt'
        if not os.path.exists(txt_file_path):
            content = extract_text(pdf_file_path)
            File(txt_file_path).write(content)
        else:
            content = File(txt_file_path).read()
        return Text(pdf_file_path + '.txt', content)

    @staticmethod
    def from_url(url):
        domain = web_utils.get_domain(url)
        hash = hashx.md5(url)[:4]
        txt_file_path = os.path.join(DIR_TEXT, f'{domain}.{hash}.txt')
        if not os.path.exists(txt_file_path):
            content = web_utils.get_url_text(url)
            File(txt_file_path).write(content)
        else:
            content = File(txt_file_path).read()
        return Text(txt_file_path, content)

    @staticmethod
    def from_x(x):
        if x.endswith('.pdf'):
            return Text.from_pdf(x)
        elif x.endswith('.txt'):
            return Text.from_txt(x)
        elif x.startswith('http'):
            return Text.from_url(x)
        raise Exception(f'Unknown data: {x}')

    def get_chunks(self) -> list[str]:
        content_size = len(self.content)
        n_batches = math.ceil(content_size / MAX_BATCH_LEN)
        avg_batch_size = int(content_size / n_batches)
        log.debug(f'{content_size=}, {n_batches=}, {avg_batch_size=}')

        chunks = ['']
        for line in self.content.splitlines():
            if len(chunks[-1]) + len(line) > avg_batch_size:
                chunks.append('')
            chunks[-1] += line + '\n'
        return chunks

    def do_textual_single(self, cmd, cmd_system_message):
        if len(self) > MAX_BATCH_LEN:
            raise Exception(f'{self} is too large!')

        def cmd_func():
            c = Chat()
            c.append_system_message(cmd_system_message)
            c.append_user_message(self.content)
            return c.send()

        return self.do_texual(cmd, cmd_func)

    def do_texual(self, cmd: str, cmd_func: callable):
        new_file_path = self.file_path + '.' + cmd
        new_content = self.do(new_file_path, cmd_func)
        if new_content is None:
            new_content = File(new_file_path).read()
        t = Text(new_file_path, new_content)
        return t

    def summarize(self):
        return self.do_textual_single(
            'summarize.txt', 'Summarize the following text'
        )

    def bullet(self, n_bullets: int):
        return self.do_textual_single(
            f'bullet.{n_bullets}.txt',
            f'Summarize the following text into {n_bullets} bullets.',
        )

    def smaller(self):
        if len(self) < MAX_BATCH_LEN:
            log.warning(f'{self} is already smaller than {MAX_BATCH_LEN}')
            return self
        cmd = 'smaller.txt'

        def cmd_func():
            chunks = self.get_chunks()
            summary_list = []
            for i, chunk in enumerate(chunks):
                chunk_file_path = self.file_path + f'.chunk-{i:03d}.txt'
                File(chunk_file_path).write(chunk)
                t_chunk = Text(chunk_file_path, chunk)
                log.debug(f'{t_chunk} => {chunk_file_path}')
                t_chunk_summary = t_chunk.summarize()
                summary_list.append(t_chunk_summary.content)
            DELIM_CHUNKS = '\n\n...\n\n'
            summary = DELIM_CHUNKS.join(summary_list)
            return summary

        return self.do_texual(cmd, cmd_func)

    def do(self, new_file_path: str, cmd_func: callable):
        result = None
        if not os.path.exists(new_file_path):
            result = cmd_func()
            if result:
                File(new_file_path).write(result)

        log.info(f'{self} => {new_file_path}')
        return result

    def speak(self):
        audio_path = self.file_path + '.speak.mp3'

        def cmd_func():
            log.debug(f'Synthesizing {str(self)}...')
            text = self.content
            tts = gTTS(text, lang='en', tld='co.uk')

            tts.save(audio_path)
            log.info(f'Synthesized {str(self)} to {audio_path}')

        self.do(audio_path, cmd_func)


if __name__ == '__main__':
    # for x in [
    #     os.path.join('tests', 'sample.txt'),
    #     os.path.join('tests', 'sample.pdf'),
    #     'https://www.dailymirror.lk'
    #     + '/top-story'
    #     + '/Israel-Palestine-conflict-MR-says-war-is-not-the-solution'
    #     + '/155-269306',
    # ]:
    #     log.debug(x)
    #     t = Text.from_x(x)
    #     t.summarize().speak()
    #     t.bullet(5).speak()

    t = Text.from_txt(os.path.join('tests', 'sample-large.txt'))
    t.smaller().summarize()
