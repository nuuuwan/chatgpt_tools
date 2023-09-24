import unittest

from gpttools import ChatRole


class TestChatRole(unittest.TestCase):
    def test_user_role(self):
        self.assertEqual(ChatRole.user, 'user')

    def test_system_role(self):
        self.assertEqual(ChatRole.system, 'system')

    def test_assistant_role(self):
        self.assertEqual(ChatRole.assistant, 'assistant')

    def test_function_role(self):
        self.assertEqual(ChatRole.function, 'function')


if __name__ == '__main__':
    unittest.main()
