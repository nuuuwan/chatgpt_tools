import os

import openai

from gpttools.core.Message import Message


class ChatWrapper:
    def __init__(self, temperature=0):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.temperature = temperature
        self.messages = []

    def __send__(self, role, content):
        self.messages.append(Message(role=role, content=content).todict())
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.messages,
            temperature=self.temperature,
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
