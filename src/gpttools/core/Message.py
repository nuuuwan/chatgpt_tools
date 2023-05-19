from attr import dataclass


@dataclass
class Message:
    role: str
    content: str

    def todict(self):
        return dict(role=self.role, content=self.content)
