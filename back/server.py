from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins="*")

@app.route("/api/image", methods=['POST'])
def image():
    result = request.json
    print(result['image'])

    # TODO use model to get score

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
                "text": "This is a really long summary about how bad your handwriting is. It really is bad. You should seek help. No one can read your handwriting. You should give up on all your hopes and dreams. No one could love you. Womp womp.",
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
    app.run(debug=True, port=3000)