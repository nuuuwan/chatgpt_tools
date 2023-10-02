import sys

from gpttools.apps.DocChatRunner import DocChatRunner


def main(file_path: str):
    DocChatRunner.run(file_path)


if __name__ == '__main__':
    file_path = sys.argv[-1] if len(sys.argv) > 1 else None
    main(file_path)
