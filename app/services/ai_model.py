from openai import OpenAI


class AIModel:
    def __init__(self, model=None):
        self.client = OpenAI()
        self.model = model or "gpt-3.5-turbo"

    def _get_response(
        self, prompt_messages: list[dict[str, str]], *args, **kwargs
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=prompt_messages,
            *args,
            **kwargs,
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

    def generate_feedback(self, question: str, writing_content: str) -> str:
        return self._get_response(
            [
                {
                    "role": "system",
                    "content": f"Given this question '{question}' and the answer text: '{writing_content}'  "
                    f"Give me feed back on the content this "
                    f"text with the following questions: I'm interested in your feedback on "
                    f"this writing. What's your evaluation?, Can you provide feedback on "
                    f"grammar and language usage?Please evaluate based on IELTS scoring "
                    f"criteria",
                },
            ]
        )


if __name__ == "__main__":
    ai = AIModel()
    print(
        ai.generate_feedback(
            question='To what extent do you agree or disagree with the statement "Technology is making people less creative"?',
            writing_content="What the hell is this shit",
        )
    )
