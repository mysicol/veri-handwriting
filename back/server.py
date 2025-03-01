from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins="*")

@app.route("/api/example", methods=['GET'])
def example():
    return jsonify(
        {
            "data": {
                "score": 75,
            }
        }
    )

@app.route("/api/image", methods=['POST'])
def image():
    result = request.json
    print(result['image'])

    # TODO use model to get score

    return jsonify(
        {
            "summary": {
                "score": 75
            }
        }
    )

if __name__ == "__main__":
    # debug = True so we can see live updates while developing
    app.run(debug=True, port=3000)