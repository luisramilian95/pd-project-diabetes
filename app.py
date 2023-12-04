from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

import pandas as pd
import pickle

with open('model-diabetes.pkl', 'rb') as f_pkl:
  model=pickle.load(f_pkl)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_data():
    if request.method == 'POST':
        
        prediction = predict_data(request=request)

        return render_template('index.html', prediction=prediction)
    return render_template('index.html')
 

def predict_data(request):
    try:
        gender = int(request.form['gender'])
        age = float(request.form['age'])
        hypertension = 0
        heart_disease = 0
        smoking_history = float(request.form['smoking_history'])
        bmi = float(request.form['bmi'])
        HbA1c_level = float(request.form['HbA1c_level'])
        blood_glucose_level = float(request.form['blood_glucose_level'])


        if request.form.get('hypertension'):
            hypertension = request.form['hypertension']

        if request.form.get('heart_disease'):
            heart_disease = request.form['heart_disease']


        data = [[gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level]]
        columns = ['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        data_frame = pd.DataFrame(data, columns=columns)

        prediction = model.predict(data_frame) 

        if (prediction[0] == 0):
            return 'No diabetes'

        return 'Diabetes'

    except:
        return 'Los datos no se ingresaron correctamente'

if __name__ == '__main__':
    app.run(debug=True, port=8081)