from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
import os

app = Flask(__name__, template_folder='../templates')

# Load faculty data
file_path = os.path.join(os.path.dirname(__file__), "data", "khoury_faculty_data.csv")
df = pd.read_csv(file_path)

def get_faculty_data():
    return df.to_dict(orient='records')

def generate_email_templates(professor):
    return {
        "research": {
            "subject": f"Research Assistant Position Inquiry",
            "body": f"""Dear Professor {professor['Name'].split()[-1]},

I hope this email finds you well. I am writing to express my interest in joining your research team as a Research Assistant. 
I am deeply impressed by your work in {professor['Research Interests'].split(';')[0] if pd.notna(professor['Research Interests']) else 'your field'}.

Thank you for your time and consideration.

Best regards,
[Your Name]"""
        },
        "recommendation": {
            "subject": "Letter of Recommendation Request",
            "body": f"""Dear Professor {professor['Name'].split()[-1]},

I hope this email finds you well. I am writing to request a letter of recommendation.

Thank you for considering my request.

Best regards,
[Your Name]"""
        },
        "ta": {
            "subject": "Teaching Assistant Position Interest",
            "body": f"""Dear Professor {professor['Name'].split()[-1]},

I hope this email finds you well. I am writing to express my interest in serving as a Teaching Assistant.

Thank you for your consideration.

Best regards,
[Your Name]"""
        }
    }

@app.route('/')
def index():
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
    faculty_matches = df[df['Email'] == faculty_email]
    if faculty_matches.empty:
        return "Faculty member not found", 404
    
    faculty_member = faculty_matches.iloc[0].to_dict()
    templates = generate_email_templates(faculty_member)
    return render_template('generate-email.html', faculty=faculty_member, templates=templates)

@app.route('/get_template', methods=['POST'])
def get_template():
    data = request.get_json()
    faculty_email = data.get('email')
    template_type = data.get('template_type')
    
    faculty_member = df[df['Email'] == faculty_email].iloc[0].to_dict()
    templates = generate_email_templates(faculty_member)
    
    return templates.get(template_type, {"error": "Template not found"})

if __name__ == '__main__':
    app.run(debug=True)
