import sys

from gpttools.summarization.Summarize import Summarize

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python summarize_url.py <url>')
        sys.exit(1)

    url = sys.argv[1]
    Summarize().summarize_url(url)
