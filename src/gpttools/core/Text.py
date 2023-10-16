import os
import tempfile

from pdfminer.high_level import extract_text
from utils import File, Log, hashx

from gpttools.apps import web_utils

log = Log('Text')
LEN_HASH = 16


class Text:
    def __init__(self, content: str):
        self.content = content

    @staticmethod
    def get_hash(x) -> str:
        return hashx.md5(x)[:LEN_HASH]

    @property
    def id(self) -> str:
        return Text.get_hash(self.content)

    @staticmethod
    def get_file_path(id) -> str:
        return os.path.join(tempfile.gettempdir(), f'text.{id}.txt')

    @property
    def file_path(self) -> str:
        return Text.get_file_path(self.id)

    def serialize(self):
        File(self.file_path).write(self.content)
        log.info(f'Saved text to {self.file_path}')

    @staticmethod
    def from_id(id):
        file_path = Text.get_file_path(id)
        content = File(file_path).read()
        return Text(content)

    @staticmethod
    def from_content(content):
        t = Text(content)
        t.serialize()
        return t

    @staticmethod
    def from_txt(file_path):
        return Text.from_content(File(file_path).read())

    @staticmethod
    def from_pdf(file_path):
        return Text.from_content(extract_text(file_path))

    @staticmethod
    def from_url(url):
        return Text.from_content(web_utils.get_url_text(url))

    @staticmethod
    def from_x(x):
        if x.endswith('.pdf'):
            return Text.from_pdf(x)
        elif x.endswith('.txt'):
            return Text.from_txt(x)
        elif x.startswith('http'):
            return Text.from_url(x)
        return Text.from_content(x)

    def summarize(self):
        pass