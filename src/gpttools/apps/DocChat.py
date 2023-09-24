import os

from utils import Log

from gpttools.apps.DocChatBase import DocChatBase

log = Log('DocChat')


class DocChat(DocChatBase):
    @staticmethod
    def get_desktop_paths() -> list[str]:
        dir_desktop = os.getenv("DIR_DESKTOP")
        file_paths = []
        for name_only in os.listdir(dir_desktop):
            if not name_only.endswith(".txt"):
                continue
            if name_only.endswith(".log"):
                continue
            file_path = os.path.join(dir_desktop, name_only)
            file_paths.append(file_path)
        return file_paths

    @staticmethod
    def list_from_desktop() -> list['DocChat']:
        desktop_file_paths = DocChat.get_desktop_paths()
        return [DocChat(file_path) for file_path in desktop_file_paths]
