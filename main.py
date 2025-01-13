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
        # print("Document contents: ", content)
        table = content['element']['table']
        for row in table['tableRows']:
            for cell in row['tableCells']:
                for paragraph in cell['content']:
                    for element in paragraph['elements']:
                        if 'textRun' in element:
                            text_run = element['textRun']
                            cell_text = text_run['content']
                            print(cell_text)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    doc_url = input("Enter the Google Doc URL: ")
    print_document_cells(doc_url)