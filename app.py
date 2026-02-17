from flask import Flask, render_template, request, send_from_directory
import numpy as np
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__, template_folder='.', static_folder='.')

@app.route('/style.css')
def serve_css():
    return send_from_directory(os.getcwd(), 'style.css')

products = {
    "P101": ("Laptop", [120,130,125,140,150,160,170,180,190,200,210,220]),
    "P102": ("Mobile", [200,210,205,220,240,250,260,270,290,300,320,340]),
    "P103": ("Headphones", [80,85,82,90,95,100,110,115,120,130,140,150])
}

# -------- ML Forecast --------
def forecast(sales_data):
    months = np.array(range(1,13)).reshape(-1,1)
    sales = np.array(sales_data)

    model = LinearRegression()
    model.fit(months, sales)

    future = np.array([[13]])
    return int(model.predict(future)[0])

# -------- Routes --------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    product_id = request.form['product_id']

    if product_id not in products:
        return render_template('index.html', prediction="Invalid Product ID")

    name, sales = products[product_id]
    result = forecast(sales)

    return render_template('index.html',
                           prediction=f"{name} → Next Month Demand: {result} units")

if __name__ == '__main__':
    app.run(debug=True)
