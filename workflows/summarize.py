from gpttools import DocChat


def main():
    print('-' * 64)
    print('DOC CHAT')
    print('-' * 64)
    doc_chat = DocChat.list_from_desktop()[0]
    doc_chat.run()
    print('-' * 64)


if __name__ == '__main__':
    main()
