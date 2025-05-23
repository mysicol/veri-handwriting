import openai
from APIKeys import APIKeys

class GPTInterface:
    def __init__(self):
        APIKeys.set_var('OPENAI_API_KEY')
        self.__gpt = openai.OpenAI()
        
    def get_summary(self, thing, prompt):
        completion = self.__gpt.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": thing}
            ]
        )

        return completion.choices[0].message.content