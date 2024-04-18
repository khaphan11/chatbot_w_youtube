import litellm
from litellm import completion
import os
from dotenv import load_dotenv


load_dotenv()
litellm.huggingface_key = os.getenv('HG_KEY')


class Query:
    def __init__(self):
        self.content = ''
        self.model = os.getenv('MODEL')
        self.api_base = os.getenv('API_BASE')


    def get_response(self, question) -> str:
        """"""
        combined_input = f"Context: {self.content}\nQuestion: {question}?"
        messages = [{"content": combined_input, "question": "Answer the question"}]

        response = completion(
            model=f'huggingface/{self.model}',
            messages=messages,
            api_base=f"{self.api_base}/{self.model}",
            max_new_tokens=512
        )

        try:
            return response.choices[0].message.content.split('Answer:')[-1]
        except:
            return response.choices[0].message.content


    def set_content(self, content) -> None:
        """"""
        self.content = content
