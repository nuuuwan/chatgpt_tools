import os

from utils import File, Log, hashx

from gpttools.summarization.summarize_utils import summarize_content
from gpttools.summarization.web_utils import get_url_text

log = Log('Summarize')


class Summarize:
    def __init__(self, dir_root=None):
        self.dir_root = dir_root or os.getenv("DIR_DESKTOP")

    @property
    def original_paths(self) -> list[str]:
        paths = []
        for file in os.listdir(self.dir_root):
            if not file.endswith(".txt"):
                continue
            if "summary." in file:
                continue
            path = os.path.join(self.dir_root, file)
            paths.append(path)
        return paths

    @staticmethod
    def get_summarized_path(original_path: str) -> str:
        tokens = list(os.path.split(original_path))
        tokens[-1] = 'summary.' + tokens[-1]
        return os.path.join(*tokens)

    def summarize(self, original_path: str):
        summarized_path = Summarize.get_summarized_path(original_path)
        if os.path.exists(summarized_path):
            log.info(f"Already summarized: {summarized_path}")
        else:
            content = File(original_path).read()
            summarized_content = summarize_content(content)
            File(summarized_path).write(summarized_content)
            log.info(f"Saved {summarized_path}")
        os.startfile(summarized_path)

    def summarize_desktop(self):
        paths = self.original_paths
        n_paths = len(paths)
        for i_path, path in enumerate(paths):
            log.info(f'Summarizing {i_path + 1}/{n_paths}: {path}')
            self.summarize(path)

    def summarize_url(self, url):
        hash = hashx.md5(url)
        path = os.path.join(self.dir_root, f'www-{hash}.txt')

        if os.path.exists(path):
            log.info(f"Already summarized: {path}")
        else:
            content = get_url_text(url)
            File(path).write(content)

        self.summarize_desktop()
