import os

from utils import File, Log

from gpttools.apps.DocChatBase import DocChatBase

log = Log('DocChat')


class DocChat(DocChatBase):
    @staticmethod
    def from_file(file_path) -> 'DocChat':
        content = File(file_path).read()
        doc_chat = DocChat(content)
        log.info(f'Loaded {file_path}')
        return doc_chat

    @staticmethod
    def get_desktop_paths() -> list[str]:
        dir_desktop = os.getenv("DIR_DESKTOP")
        paths = []
        for name_only in os.listdir(dir_desktop):
            if not name_only.endswith(".txt"):
                continue
            if "summary." in name_only:
                continue
            path = os.path.join(dir_desktop, name_only)
            paths.append(path)
        return paths

    @staticmethod
    def list_from_desktop() -> list['DocChat']:
        desktop_paths = DocChat.get_desktop_paths()
        return [DocChat.from_file(path) for path in desktop_paths]
