import os
import tempfile

from gtts import gTTS
from pdfminer.high_level import extract_text
from utils import File, Log

from gpttools.apps import web_utils
from gpttools.core.Chat import Chat

log = Log('Text')


class Text:
    def __init__(self, label: str, content: str):
        self.label = label
        self.content = content

    @property
    def n_characters(self):
        return len(self.content)

    @property
    def n_words(self):
        return len(self.content.split(' '))

    @property
    def n_paragraphs(self):
        return len(self.content.split('\n\n'))

    def __len__(self):
        return self.n_chars

    def __str__(self):
        return f'{self.label}({self.n_characters:,}c, {self.n_words:,}w, {self.n_paragraphs:,}p)'

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def get_file_path(label) -> str:
        return os.path.join(tempfile.gettempdir(), f'text.{label}.txt')

    @property
    def file_path(self) -> str:
        return Text.get_file_path(self.label)

    def serialize(self):
        File(self.file_path).write(self.content)
        log.info(f'Serialized {self} to {self.file_path}')

    @staticmethod
    def from_id(id):
        file_path = Text.get_file_path(id)
        content = File(file_path).read()
        return Text(content)

    @staticmethod
    def from_content(label, content):
        t = Text(label, content)
        t.serialize()
        return t

    @staticmethod
    def from_txt(label, file_path):
        return Text.from_content(label, File(file_path).read())

    @staticmethod
    def from_pdf(label, file_path):
        return Text.from_content(label, extract_text(file_path))

    @staticmethod
    def from_url(label, url):
        return Text.from_content(label, web_utils.get_url_text(url))

    @staticmethod
    def from_x(label, x):
        if x.endswith('.pdf'):
            return Text.from_pdf(label, x)
        elif x.endswith('.txt'):
            return Text.from_txt(label, x)
        elif x.startswith('http'):
            return Text.from_url(label, x)
        return Text.from_content(label, x)

    def summarize(self):
        cmd = 'summary'

        def cmd_func():
            c = Chat()
            c.append_system_message('Summarize the following text:')
            c.append_user_message(self.content)
            return c.send()

        return self.do(cmd, cmd_func)

    def do(self, cmd: str, cmd_func: callable):
        new_label = self.label + '.' + cmd
        file_path = Text.get_file_path(new_label)
        if os.path.exists(file_path):
            new_content = File(file_path).read()
        else:
            new_content = cmd_func()

        t = Text.from_content(new_label, new_content)
        log.info(f'{cmd}({self}) => {str(t)}')
        return t

    def speak(self):
        audio_path = self.file_path + '.mp3'
        if os.path.exists(audio_path):
            log.info(f'Audio file already exists: {audio_path}')
            return

        log.debug(f'Synthesizing {str(self)}...')
        text = self.content
        tts = gTTS(text, lang='en', tld='co.uk')

        tts.save(audio_path)
        log.info(f'Synthesized {str(self)} to {audio_path}')


if __name__ == '__main__':
    t = Text.from_x('sample', os.path.join('tests', 'sample.txt'))
    t.summarize().speak()
