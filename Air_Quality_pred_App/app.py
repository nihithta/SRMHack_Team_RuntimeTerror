from flask import Flask, render_template, jsonify, request
import joblib
import requests
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def index_():
    url = "https://api.openaq.org/v2/latest/2498781?limit=1000&page=1&offset=0&sort=asc"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        
        # Initialize empty lists to store parameter values
        pm1_values = []
        pm10_values = []
        pm25_values = []
        relativehumidity_values = []
        temperature_values = []
        um003_values = []
        
        # Loop through results to extract parameter values
        for result in results:
            measurements = result.get('measurements', [])
            for measurement in measurements:
                parameter = measurement.get('parameter')
                value = measurement.get('value')
                
                # Append value to corresponding parameter list
                if parameter == 'pm1':
                    pm1_values.append(value)
                elif parameter == 'pm10':
                    pm10_values.append(value)
                elif parameter == 'pm25':
                    pm25_values.append(value)
                elif parameter == 'relativehumidity':
                    relativehumidity_values.append(value)
                elif parameter == 'temperature':
                    temperature_values.append(value)
                elif parameter == 'um003':
                    um003_values.append(value)
        
        # Combine all parameter values into a single numpy array
        values_list = np.array([
            pm1_values,
            pm10_values,
            pm25_values,
            relativehumidity_values,
            temperature_values,
            um003_values
        ])

        # Load the scaler model
        scaler = joblib.load('model/scaler (1).joblib')
        
        # Reshape the values_list to (n_samples, n_features) for scaling
        values_list_reshaped = values_list.T  # Transpose to align with (n_samples, n_features)
        
        scaled_values = scaler.transform(values_list_reshaped)

        x = joblib.load("model/model.h5")
        ans = x.predict(scaled_values)


    return render_template('index.html', scaled_values=scaled_values)

@app.route('/api/data')
def get_api_data():
    url = "https://api.openaq.org/v2/latest/2498781?limit=1000&page=1&offset=0&sort=asc"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)  # Return JSON response
    else:
        return jsonify({'error': 'Failed to fetch data'})

if __name__ == '__main__':
    app.run(debug=True)