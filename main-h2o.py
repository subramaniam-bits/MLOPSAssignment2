from flask import Flask, request, jsonify, render_template
import os
import h2o
import pandas as pd
from flask_cors import CORS  # Import CORS

# Initialize Flask app
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Initialize H2O
h2o.init()

# Load the saved H2O model
model_path = './best_diabetes_model/StackedEnsemble_AllModels_1_AutoML_1_20240922_131435'
model = h2o.load_model(model_path)

print("Model loaded")

@app.route('/')
def index():
    # Render the main index.html page
    return render_template('index.html')

def interpret_prediction(prediction):
    # Define a mapping from numerical values to labels
    if prediction == 0:
        return "No Diabetes"
    else:
        return "Diabetes"

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the request
    data = request.json
    print("Received data:", data)

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame([data])
    
    # Ensure all columns are present and in the correct order
    required_columns = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'bmi', 'diabetes_pedigree_function', 'age']
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0  # Or some other default value
    df = df[required_columns]
    
    # Convert DataFrame to H2OFrame
    h2o_frame = h2o.H2OFrame(df)
    
    # Make prediction
    predictions = model.predict(h2o_frame)
    
    # Convert predictions to pandas DataFrame
    predictions_df = predictions.as_data_frame()
    
    # Extract the prediction value
    predict_value = predictions_df['predict'][0]
    
    # Print and return the result
    result = interpret_prediction(predict_value)
    print(f"The prediction is: {result}")

    return jsonify({"prediction": result})

# if __name__ == '__main__':
#     app.run(debug=True)
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
