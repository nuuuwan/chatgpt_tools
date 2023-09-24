import unittest

from gpttools.apps.DocCommands import (CMD_POSTAMBLE, CMD_PREAMBLE,
                                       CMD_PRETTIFY, get_cmd_summarize)


class TestDocCommands(unittest.TestCase):
    def test_cmd_preamble(self):
        self.assertEqual(
            CMD_PREAMBLE.strip(), 'The following is a part from a document:'
        )

    def test_cmd_postamble(self):
        self.assertEqual(
            CMD_POSTAMBLE.strip(),
            'You will be asked a set of questions about the part.',
        )

    def test_get_cmd_summarize(self):
        self.assertEqual(
            get_cmd_summarize(3).strip(),
            'Summarize into 3 unnumbered bullet points,\n'
            + 'including a space after each bullet paragraph.',
        )
        self.assertEqual(
            get_cmd_summarize(5).strip(),
            'Summarize into 5 unnumbered bullet points,\n'
            + 'including a space after each bullet paragraph.',
        )

    def test_cmd_prettify(self):
        self.assertEqual(
            CMD_PRETTIFY.strip(),
            'In your summary, append emojis next to words,\n'
            + 'replace each bullet with an emoji that '
            + 'represents the bullet\'s content,\n'
            + 'and replace words with hashtags and handles',
        )


if __name__ == '__main__':
    unittest.main()
