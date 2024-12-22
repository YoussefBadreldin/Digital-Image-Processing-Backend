from compression import compression
from enhancement import enhancement
from segmentation import segmentation

app = Flask(__name__)

app.register_blueprint(compression.app, url_prefix='/compress')
app.register_blueprint(enhancement.app, url_prefix='/enhance')
app.register_blueprint(segmentation.app, url_prefix='/segment')

if __name__ == "__main__":
    app.run(debug=True)
