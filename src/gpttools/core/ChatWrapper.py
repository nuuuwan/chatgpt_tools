import os

import openai

from gpttools.core.Message import Message

openai.Completion.create(
    model="text-davinci-003",
    prompt="Say this is a test",
    max_tokens=7,
    temperature=0,
)


class ChatWrapper:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.messages = []

    def __send__(self, role, content):
        self.messages.append(Message(role=role, content=content).todict())
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo', messages=self.messages
        )
        return response['choices'][0]['message']['content']

    def send_system(self, content):
        return self.__send__("system", content)

    def send_user(self, content):
        return self.__send__("user", content)


if __name__ == "__main__":
    chat = ChatWrapper()
    while True:
        content = input("> ")
        if content == 'x':
            break
        print(chat.send_user(content))
