from flask import Flask, render_template, request
import math
import numpy as np
import sqlite3

app = Flask(__name__)

# Function to make the prediction
def predict_charges(region, age, sex, bmi, children, smoker):
    # Dummy prediction logic (replace with  actual prediction model)
    a = np.zeros(5)
    a[0] = age
    a[1] = sex
    a[2] = bmi
    a[3] = children
    a[4] = smoker

    # Replace this with the actual prediction logic (e.g., using trained model)
    # For now, we are just returning a dummy value based on some calculation.
    predicted_charge = a[0] * 100 + a[1] * 200 + a[2] * 50 + a[3] * 20 + a[4] * 150
    return f"Predicted Medical Insurance Charge is: ${predicted_charge:,.2f}"

# Function to insert the data into the database
def log_prediction_to_db(age, sex, bmi, children, smoker, prediction):
    conn = sqlite3.connect('insurance_predictions.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO predictions (age, sex, bmi, children, smoker, prediction)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (age, sex, bmi, children, smoker, prediction))
    
    conn.commit()
    conn.close()
    
    
# Home route to show the form and prediction (if any)
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', prediction=None)  # No prediction on initial page load

# Route to handle the form submission and make the prediction
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get data from the form
        age = request.form['age']
        sex = request.form['sex']
        bmi = request.form['bmi']
        children = request.form['children']
        smoker = request.form['smoker']

        # Convert form data to the appropriate types
        age = float(age)
        sex = int(sex)
        bmi = float(bmi)
        children = int(children)
        smoker = int(smoker)

        # Make the prediction using the predict_charges function
        prediction = predict_charges('northwest', age, sex, bmi, children, smoker)

# Log the data into the database
        log_prediction_to_db(age, sex, bmi, children, smoker, prediction)
        
        
        # Pass the prediction to the template
        return render_template('index.html', prediction=prediction)

    return render_template('index.html', prediction=None)  # If the form is not submitted, don't show prediction

if __name__ == '__main__':
    app.run(debug=True)
