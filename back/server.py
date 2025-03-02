from flask import Flask, jsonify, request
from flask_cors import CORS
from GPTInterface import GPTInterface
from MLModel import Methods, makeModels, MLModel
import pickle

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

    input_text = "we r tests stufs"

    # TODO use model to get score
    summary = GPTInterface().get_summary(input_text)

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
                "mostLegible": "a",
                "mostConsistent": "j",
                "worst": worst,
            }
        }
    )

if __name__ == "__main__":
    # debug = True so we can see live updates while developing
    app.run(debug=False, port=3000)