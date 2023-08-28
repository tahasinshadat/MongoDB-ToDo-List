from flask import Flask, render_template, redirect, url_for, request

from flask_pymongo import PyMongo

# take the string object id and convert it into something mongo can actually work with
from bson.objectid import ObjectId

from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='MONGO_URI.env')  # Load variables from .env file

mongo = PyMongo()

def create_app():
    app = Flask(__name__)

    app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

    mongo.init_app(app)

    return app

app = create_app()


@app.route('/')
def index():
    todos_collection = mongo.db.todos
    todos = todos_collection.find()
    return render_template('index.html', todos=todos)


@app.route('/add_todo', methods=['POST'])
def add_todo():
    todos_collection = mongo.db.todos
    todo_item = request.form.get('add-todo')
    # print(todo_item)
    if todo_item == '':
        return redirect(url_for('index'))
    todos_collection.insert_one(
        {
            'text' : todo_item,
            'complete' : False
        }
    )
    return redirect(url_for('index'))

''' 

OTHER USEFUL FUNCTIONS FOR UPDATING:

$set: Updates the value of a field or creates a field if it doesn't exist.

$unset: Removes a field from a document.

$inc: Increments the value of a numeric field by a specified amount. **** For likes

$push: Appends a value to an array field.

$pop: Removes the first or last element from an array field.

$pull: Removes elements matching a specified condition from an array field.

$addToSet: Adds a value to an array field if it doesn't already exist in the array.

$rename: Renames a field.

$mul: Multiplies the value of a numeric field by a specified amount.

$min: Updates a field to a specified value if the specified value is less than the current value.

$max: Updates a field to a specified value if the specified value is greater than the current value.


'''

@app.route('/complete_todo/<oid>')
def complete_todo(oid):
    todos_collection = mongo.db.todos
    # print(oid)

    todos_collection.update_one(
        {'_id': ObjectId(oid)},     # Get the item given it's object ID which is being converted from a string to an ID
        {'$set': {'complete': True}} # Set it's value to it's updated one
    )

    return redirect(url_for('index'))


@app.route('/delete_completed')
def delete_completed():
    todos_collection = mongo.db.todos
    
    # Look for everything that has the field complete as True, and will delete it
    todos_collection.delete_many(
        {'complete' : True}
    )

    return redirect(url_for('index'))


@app.route('/delete_all')
def delete_all():
    todos_collection = mongo.db.todos
    
    # Passing in an Empty dictionary represents getting everything
    todos_collection.delete_many({})

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
