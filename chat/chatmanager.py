import json
from dataclasses import dataclass

import requests

from .api import API, Message, Messages, Role


@dataclass
class ChatManager:
    messages: Messages = None
    api_response: requests.Response = None

    def __post_init__(self):
        self.messages = Messages()
        self.api = API()

    def send(self, prompt: str):
        message = Message(role=Role.user, content=prompt)
        self.messages.append(message)

    def retrieve_reply(self):
        self.api_response = self.api.get_reply(self.messages)

    def get_reply_chunks(self):
        chunks = []
        for chunk in self.get_response_chunks():
            chunks.append(chunk)
            yield chunk

        reply = "".join(chunks)
        message = Message(role=Role.assistant, content=reply)
        self.messages.append(message)

    def get_response_chunks(self):
        whitespace_seen = False
        for response in self.get_api_response_chunks():
            message = self.parse_response(response)
            if message == "\n\n" and not whitespace_seen:
                whitespace_seen = True
            elif message:
                yield message

    @classmethod
    def parse_response(cls, response_bytes: bytes):
        response_bytes_json = response_bytes.strip()
        try:
            response_info = json.loads(response_bytes_json)
        except json.JSONDecodeError:
            print(response_bytes_json)
            raise
        response = response_info["choices"][0]["delta"]
        return response.get("content")

    def get_api_response_chunks(self):
        api_response_parts = []
        for chunk in self.api_response:
            data_keyword = b"data: "
            if chunk.startswith(data_keyword) and api_response_parts:
                api_response = b"".join(api_response_parts)
                api_responses = api_response.split(data_keyword)
                for response in api_responses:
                    if response:
                        yield response
                api_response_parts = []
            api_response_parts.append(chunk)
