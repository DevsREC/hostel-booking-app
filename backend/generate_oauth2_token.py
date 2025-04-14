# save this as generate_oauth2_token.py
import os
from google_auth_oauthlib.flow import InstalledAppFlow

# Set the scopes needed for email sending
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def generate_refresh_token(client_id, client_secret):
    client_config = {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token",
            "redirect_uris": ["http://localhost:8000/"]
        }
    }
    
    flow = InstalledAppFlow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/'
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent')
    print(f'Please go to this URL and authorize access: {auth_url}')
    
    code = input('Enter the authorization code: ').strip()
    flow.fetch_token(code=code)
    
    print(f"Refresh token: {flow.credentials.refresh_token}")
    print("Save this refresh token in your Django settings for django-gmailapi-backend")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--client_id', required=True, help='OAuth2 Client ID')
    parser.add_argument('--client_secret', required=True, help='OAuth2 Client Secret')
    args = parser.parse_args()
    
    generate_refresh_token(args.client_id, args.client_secret)