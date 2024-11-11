from flask import Flask, request, jsonify, render_template
from analyze import read_image

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/api/v1/analysis/", methods=['POST'])
def analysis():
    try:
        data = request.get_json()
        image_uri = data.get('url')
        if not image_uri:
            return jsonify({'error': 'No image URI provided'}), 400

        result = read_image(image_uri)
        return jsonify({"text": result}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred during image analysis'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
