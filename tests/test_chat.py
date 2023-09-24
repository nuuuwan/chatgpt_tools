import unittest
from unittest.mock import patch

from gpttools import Chat, ChatRole


class TestChat(unittest.TestCase):
    def setUp(self):
        self.chat = Chat()

    def test_create_chat(self):
        self.assertEqual(self.chat.options, {'temperature': 0.1})
        self.assertEqual(self.chat.messages, [])

    def test_append_message(self):
        self.chat.append_message(ChatRole.user, 'Hello, world!')
        self.assertEqual(
            self.chat.messages,
            [{'role': ChatRole.user, 'content': 'Hello, world!'}],
        )

    def test_append_system_message(self):
        self.chat.append_system_message('Hello, world!\n')
        self.assertEqual(
            self.chat.messages,
            [{'role': ChatRole.system, 'content': 'Hello, world!'}],
        )

    def test_append_user_message(self):
        self.chat.append_user_message('Hello, world!')
        self.assertEqual(
            self.chat.messages,
            [{'role': ChatRole.user, 'content': 'Hello, world!'}],
        )

    def test_append_assistant_message(self):
        self.chat.append_assistant_message('Hello, world!')
        self.assertEqual(
            self.chat.messages,
            [{'role': ChatRole.assistant, 'content': 'Hello, world!'}],
        )

    @patch('openai.ChatCompletion.create')
    def test_send(self, mock_create):
        mock_create.return_value = {
            'choices': [{'message': {'content': 'Hello, world!'}}]
        }

        self.chat = Chat()

        self.chat.append_system_message('Hello, world!')

        response = self.chat.send()
        self.assertEqual(response, 'Hello, world!')
        self.assertEqual(
            self.chat.messages,
            [
                {'role': ChatRole.system, 'content': 'Hello, world!'},
                {'role': ChatRole.assistant, 'content': 'Hello, world!'},
            ],
        )


if __name__ == '__main__':
    unittest.main()
