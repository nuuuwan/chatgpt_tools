from utils import File, Log

CHARS_PER_BULLET = 1_000


log = Log('FileLogger')


class FileLogger:
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        self.log_lines = []

    def write_log(self):
        File(self.log_file_path).write_lines(self.log_lines)

    def append_log(self, line: str):
        self.log_lines.append(line)
        self.log_lines.append('...')
        self.write_log()
