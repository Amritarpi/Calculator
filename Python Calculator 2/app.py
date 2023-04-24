# import pytz
from datetime import datetime  #importing datatime class from module datatime
from flask import Flask, render_template, request # flask is used to create web app, render templates to render html templates, request to get data submitted thru http requests
from pymongo import MongoClient #importing PyMongo class that manages MongoDB connections to the Flask app

app = Flask(__name__) #creating an instance of Flask that assigns to the app variables then pass __name__ as argument to flask(to find files n templates)

client = MongoClient('mongodb://localhost:27017/') #URI connection to the database names calculator n collection name history
db = client['calculator'] #PyMongo connects to the MongoDB server running on port 27017 on localhost, to the database named calculator. 

history = db['history'] #history collection is exposed as the db attribute.

@app.route('/') # useer visit url flask will call this func n return to templates
def home():
    return render_template('index.html')

# this is another url n works only when user submits form thru post request

@app.route('/', methods=['POST']) #route to add to the databse using the 'POST' method
#def calculate():
    #try:
        #num1 = float(request.form['num1'])
        #num2 = float(request.form['num2'])
        #operation = request.form['operation']
    #except KeyError as e:
        # Handle missing parameter error
        #return render_template('error.html', message=f'Missing parameter: {str(e)}'), 400

def calculate(): #function definition
   
    num1 = float(request.form['num1']) # num1, num2, operation are taken as inputs from the user and stored in the respective variables
    num2 = float(request.form['num2'])
    operation = request.form['operation']
# 2operands, 4opertaions from the request data

    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        result = num1 / num2
#performs requested calculations n inserts a new document into history collection
  
    timestamp = datetime.utcnow()
    # utc_timezone = pytz.timezone('UTC')
    # ist_timezone = pytz.timezone('Asia/Kolkata')
    # ist_timestamp = utc_timezone.localize(utc_timestamp).astimezone(ist_timezone)
    history.insert_one({  #inserting the document into the history collection
        'num1': num1,
        'num2': num2,
        'operation': operation,
        'result': result,
        'created_at': timestamp
    })


    return render_template('index.html', result=result) # The function then returns the index.html template, passing the calculated result as  variable that can be rendered in the HTML.

if __name__ == '__main__': # script is running as main program, this runs directy
    app.run(debug=True) # if debug is true thats means, its enable, flask development server with debugging is enabled
