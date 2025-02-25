from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "Hello, this is your Flask API!"})

@app.route('/api/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Process the CSV file
        data = []
        with open(filepath, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                data.append(row)

        return jsonify({"message": "File uploaded and processed successfully", "data": data}), 200

    return jsonify({"error": "Invalid file type. Only CSV files are allowed"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
