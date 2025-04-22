from flask import Flask, request, jsonify, render_template
import csv

app = Flask(__name__)

# Load professor data from a CSV file
professors = []
with open('khoury_faculty_data.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        professors.append({
            "name": row["Name"],
            "position": row["Position"],
            "research_interest": row["Research Interests"],
        })

@app.route('/suggest', methods=['GET'])
def suggest_professors():
    # Get query parameters
    position = request.args.get('position')
    research_interest = request.args.get('research_interest')
    search = request.args.get('search')

    # Filter professors based on query parameters
    suggestions = [
        prof for prof in professors
        if (not position or prof['position'].lower() == position.lower()) and
           (not research_interest or research_interest.lower() in prof['research_interest'].lower()) and
           (not search or search.lower() in prof['name'].lower() or search.lower() in prof['research_interest'].lower())
    ]

    return jsonify(suggestions)

@app.route('/')
def index():
    return render_template('faculty-suggestion.html')

if __name__ == '__main__':
    app.run(debug=True)