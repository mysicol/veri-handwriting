from flask import Flask, jsonify, request
from flask_cors import CORS
from GPTInterface import GPTInterface
from MLModel import Methods, makeModels, MLModel
import image_squares
import numpy as np
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
    file = request.files['image']
    print(file)

    file = np.frombuffer(file.read(), np.uint8)
    squares = image_squares.characters_from_np(file)

    scores = {}
    print("MODEL:", models)
    for square in squares:
        if square[1] in models:
            # Process the image
            im = square[0]
            np.array([im], dtype=np.float64)
            im = im.reshape(-1, im.shape[1])
            im = im.flatten()
            im = np.array([im], dtype=np.float64)

            # Get image score
            neatness = abs(models[square[1]].score(im)[0][0])

            # Add score to scores array
            if square[1] not in scores:
                scores[square[1]] = []
            scores[square[1]].append(neatness)
    
    print(scores)

    for key in scores.keys():
        scores[key] = int(np.mean(scores[key]) * 100)
    
    print(sorted(scores.keys()))

    results = [x for x in sorted(zip(scores.values(), scores.keys()))]

    text_arr = [square[1] for square in squares]
    input_text = "".join(text_arr)

    prompt = "Explain any spelling/grammar errors you find in the following content. Do NOT comment on capitalization or punctuation errors; assume all inputs will be in lowercase and lack punctuation. Be encouraging like you are talking to a child."

    legible_letter = str(results[0][1])
    legible_score = str(results[0][0])
    prompt_legible = "Give an extremely silly billy and mean and sassy, one-sentence message like you are talking to a child explaining that the following letter was the least legibly written in the sample of handwriting that was just processed. Please do not use the word 'brat' AT ALL. also DO NOT use terms of endearment AT ALL."

    consistent_letter = str(results[-1][1])
    consistent_score = str(results[-1][0])
    prompt_consistent = "Give an extremely silly and mean and sassy, one-sentence message like you are talking to a child explaining that the following letter was the most consistently written in the sample of handwriting that was just processed. Please do not use the word 'brat' AT ALL. also DO NOT use terms of endearment AT ALL."

    # TODO use model to get score
    summary = GPTInterface().get_summary(input_text, prompt)
    legibility = GPTInterface().get_summary(legible_letter, prompt_legible)
    consistence = GPTInterface().get_summary(consistent_letter, prompt_consistent)

    worst = []
    for i in range(len(results)):
        worst.append({
                "id": i,
                "letter": results[i][1],
                "score": results[i][0],    
        })

    if len(worst) > 3:
        worst = worst[0:3]

    return jsonify(
        {
            "summary": {
                "input": input_text,
                "text": summary,
                "neatness": 75,
                "consistency": 55,
                "mostLegible": "Your least legible letter was '" + legible_letter + "', at " + legible_score + "% legibility. " + legibility,
                "mostConsistent": "Your most consistent letter was '" + consistent_letter + "', at " + consistent_score + "% legibility. " + consistence,
                "worst": worst,
            }
        }
    )

if __name__ == "__main__":
    # debug = True so we can see live updates while developing
    app.run(debug=False, port=3000)