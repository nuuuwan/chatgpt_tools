import os
import shutil
import tempfile
import unittest

from gpttools import Text

DIR_TEMP = tempfile.gettempdir()
DIR_SAMPLES = os.path.join('tests', 'samples')


class TestText(unittest.TestCase):
    def setUp(self) -> None:
        for file in os.listdir(DIR_TEMP):
            if file.endswith('.txt') or file.endswith('.pdf'):
                shutil.copyfile(
                    os.path.join(DIR_TEMP, file),
                    os.path.join(DIR_SAMPLES, file),
                )

    def test_from_x(self):
        for x in [
            os.path.join(DIR_TEMP, 'sample.txt'),
            os.path.join(DIR_TEMP, 'sample.pdf'),
            'https://www.dailymirror.lk'
            + '/top-story'
            + '/Israel-Palestine-conflict-MR-says-war-is-not-the-solution'
            + '/155-269306',
        ]:
            t = Text.from_x(x)
            t.summarize().speak()
            t.bullet(5).speak()

    def test_smaller(self):
        t = Text.from_txt(os.path.join(DIR_TEMP, 'sample-large.txt'))
        t.smaller().summarize()

        with self.assertRaises(Exception) as _:
            t.summarize()


if __name__ == '__main__':
    unittest.main()
