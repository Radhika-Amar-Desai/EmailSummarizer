from flask import Flask, session, redirect, url_for, request, jsonify
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Only for testing on localhost

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CLIENT_SECRETS_FILE = os.environ['TEMP']  # Path to your client secret file

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
    """Reads and displays emails from a specific email address."""
    if 'credentials' not in session:
        return redirect(url_for('authorize'))

    credentials_dict = session['credentials']
    credentials = Credentials(
        token=credentials_dict['token'],
        refresh_token=credentials_dict.get('refresh_token'),
        token_uri=credentials_dict['token_uri'],
        client_id=credentials_dict['client_id'],
        client_secret=credentials_dict['client_secret'],
        scopes=credentials_dict['scopes']
    )

    # Initialize Gmail API service
    service = build('gmail', 'v1', credentials=credentials)

    try:
        # Fetch messages from the specified email address
        results = service.users().messages().list(userId='me').execute()
        #print(results[0])
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
                    # Parse the Date header to extract the time
                    raw_date = header['value']
                    email_info['time'] = raw_date  # Extract only the time
                    

            email_data.append(email_info)

        return jsonify(email_data)
    except Exception as e:
        # Handle token refresh or other errors
        return jsonify({'error': str(e)})


@app.route('/logout')
def logout():
    """Logs the user out by clearing the session."""
    session.clear()
    return redirect(url_for('authorize'))


if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)
