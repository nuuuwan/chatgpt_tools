from attr import dataclass

from gpttools.core.ChatRole import ChatRole


@dataclass
class Message:
    role: ChatRole
    content: str

    def todict(self):
        return dict(role=self.role, content=self.content)
