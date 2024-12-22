from flask import Flask, request, jsonify
from segmentation.thresholding_segmentation import thresholding_segmentation
from segmentation.watershed_segmentation import watershed_segmentation

app = Flask(__name__)

@app.route('/segment/thresholding', methods=['POST'])
def segment_thresholding():
    file = request.files['image']
    threshold = int(request.form.get('threshold', 127))  # Default threshold if not provided
    file.save("input_image.jpg")
    binary_path, adaptive_path = thresholding_segmentation("input_image.jpg", threshold)
    return jsonify({
        "binary_image_path": binary_path,
        "adaptive_image_path": adaptive_path
    })

@app.route('/segment/watershed', methods=['POST'])
def segment_watershed():
    file = request.files['image']
    file.save("input_image.jpg")
    watershed_result, colored_grains = watershed_segmentation("input_image.jpg")
    return jsonify({
        "watershed_image_path": watershed_result,
        "colored_grains_image_path": colored_grains
    })

if __name__ == "__main__":
    app.run(debug=True)
