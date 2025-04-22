from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
professors_df = pd.read_csv("khoury_faculty_data.csv")
professors_df["Name"] = professors_df["Name"].astype(str)  # Ensure all names are strings
print(professors_df.head())  # Print the first few rows of the DataFrame

TEMPLATES_FILE = "email_templates.json"

# Load existing templates or create a default structure
if os.path.exists(TEMPLATES_FILE):
    with open(TEMPLATES_FILE, "r") as file:
        custom_templates = json.load(file)
else:
    custom_templates = {
        "Research Assistant": """
        Dear Professor {name},

        I hope this email finds you well. I am writing to express my interest in joining your research team as a Research Assistant. 
        I am deeply impressed by your work in [specific field or project], and I believe my skills and experience align well with your research goals.

        I would greatly appreciate the opportunity to discuss how I can contribute to your ongoing projects. 
        Please let me know a time that works for you.

        Thank you for your time and consideration.

        Best regards,
        [Your Name]
        """,
        "Letter of Recommendation": """
        Dear Professor {name},

        I hope this email finds you well. I am reaching out to kindly request a letter of recommendation from you. 
        Your guidance and mentorship during [specific course or project] have been invaluable, and I believe your recommendation would greatly strengthen my application for [specific program or opportunity].

        Please let me know if you would be willing to assist me with this. I would be happy to provide any additional information or materials you may need.

        Thank you for your time and support.

        Best regards,
        [Your Name]
        """,
        "Teaching Assistant": """
        Dear Professor {name},

        I hope this email finds you well. I am writing to express my interest in serving as a Teaching Assistant for your course, [specific course name]. 
        Having excelled in this course and gained a strong understanding of the material, I am confident in my ability to assist students effectively.

        I would greatly appreciate the opportunity to discuss this role further. Please let me know if there is a convenient time to meet.

        Thank you for your time and consideration.

        Best regards,
        [Your Name]
        """
    }

@app.route("/")
def index():
    return render_template("generate-email.html")

@app.route("/get_professor", methods=["POST"])
def get_professor():
    # Get the input name from the frontend
    input_name = request.form["name"].lower()

    # Get all names from the CSV file
    all_names = professors_df["Name"].str.lower()

    # Find rows that contain the input string
    matching_professors = professors_df[all_names.str.contains(input_name, na=False)]

    # If matches are found, return them as a list of dictionaries
    if not matching_professors.empty:
        return jsonify({
            "professors": matching_professors.to_dict(orient="records"),
            "first_professor_name": matching_professors.iloc[0]["Name"]  # Include the first professor's name
        })

    # If no matches are found, return an error message
    return jsonify({"error": "No professor found"})

@app.route("/get_templates", methods=["GET"])
def get_templates():
    # Return the list of custom templates as a JSON response
    return jsonify({"templates": custom_templates})

@app.route("/upload_template", methods=["POST"])
def upload_template():
    # Get the template name and content from the request
    template_name = request.form["template_name"]
    template_content = request.form["template_content"]

    # Save the new template
    custom_templates[template_name] = template_content
    with open(TEMPLATES_FILE, "w") as file:
        json.dump(custom_templates, file)

    return jsonify({"message": "Template uploaded successfully", "templates": custom_templates})

@app.route("/generate_email", methods=["POST"])
def generate_email():
    # Get the professor's name and purpose of the email from the frontend
    name = request.form["name"]
    reason = request.form["reason"]

    # Use the custom template if it exists
    if reason in custom_templates:
        email_template = custom_templates[reason].replace("{name}", name)
    else:
        # Default template for other purposes
        email_template = f"""
        Dear Professor {name},

        I hope this email finds you well. I am reaching out to you regarding {reason}. 
        I believe that your expertise and insights would be invaluable, and I would greatly appreciate the opportunity to discuss this further with you.

        Please let me know a time that works for you, and I will be happy to accommodate your schedule.

        Thank you for your time and consideration.

        Best regards,
        [Your Name]
        """

    # Return the generated email as a JSON response
    return jsonify({"email": email_template, "templates": custom_templates})

if __name__ == "__main__":
    app.run(debug=True)
