import os
import sys

from utils import File, Log

from gpttools.apps import web_utils

log = Log('url_to_txt')


def main(url: str, file_label: str):
    text = web_utils.get_url_text(url)
    file_path = os.path.join(os.getenv("DIR_DESKTOP"), f'{file_label}.txt')

    File(file_path).write(text)
    print(f'Wrote {file_path} ({len(text):,}B)')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python summarize_url.py <url> <file_label>')
        sys.exit(1)

    url = sys.argv[1]
    file_label = sys.argv[2]

    main(url, file_label)
