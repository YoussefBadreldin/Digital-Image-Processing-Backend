from flask import Flask, request, jsonify
from compression import compress_image
from enhancement import enhance_image
from segmentation import segment_image

app = Flask(__name__)

@app.route('/compress', methods=['POST'])
def compress():
    image = request.files['image']
    result_path = compress_image(image)
    return jsonify({'result': result_path})

@app.route('/enhance', methods=['POST'])
def enhance():
    image = request.files['image']
    result_path = enhance_image(image)
    return jsonify({'result': result_path})

@app.route('/segment', methods=['POST'])
def segment():
    image = request.files['image']
    result_path = segment_image(image)
    return jsonify({'result': result_path})

if __name__ == '__main__':
    app.run(debug=True)
