from flask import Flask, request, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

# Load college data from CSV
def load_colleges():
    colleges = []
    with open('colleges.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            colleges.append(row)
    return colleges

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    stream = data.get('stream')
    subjects = data.get('subjects', [])
    marks = int(data.get('marks', 0))
    interests = data.get('interests', [])
    state = data.get('state')

    colleges = load_colleges()
    matches = []

    for college in colleges:
        if stream.lower() in college['Stream'].lower():
            if int(college['Cutoff']) <= marks:
                if state.lower() in college['State'].lower():
                    matches.append(college)

    return jsonify({
        "status": "success",
        "recommendations": matches[:10]
    })

if __name__ == '__main__':
    app.run(debug=True)
