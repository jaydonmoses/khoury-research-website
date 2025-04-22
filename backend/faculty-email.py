from flask import Flask, render_template, request, url_for
import pandas as pd
import os

app = Flask(__name__, template_folder='../templates')

# Load faculty data
file_path = os.path.join(os.path.dirname(__file__), "data", "khoury_faculty_data.csv")
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

@app.route('/generate-email/<faculty_email>')
def generate_email_page(faculty_email):
    faculty_member = df[df['Email'] == faculty_email].iloc[0] if len(df[df['Email'] == faculty_email]) > 0 else None
    return render_template('generate-email.html', faculty=faculty_member)

if __name__ == '__main__':
    app.run(debug=True)
