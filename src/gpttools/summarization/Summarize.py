import os

from utils import File, Log

from gpttools.summarization.summarize_utils import summarize_content

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
            if file.endswith(".summary.txt"):
                continue
            path = os.path.join(self.dir_root, file)
            paths.append(path)
        return paths

    def summarize(self, original_path: str):
        summarized_path = original_path[:-4] + ".summary.txt"
        content = File(original_path).read()
        summarized_content = summarize_content(content)
        File(summarized_path).write(summarized_content)
        log.info(f"Saved {summarized_path}")

    def summarize_all(self):
        paths = self.original_paths
        n_paths = len(paths)
        for i_path, path in enumerate(paths):
            log.debug(f'Summarizing {i_path + 1}/{n_paths}: {path}')
            self.summarize(path)


if __name__ == '__main__':
    Summarize().summarize_all()
