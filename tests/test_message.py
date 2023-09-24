import unittest

from gpttools import ChatRole, Message


class TestMessage(unittest.TestCase):
    def test_create_message(self):
        message = Message(ChatRole.user, 'Hello, world!')
        self.assertEqual(message.role, ChatRole.user)
        self.assertEqual(message.content, 'Hello, world!')

    def test_message_todict(self):
        message = Message(ChatRole.system, 'Goodbye, world!')
        self.assertEqual(
            message.todict(),
            {'role': ChatRole.system, 'content': 'Goodbye, world!'},
        )


if __name__ == '__main__':
    unittest.main()
