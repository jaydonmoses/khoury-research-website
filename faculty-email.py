from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load faculty data
file_path = "khoury_faculty_data.csv"  # Updated path
df = pd.read_csv(file_path)

def get_faculty_data():
    # Convert the DataFrame to a list of dictionaries for template rendering
    return df.to_dict(orient='records')

@app.route('/')
def index():
    # Fetch faculty data and pass it to the template
    faculty_data = get_faculty_data()
    return render_template('index.html', faculty=faculty_data)

@app.route('/send_email', methods=['POST'])
def send_email():
    selected_emails = request.form.getlist('emails')
    if selected_emails:
        mailto_links = [f"mailto:{email}" for email in selected_emails]
        script = "".join([f"window.open('{link}', '_blank');" for link in mailto_links])
        return f"<script>{script}</script>"
    return "<script>alert('Please select at least one professor to email.'); window.history.back();</script>"

if __name__ == '__main__':
    app.run(debug=True)
