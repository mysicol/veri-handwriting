from flask import Flask, jsonify, request
from flask_cors import CORS
from GPTInterface import GPTInterface
from MLModel import Methods, makeModels, MLModel
import pickle
import random
import string

app = Flask(__name__)
cors = CORS(app, origins="*")

# makeModels("letters", Methods.DIRECT_LINEAR_REGRESSION) ONLY UNCOMMENT TO RETRAIN MODELS

with open('weights.pkl', 'rb') as f:
    models = pickle.load(f)
print("Read successfully!")

@app.route("/api/image", methods=['POST'])
def image():
    result = request.json
    print(result['image'])

    input_text = "helo this is test centence"
    prompt = "Explain any spelling/grammar errors you find in the following content. Do NOT comment on capitalization or punctuation errors; assume all inputs will be in lowercase and lack punctuation. Be encouraging like you are talking to a child."

    legible_letter = random.choice(string.ascii_lowercase)
    prompt_legible = "Give an extremely silly billy and mean and sassy, one-sentence message like you are talking to a child explaining that the following letter was the least legibly written in the sample of handwriting that was just processed. Please do not use the word 'brat' AT ALL. also DO NOT use terms of endearment AT ALL."

    consistent_letter = random.choice(string.ascii_lowercase)
    prompt_consistent = "Give an extremely silly and mean and sassy, one-sentence message like you are talking to a child explaining that the following letter was the most consistently written in the sample of handwriting that was just processed. Please do not use the word 'brat' AT ALL. also DO NOT use terms of endearment AT ALL."

    # TODO use model to get score
    summary = GPTInterface().get_summary(input_text, prompt)
    legibility = GPTInterface().get_summary(legible_letter, prompt_legible)
    consistence = GPTInterface().get_summary(consistent_letter, prompt_consistent)

    worst = [
        {
            "id": 0,
            "letter": "t",
            "score": 45,    
        },
        {
            "id": 1,
            "letter": "q",
            "score": 38,    
        },
        {
            "id": 2,
            "letter": "x",
            "score": 25,    
        },
    ]

    return jsonify(
        {
            "summary": {
                "input": input_text,
                "text": summary,
                "neatness": 75,
                "consistency": 55,
                "mostLegible": "Your least legible letter was '" + legible_letter + "'. " + legibility,
                "mostConsistent": "Your most consistent letter was '" + consistent_letter + "'. " + consistence,
                "worst": worst,
            }
        }
    )

if __name__ == "__main__":
    # debug = True so we can see live updates while developing
    app.run(debug=False, port=3000)