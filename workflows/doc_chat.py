from gpttools import DocChat


def main():
    print('')
    print('-' * 64)
    print('DOC CHAT')
    print('-' * 64)
    doc_chat_list = DocChat.list_from_desktop()
    if len(doc_chat_list) == 0:
        print('No documents found on desktop')
        return False

    if len(doc_chat_list) == 1:
        doc_chat = doc_chat_list[0]
    else:
        print('Choose a document:')
        for i, doc_chat in enumerate(doc_chat_list):
            print(f'{i + 1}. {doc_chat.file_path}')
        try:
            choice = int(input('Choice: '))
            doc_chat = doc_chat_list[choice - 1]
        except BaseException:
            return False

    doc_chat.run()
    print('-' * 64)
    return True


if __name__ == '__main__':
    main()
