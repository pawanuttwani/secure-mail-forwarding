from flask import Flask, request, redirect, url_for, flash, render_template
import requests
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

API_KEY = 'sk_4dd7bf04061449aab0647c4867dd81a7'
DOMAIN = 'secureemailforwarding.tech'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_alias', methods=['POST'])
def create_alias():
    alias = request.form['alias']  # Only the alias part
    forward_to = request.form['forward_to']
    
    # Construct the API request to create the alias with full domain
    full_alias = f"{alias}@{DOMAIN}"  # Full alias with domain
    url = f'https://api.improvmx.com/v3/domains/{DOMAIN}/aliases/'
    headers = {
        'Authorization': f'Basic api:{API_KEY}',
        'Content-Type': 'application/json'
    }
    data = json.dumps({"alias": alias, "forward": forward_to})  # Alias part remains the same

    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()

    if response_data.get('success'):
        flash(f'Alias "{full_alias}" successfully created!', 'success')
    else:
        # Check for specific error messages
        error_message = response_data.get('errors', {}).get('alias', ['An unknown error occurred.'])[0]
        
        # Customize the error message for the already registered alias
        if "If you want to add multiple emails for an alias" in error_message:
            flash('This alias is already registered. Please choose another.', 'danger')
        else:
            flash(f'Error: {error_message}', 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
