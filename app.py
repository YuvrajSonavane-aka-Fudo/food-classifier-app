from flask import Flask, request, render_template, jsonify
import boto3

app = Flask(__name__)

# Initialize Rekognition client
rekognition = boto3.client("rekognition", region_name="us-east-1")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
def classify():
    file = request.files["image"]
    image_bytes = file.read()

    response = rekognition.detect_labels(
        Image={"Bytes": image_bytes},
        MaxLabels=5,
        MinConfidence=70
    )

    labels = [label["Name"] for label in response["Labels"]]
    return jsonify({"labels": labels})

if __name__ == "__main__":
    app.run(debug=True)
