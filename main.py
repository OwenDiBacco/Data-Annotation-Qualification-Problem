from google.oauth2 import service_account
from googleapiclient.discovery import build
import re

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def get_credentials():
    return service_account.Credentials.from_service_account_file(
        'service-account.json', 
        scopes=SCOPES
    )

def extract_doc_id(url):
    match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', url)
    return match.group(1) if match else None


def connect_to_document(doc_url):
    creds = get_credentials()
    service = build('docs', 'v1', credentials=creds)

    # Extract document ID from URL
    doc_id = extract_doc_id(doc_url)
    if not doc_id:
        raise ValueError("Invalid Google Docs URL")

    # Get the document content
    document = service.documents().get(documentId=doc_id).execute()
    if not document:
        raise ValueError("Could not access document")

    return document


def print_document_cells(doc_url):
    try:
        # Get credentials and build service
        document = connect_to_document(doc_url)

        # Print content from each paragraph
        content = document.get('body', {}).get('content', [])
        for struct in content:
            if 'table' in struct:
                table = struct['table']
                for row in table.get('tableRows', []):
                    for cell in row.get('tableCells', []):
                        for content_item in cell.get('content', []):
                            for element in content_item.get('paragraph', {}).get('elements', []):
                                if 'textRun' in element:
                                    print(element['textRun']['content'].strip())

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    doc_url = input("Enter the Google Doc URL: ")
    print_document_cells(doc_url)