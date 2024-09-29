from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
from flask_cors import CORS
import json
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Load the serialized model
with open('diabetes_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('diabetes_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/')
def index():
    # Render the main index.html page
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'OPTIONS'])
# def predict():
#     data = request.get_json(force=True)
#     # Print the received values for debugging
#     print("Received features:", data)
#     feature_names = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree_function', 'age']
    
#     # Extract features from the request data
#     features = {
#         'pregnancies': [data['pregnancies']],
#         'glucose': [data['glucose']],
#         'blood_pressure': [data['blood_pressure']],
#         'skin_thickness': [data['skin_thickness']],
#         'insulin': [data['insulin']],
#         'bmi': [data['bmi']],
#         'diabetes_pedigree_function': [data['diabetes_pedigree_function']],
#         'age': [data['age']]
#     }

#     # Convert features to a DataFrame and apply scaling
#     features_df = pd.DataFrame(features, columns=feature_names)
#     features_scaled = scaler.transform(features_df)

#     prediction = model.predict(features_scaled)[0]
#     result = 'Diabetes' if prediction == 1 else 'No Diabetes'
  
#     return jsonify({'prediction': result, 'ok': 'true'})

def predict():
    data = request.get_json(force=True)
    # Print the received values for debugging
    print("Received features:", data)
    data = {
    "data": {
        "pregnancies": 6,
        "glucose": 148,
        "blood_pressure": 72,
        "skin_thickness": 35,
        "insulin": 0,
        "bmi": 33.6,
        "diabetes_pedigree_function": 0.627,
        "age": 50
    }
    }

    # Convert the dictionary to a JSON string if needed
    json_data = json.dumps(data)
    response = requests.post('https://mlopsassigment2.azurewebsites.net/api/diabatic_model?code=ApY_47QZjGvYh4a0nwZ0nHd49YILiSxjZKpoDNlmQ2FBAzFuJkJQfQ%3D%3D', json=data)
    return jsonify({'prediction': response, 'ok': 'true'})

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000)
