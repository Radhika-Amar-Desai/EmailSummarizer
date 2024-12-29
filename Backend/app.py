from flask import Flask, session, redirect, url_for, request, jsonify
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from pymongo import MongoClient
import os
import datetime
import summarize
import classify


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Only for testing on localhost

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CLIENT_SECRETS_FILE = os.environ['TEMP']  # Path to your client secret file

# MongoDB connection setup
mongo_client = MongoClient("mongodb://localhost:27017/")
email_db = mongo_client["email_database"]  # Database name
emails_collection = email_db["emails"]  # Collection name
categorized_summaries_collection = email_db["categorized_summaries"]



@app.route('/authorize')
def authorize():
    """Initiates the OAuth flow."""
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',  # Ensures refresh_token is obtained
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    """Handles the OAuth callback."""
    state = session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(url_for('read_emails'))


@app.route('/read_emails')
def read_emails():
    """Reads emails from the main inbox received on a specific date provided in the POST request."""
    if 'credentials' not in session:
        return redirect(url_for('authorize'))

    # Parse the date from the POST request
    try:
        # data = request.json
        target_date = "2024-12-28"

        if not target_date:
            return jsonify({'error': 'Date is required in the request body'}), 400

        # Validate the date format
        try:
            target_date = datetime.datetime.strptime(target_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    credentials_dict = session['credentials']
    credentials = Credentials(
        token=credentials_dict['token'],
        refresh_token=credentials_dict.get('refresh_token'),
        token_uri=credentials_dict['token_uri'],
        client_id=credentials_dict['client_id'],
        client_secret=credentials_dict['client_secret'],
        scopes=credentials_dict['scopes']
    )

    service = build('gmail', 'v1', credentials=credentials)

    try:
        # Fetch messages from the main inbox on the specified date
        query = f"label:INBOX after:{target_date} before:{target_date + datetime.timedelta(days=1)}"
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        email_data = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            headers = msg['payload'].get('headers', [])

            email_info = {
                'id': message['id'],
                'snippet': msg.get('snippet', '')
            }

            for header in headers:
                if header['name'] == 'From':
                    email_info['from'] = header['value']
                elif header['name'] == 'Date':
                    email_info['time'] = header['value']

            # Save email to MongoDB
            emails_collection.insert_one(email_info)

            # Remove the `_id` field (it will be added automatically by MongoDB)
            if '_id' in email_info:
                del email_info['_id']

            email_data.append(email_info)

        return jsonify(email_data)
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/logout')
def logout():
    """Logs the user out by clearing the session."""
    session.clear()
    return redirect(url_for('authorize'))


@app.route('/get_classified_summary')
def get_classified_summary():
    """
    Retrieves email summaries, classifies them based on user-defined categories,
    and returns a JSON object with classified summaries.
    """
    try:
        
        emails = list(emails_collection.find({}, {"_id": 0}))  # Exclude the MongoDB `_id` field
        if not emails:
            return jsonify({'error': 'No emails found in the database'}), 404
        
        summaries = summarize.generate_summary(emails)
        categories = ["VIT related", "others"]
        categorized_summaries = classify.classify_emails(summaries, categories)
        
        # categorized_summary_docs = [
        #     {"content": summary["content"], "category": summary["label"]}
        #     for summary in categorized_summaries
        # ]
        
        # categorized_summaries_collection.insert_many(categorized_summary_docs)
        
        return jsonify({'classified_summaries': categorized_summaries})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)
