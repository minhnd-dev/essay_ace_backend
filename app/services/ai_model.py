from openai import OpenAI


class AIModel:
    def __init__(self, model=None):
        self.client = OpenAI()
        self.model = model or "gpt-3.5-turbo"

    def _get_response(self, prompt_messages: list[dict[str, str]]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=prompt_messages,
        )
        return response.choices[0].message.content

    def rewrite(self, topic: str, response_content: str) -> str:
        return self._get_response(
            [
                {
                    "role": "system",
                    "content": "You are a great IELTS teacher with many years of experience. "
                    "You will rewrite the following text to make it as good as you can",
                },
                {"role": "user", "content": f"Topic: {topic}"},
                {"role": "user", "content": response_content},
            ]
        )

    def generate_topic(self) -> str:
        return self._get_response(
            [
                {
                    "role": "system",
                    "content": "You are a great IELTS teacher with many years of experience. Only give me the question with any additional texts",
                },
                {
                    "role": "user",
                    "content": f"Write a question for an IELTS task 2 essay",
                },
            ]
        )


if __name__ == "__main__":
    ai = AIModel()
    print(ai.generate_topic())
