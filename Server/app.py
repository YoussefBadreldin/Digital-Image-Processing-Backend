from flask import Flask, request, jsonify
import enhance
import compress
import segment
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/enhance', methods=['POST'])
def enhance_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    result = enhance.process(file)
    return jsonify(result)

@app.route('/compress', methods=['POST'])
def compress_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    result = compress.process(file)
    return jsonify({'result': result})

@app.route('/segment', methods=['POST'])
def segment_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    result = segment.process(file)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
