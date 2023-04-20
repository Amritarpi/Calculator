from datetime import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['calculator']

history = db['history']


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def calculate():
   
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    operation = request.form['operation']


    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        result = num1 / num2

  
    timestamp = datetime.utcnow()
    history.insert_one({
        'num1': num1,
        'num2': num2,
        'operation': operation,
        'result': result,
        'created_at': timestamp
    })


    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
