from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://127.0.0.1:27017")
db = client['mydatabase']

# Collections
person_collection = db['people']
call_log_collection = db['app']

# Route to add person data
@app.route('/add_person', methods=['POST'])
def add_person():
    data = request.json
    if 'name' in data and 'email' in data and 'number' in data:
        person = {
            'name': data['name'],
            'email': data['email'],
            'number':data['number']
        }
        person_collection.insert_one(person)
        return jsonify({'message': 'Person added successfully!'}), 201
    else:
        return jsonify({'message': 'Invalid data'}), 400

# Route to fetch person data
@app.route('/get_persons', methods=['GET'])
def get_persons():
    persons = list(person_collection.find({}, {'_id': 0}))  # Exclude the '_id' field from the result
    return jsonify(persons), 200

# Route to add multiple call log data
@app.route('/add_call_logs', methods=['POST'])
def add_call_logs():
    data = request.json
    if isinstance(data, list):
        call_logs = []
        for log in data:
            if 'number' in log and 'type' in log and 'date' in log and 'duration' in log:
                call_logs.append({
                    'number': log['number'],
                    'type': log['type'],
                    'date': log['date'],
                    'duration': log['duration']
                })
            else:
                return jsonify({'message': 'Invalid data in one of the call logs'}), 400
        call_log_collection.insert_many(call_logs)
        return jsonify({'message': 'Call logs added successfully!'}), 201
    else:
        return jsonify({'message': 'Invalid data format'}), 400

# Route to fetch call log data
@app.route('/get_call_logs', methods=['GET'])
def get_call_logs():
    call_logs = list(call_log_collection.find({}, {'_id': 0}))  # Exclude the '_id' field from the result
    return jsonify(call_logs), 200

if __name__ == '__main__':
    app.run(debug=True)
