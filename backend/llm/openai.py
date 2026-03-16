import base64
import json
from pathlib import Path
from typing import Any

from openai import OpenAI
from langchain_openai import ChatOpenAI

from backend.config import get_settings


class OpenAILLM:
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.0,
    ):
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key=get_settings().openai_api_key)

    def chat(self, content: str, system_prompt: str | None = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": content})

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages,
        )

        return response.choices[0].message.content

    def chat_json(self, content: str, system_prompt: str | None = None) -> dict[str, Any]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": content})

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

    def chat_vision(self, image_path: str, system_prompt: str | None = None) -> dict[str, Any]:
        image_data = base64.b64encode(Path(image_path).read_bytes()).decode("utf-8")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_data}",
                        "detail": "low",
                    },
                },
            ],
        })

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=self.temperature,
            messages=messages,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

    def as_chat_model(self) -> ChatOpenAI:
        return ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            api_key=self.client.api_key
        )