from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb://127.0.0.1:27017")
db = client['mydatabase']

# Collections
question_collection = db['questions']

# Route to add multiple question data
@app.route('/add_questions', methods=['POST'])
def add_questions():
    data = request.json
    if isinstance(data, list):
        questions_to_add = []
        duplicate_questions = []
        for question in data:
            if 'question' in question:
                exiting_question = question_collection.find_one({'question': question['question']})
                if not exiting_question:
                    questions_to_add.append({
                        'question': question['question']
                    })
                else:
                    duplicate_questions.append(question['question'])
            else:
                return jsonify({'message': 'Invalid data in one of the question format'}), 400

        if questions_to_add:
            question_collection.insert_many(questions_to_add)

        response = {
            'message' : 'Question Processed.',
            'added_questions':[q['question'] for q in questions_to_add],
            'duplicate_question': duplicate_questions
        }
        return jsonify(response), 201
    else:
        return jsonify({'message': 'Invalid data format'}), 400

# Route to update a question
@app.route('/update_question', methods=['PUT'])
def update_question():
    data = request.json
    if 'old_question' in data and 'new_question' in data:
        old_question = data['old_question']
        new_question = data['new_question']

        # Check if the old question exists
        existing_question = question_collection.find_one({'question': old_question})
        if existing_question:
            # Check if the new question is a duplicate
            duplicate_question = question_collection.find_one({'question': new_question})
            if duplicate_question:
                return jsonify({'message': 'New question already exists as a duplicate.'}), 400

            # Update the question
            question_collection.update_one({'question': old_question}, {'$set': {'question': new_question}})
            return jsonify({'message': 'Question updated successfully!'}), 200
        else:
            return jsonify({'message': 'Old question not found.'}), 404
    else:
        return jsonify({'message': 'Invalid data format. Both "old_question" and "new_question" are required.'}), 400

# Route to delete a question
@app.route('/delete_question', methods=['DELETE'])
def delete_question():
    data = request.json
    if 'question' in data:
        question = data['question']

        # Check if the question exists
        existing_question = question_collection.find_one({'question': question})
        if existing_question:
            question_collection.delete_one({'question': question})
            return jsonify({'message': 'Question deleted successfully!'}), 200
        else:
            return jsonify({'message': 'Question not found.'}), 404
    else:
        return jsonify({'message': 'Invalid data format. "question" is required.'}), 400

# Route to fetch question data
@app.route('/get_questions', methods=['GET'])
def get_questions():
    questions = list(question_collection.find({}, {'_id': 0}))
    return jsonify(questions), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
