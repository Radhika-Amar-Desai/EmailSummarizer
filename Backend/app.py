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


@app.route('/logout')
def logout():
    """Logs the user out by clearing the session."""
    session.clear()
    return redirect(url_for('authorize'))


def fetch_emails(target_date=None):
    """
    Core logic for retrieving emails from Gmail.
    Automatically initiates OAuth flow if the user is not authenticated.
    """
    if 'credentials' not in session:
        # Redirect to the authorization route to authenticate the user
        raise ValueError("User is not authenticated")

    credentials_dict = session['credentials']
    credentials = Credentials(
        token=credentials_dict['token'],
        refresh_token=credentials_dict.get('refresh_token'),
        token_uri=credentials_dict['token_uri'],
        client_id=credentials_dict['client_id'],
        client_secret=credentials_dict['client_secret'],
        scopes=credentials_dict['scopes']
    )

    # Check if token has expired and refresh if possible
    if credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
            # Save the refreshed credentials back to the session
            session['credentials'] = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
        except Exception as e:
            raise ValueError(f"Token refresh failed: {e}")

    service = build('gmail', 'v1', credentials=credentials)

    if not target_date:
        target_date = datetime.datetime.now().date()

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

        email_data.append(email_info)

    return email_data


@app.route('/read_emails', methods=['POST'])
def read_emails():
    try:
        target_date = request.json  # Example date logic
        emails = fetch_emails(target_date=target_date)
        return jsonify(emails)
    except ValueError as e:
        if "User is not authenticated" in str(e):
            # Redirect to the authorize route if not authenticated
            return redirect(url_for('authorize'))
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_classified_summary', methods=['POST'])
def get_classified_summary():
    try:
        target_date = request.json
        emails = fetch_emails(target_date=target_date)  # Reuse the same logic

        summaries = summarize.generate_summary(emails)
        
        categories = request.json    
        categorized_summaries = classify.classify_emails(summaries, categories)
        
        return jsonify({'classified_summaries': categorized_summaries})
    
    except ValueError as e:
        
        if "User is not authenticated" in str(e):
            return redirect(url_for('authorize'))
        
        return jsonify({'error': str(e)}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)