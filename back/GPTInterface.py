import openai
from APIKeys import APIKeys

class GPTInterface:
    def __init__(self):
        APIKeys.set_var('OPENAI_API_KEY')
        self.__gpt = openai.OpenAI()
        
    def get_summary(self, thing):
        completion = self.__gpt.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Explain any spelling/grammar errors you find in the following content. Do NOT comment on capitalization or punctuation errors; assume all inputs will be in lowercase and lack punctuation. Be encouraging like you are talking to a child."},
                {"role": "user", "content": thing}
            ]
        )

        return completion.choices[0].message.content