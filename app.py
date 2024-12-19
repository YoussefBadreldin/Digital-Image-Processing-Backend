from flask import Flask, request, jsonify
from compression import compress_image
from enhancement import enhance_image
from segmentation import segment_image

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_image():
    image = request.files['image']
    action = request.form['action']
    
    if action == 'compress':
        result_path = compress_image(image)
    elif action == 'enhance':
        result_path = enhance_image(image)
    elif action == 'segment':
        result_path = segment_image(image)
    else:
        return jsonify({'error': 'Invalid action'}), 400
    
    return jsonify({'result': result_path})

if __name__ == '__main__':
    app.run(debug=True)
