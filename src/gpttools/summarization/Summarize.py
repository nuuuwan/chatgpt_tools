import os

from utils import File, Log

log = Log('Summarize')


def batch_content(content: str):
    MAX_BATCH_LEN = 3_000
    paragraphs = content.split("\n")
    batches = ['']
    for paragraph in paragraphs:
        if len(batches[-1]) + len(paragraph) < MAX_BATCH_LEN:
            batches[-1] += paragraph + "\n"
        else:
            batches.append('')
            batches[-1] = paragraph + "\n"
    return batches


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

    def summarize_batch(self, batch):
        return batch

    def summarize_content(self, content):
        batches = batch_content(content)
        summarized_content = ''
        for batch in batches:
            summarized_batch = self.summarize_batch(batch_content)
            summarized_content += summarized_batch
        return summarized_content

    def summarize(self, original_path: str):
        summarized_path = original_path[:-4] + ".summary.txt"
        content = File(original_path).read()
        summarized_content = self.summarize_content(content)
        File(summarized_path).write(summarized_content)
        log.info(f"Summarized {original_path} to {summarized_path}")

    def summarize_all(self):
        for path in self.original_paths:
            self.summarize(path)


if __name__ == '__main__':
    Summarize().summarize_all()
