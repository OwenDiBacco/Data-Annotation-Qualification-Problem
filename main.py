
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import re

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def extract_doc_id(url):
    match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', url)
    return match.group(1) if match else None

def decode_secret_message(doc_url):
    # Get credentials and build service
    creds = get_credentials()
    service = build('docs', 'v1', credentials=creds)
    
    # Extract document ID from URL
    doc_id = extract_doc_id(doc_url)
    if not doc_id:
        raise ValueError("Invalid Google Docs URL")
    
    # Get the document content
    document = service.documents().get(documentId=doc_id).execute()
    
    # Parse the content to get coordinates and characters
    grid_points = []
    content = document.get('body').get('content')
    
    for element in content:
        if 'paragraph' in element:
            paragraph = element.get('paragraph').get('elements')[0].get('textRun').get('content')
            # Skip empty lines
            if not paragraph.strip():
                continue
                
            # Parse coordinates and character
            try:
                parts = paragraph.strip().split()
                if len(parts) >= 3:
                    x = int(parts[0])
                    y = int(parts[1])
                    char = parts[2]
                    grid_points.append((x, y, char))
            except (ValueError, IndexError):
                continue
    
    # Find grid dimensions
    max_x = max(point[0] for point in grid_points) + 1
    max_y = max(point[1] for point in grid_points) + 1
    
    # Create empty grid
    grid = [[' ' for _ in range(max_x)] for _ in range(max_y)]
    
    # Fill in the characters
    for x, y, char in grid_points:
        grid[y][x] = char
    
    # Print the grid
    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    # Example usage
    doc_url = input("Enter the Google Doc URL: ")
    decode_secret_message(doc_url)
