import pickle

import flask
from flask import Flask, request, jsonify
#from main import recommendation_Choices
import json
from Review import Offensive_Or_Not
from flask import Flask, request, jsonify
# Initialize Flask app
app = Flask(__name__)
import os

# Create API endpoints for each model
@app.route('/')
def index():
    return flask.render_template('index.html', result=" ")

# Create API endpoints for each model
@app.route('/madireview', methods=['POST'])
def review_model_predict():

    input_review = (request.args['input_review'])  # Extract input data from JSON
    # Extract input data from JSON
    response=Offensive_Or_Not(input_review)
    response = {"result": response}
    return response

@app.post('/review')
def predict_model_review():
    # Extract input data from JSON
    input_review = request.form.get("comment")

    # Assuming Offensive_Or_Not is your function to classify reviews
    result = Offensive_Or_Not(input_review)

    # Define the file paths using os.path.join
    base_dir = os.path.dirname(__file__)
    readme_path = os.path.join(base_dir, 'readme.txt')
    offensive_path = os.path.join(base_dir, 'Offensive.txt')

    # Append the review to the respective file based on the result
    if result == "Not Offensive":
        with open(readme_path, 'a', encoding='utf-8') as f:
            f.write(input_review + ',\n')
    else:
        with open(offensive_path, 'a', encoding='utf-8') as f:
            f.write(input_review + ',\n')

    # Render the template with the result
    return flask.render_template('index.html', result=result)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Start the server