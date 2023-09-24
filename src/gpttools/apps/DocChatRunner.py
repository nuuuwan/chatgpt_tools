import os

from gpttools.apps.DocChat import DocChat
from utils import Log

log = Log('DocChatRunner')


class DocChatRunner:
    @staticmethod
    def is_quit(input_text: str) -> bool:
        return input_text.strip() in ['exit', 'quit', 'x', 'q']

    @staticmethod
    def is_empty(input_text: str) -> bool:
        return len(input_text.strip()) < 3

    @staticmethod
    def is_refresh(input_text: str) -> bool:
        return input_text.strip() in ['refresh', 'ref']

    @staticmethod
    def load_doc_chat() -> DocChat:
        doc_chat_list = DocChat.list_from_desktop()

        if len(doc_chat_list) == 0:
            print('No documents found on desktop')
            return None

        if len(doc_chat_list) == 1:
            return doc_chat_list[0].prep()

        print('Choose a document:')
        for i, doc_chat in enumerate(doc_chat_list):
            name_only = os.path.split(doc_chat.file_path)[-1][:-4]
            print(f'\t{i + 1}. {name_only}')
        print()
        try:
            choice = int(input(f'[1-{len(doc_chat_list)}]? '))
            return doc_chat_list[choice - 1].prep()
        except BaseException:
            return None

    @staticmethod
    def run_with_doc_chat(doc_chat, input_text):
        doc_chat.append_log(input_text)
        assistant_response = doc_chat.do(input_text)
        doc_chat.finish(assistant_response)
        doc_chat.append_log(assistant_response)

    @staticmethod
    def run():
        doc_chat = None
        while True:
            if not doc_chat:
                doc_chat = DocChatRunner.load_doc_chat()

            if not doc_chat:
                break

            print()
            input_text = input(doc_chat.short_name + '> ')
            print()

            if DocChatRunner.is_quit(input_text):
                break

            if DocChatRunner.is_empty(input_text):
                continue

            if DocChatRunner.is_refresh(input_text):
                doc_chat = None
                continue

            DocChatRunner.run_with_doc_chat(doc_chat, input_text)
