from flask import Flask, render_template, request
import os  # Add this import
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

def check_for_leaks(html_content, organization_name, sensitive_data):
    soup = BeautifulSoup(html_content, 'html.parser')
    leaked_data = []

    for data_type, patterns in sensitive_data.items():
        for pattern in patterns:
            matches = re.findall(pattern, soup.get_text(), re.IGNORECASE)
            if matches:
                leaked_data.extend(matches)

    return leaked_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_leaks', methods=['POST'])
def check_leaks():
    # Get the absolute path to the dark_web.html file
    dark_web_path = os.path.join(os.path.dirname(__file__), 'data', 'dark_web.html')

    # Check if the file exists before attempting to open it
    if os.path.exists(dark_web_path):
        with open(dark_web_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Define sensitive data patterns to check for in the HTML content
        sensitive_data_patterns = {
            'Names': ["John Doe", "Jane Smith", "Bob Johnson", "Alice Williams"],
            'Emails': [r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'],
            'Phone Numbers': [r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'],
            'Passwords': [r'\bpassword\b', r'\b123456\b', r'\bqwerty\b']
        }

        # Check for leaks in the simulated HTML content
        leaked_data = check_for_leaks(html_content, "MyCompany", sensitive_data_patterns)

        return render_template('index.html', leaked_data=leaked_data)

    else:
        return "Error: dark_web.html file not found."

if __name__ == '__main__':
    app.run(debug=True)