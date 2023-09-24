import unittest

from gpttools.apps.DocChatBase import MAX_BATCH_LEN, DocChatBase


class TestDocChatBase(unittest.TestCase):
    def setUp(self):
        self.content = 'This is a test document.\nIt has multiple lines.\n'
        self.doc_chat = DocChatBase(self.content)

    def test_create_doc_chat_base(self):
        self.assertEqual(self.doc_chat.content, self.content)
        self.assertEqual(len(self.doc_chat), len(self.content))
        self.assertEqual(
            self.doc_chat.chunks,
            ['This is a test document.\nIt has multiple lines.\n'],
        )

    def test_chunks(self):
        dummy_chunk = 'a' * (MAX_BATCH_LEN - 10)
        self.doc_chat.content = dummy_chunk + '\n' + dummy_chunk
        self.assertEqual(len(self.doc_chat.chunks), 2)
        self.assertLessEqual(len(self.doc_chat.chunks[0]), 15_000)
        self.assertLessEqual(len(self.doc_chat.chunks[1]), 15_000)


if __name__ == '__main__':
    unittest.main()
