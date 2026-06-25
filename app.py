from flask import Flask, request, render_template, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import os
from urllib.parse import quote_plus

app = Flask(__name__)


dbUser = os.getenv("MONGODB_USERNAME")
dbPassword = os.getenv("MONGODB_PASSWORD")
dbName = os.getenv("MONGODB_DB_NAME", "mytododb")   # default if not set
dbHost = os.getenv("MONGODB_HOST", "cluster0.mp3lyec.mongodb.net")
appName = os.getenv("MONGODB_APP_NAME", "Cluster0")

if not dbUser or not dbPassword:
    raise ValueError("MONGODB_USERNAME or MONGODB_PASSWORD is not set")

uri = (
    f"mongodb+srv://{quote_plus(dbUser)}:{quote_plus(dbPassword)}@{dbHost}/{dbName}"
    f"?retryWrites=true&w=majority&appName={quote_plus(appName)}"
)


if not uri:
    raise ValueError("MONGO_URI environment variable is not set")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"MongoDB connection error: {e}")

db = client.mytododb
students_collection = db.students


@app.route('/pupil')
def home():
    students = students_collection.find()
    return render_template('index.html', students=students)


@app.route('/pupil_add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        student_data = {
            'fname': request.form['fname'],
            'lname': request.form['lname'],
            'Gender': request.form['Gender'],
            'ID': request.form['ID'],
            'Subject': request.form['Subject'],
            'phone': request.form['phone'],
            'AdminDate': request.form['AdminDate']
        }
        students_collection.insert_one(student_data)
    return redirect(url_for('home'))


@app.route('/pupil_delete_student/<student_id>', methods=['GET'])
def delete_student(student_id):
    students_collection.delete_one({'_id': ObjectId(student_id)})
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8002)
