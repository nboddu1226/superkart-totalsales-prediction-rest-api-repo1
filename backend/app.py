# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_total_sales_predictor_api = Flask("SuperKart Total Sales Predictor")

# Load the trained machine learning model
model = joblib.load("superkart_model_total_sales_v1_0.joblib")

# Define a route for the home page (GET request)
@superkart_total_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Total Sales Prediction API!"

# Define an endpoint for single property prediction (POST request)
@superkart_total_sales_predictor_api.post('/v1/superkart')
def predict_superkart_totalsales():
    """
    This function handles POST requests to the '/v1/superkart' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    superkart_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': superkart_data['Product_Weight'],
        'Product_Sugar_Content': superkart_data['Product_Sugar_Content'],
        'Product_Allocated_Area': superkart_data['Product_Allocated_Area'],
        'Product_MRP': superkart_data['Product_MRP'],
        'Store_Size': superkart_data['Store_Size'],
        'Store_Location_City_Type': superkart_data['Store_Location_City_Type'],
        'Store_Type': superkart_data['Store_Type'],
        'Product_Id_char': superkart_data['Product_Id_char'],
        'Store_Age_Years': superkart_data['Store_Age_Years'],
        'Product_Type_Category': superkart_data['Product_Type_Category']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get log_price)
    superkart_predicted_total_sales = model.predict(input_data)[0]

    # Return the actual price
    return jsonify({'SuperKart Predicted Total Sales (in dollars)': superkart_predicted_total_sales})


# Define an endpoint for batch prediction (POST request)
@superkart_total_sales_predictor_api.post('/v1/superkartbatch')
def predict_superkart_totalsales_batch():
    """
    This function handles POST requests to the '/v1/superkartbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_superkart_total_sales = model.predict(input_data).tolist() 

    # Return the predictions dictionary as a JSON response
    return predicted_superkart_total_sales

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_total_sales_predictor_api.run(debug=True)
