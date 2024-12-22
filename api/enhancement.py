from flask import Flask, request, jsonify
from enhancement.gray_level_slicing import gray_level_slicing
from enhancement.histogram_equalization import histogram_equalization

app = Flask(__name__)

@app.route('/enhance/gray_level_slicing', methods=['POST'])
def enhance_gray_level_slicing():
    file = request.files['image']
    min_val = int(request.form.get('min_val', 100))  # Default min_val if not provided
    max_val = int(request.form.get('max_val', 150))  # Default max_val if not provided
    file.save("input_image.jpg")
    result_path = gray_level_slicing("input_image.jpg", min_val, max_val)
    return jsonify({"enhanced_image_path": result_path})

@app.route('/enhance/histogram_equalization', methods=['POST'])
def enhance_histogram_equalization():
    file = request.files['image']
    file.save("input_image.jpg")
    result_path = histogram_equalization("input_image.jpg")
    return jsonify({"enhanced_image_path": result_path})

if __name__ == "__main__":
    app.run(debug=True)
