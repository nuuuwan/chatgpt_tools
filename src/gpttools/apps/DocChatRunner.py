import shlex

from utils import Log

from gpttools.apps.DocChat import DocChat

log = Log('DocChatRunner')


class DocChatRunner:
    @staticmethod
    def is_quit(input_text: str) -> bool:
        return input_text.strip() in ['exit', 'quit', 'x', 'q']

    @staticmethod
    def is_empty(input_text: str) -> bool:
        return len(input_text.strip()) < 3

    @staticmethod
    def run_with_doc_chat(doc_chat, input_text):
        doc_chat.append_log(input_text)
        assistant_response = doc_chat.do(input_text)
        doc_chat.speak(assistant_response)
        doc_chat.finish(assistant_response)
        doc_chat.append_log(assistant_response)
        
    @staticmethod
    def run(file_path: str):
        if file_path:
            doc_chat = DocChat.load(file_path)
            log = Log('DocChat')
        else:
            doc_chat = None
            log = Log('DocChatRunner')

        while True:
            log.info('')
            input_text = input('> ')

            if DocChatRunner.is_quit(input_text):
                break

            if DocChatRunner.is_empty(input_text):
                continue

            print(' ')

            tokens = shlex.split(input_text, posix=False)
            cmd_token = tokens[0]
            if cmd_token == 'load':
                source = tokens[1].replace('"', '').strip()
                doc_chat = DocChat.load(source)
                log = Log(doc_chat.short_name)
                continue

            if not doc_chat:
                continue

            DocChatRunner.run_with_doc_chat(doc_chat, input_text)
