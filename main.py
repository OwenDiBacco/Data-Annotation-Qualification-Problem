from google.oauth2 import service_account
from googleapiclient.discovery import build
import re

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def get_credentials():
    return service_account.Credentials.from_service_account_file(
        'service-account.json', 
        scopes=SCOPES
    )


def connect_to_document(doc_id):
    creds = get_credentials()
    service = build('docs', 'v1', credentials=creds)
    document = service.documents().get(documentId=doc_id).execute()
    return document


def get_document_cells(doc_id):
    document = connect_to_document(doc_id)
    content = document.get('body', {}).get('content', [])
    cell_contents = []
    for struct in content:
        if 'table' in struct:
            table = struct['table']
            for row in table.get('tableRows', []):
                for cell in row.get('tableCells', []):
                    for content_item in cell.get('content', []):
                        for element in content_item.get('paragraph', {}).get('elements', []):
                            if 'textRun' in element:
                                cell_contents.append(element['textRun']['content'].strip())
                                
    cell_contents = cell_contents[3:]
    return cell_contents


def display_code(cell_contents):
    max_x = max(cell_contents[i] for i in range(0, len(cell_contents), 3))
    max_y = max(cell_contents[i + 2] for i in range(0, len(cell_contents), 3))

    print(max_x, ' ', max_y)
    
    result = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)] 
    # result = [[' ' for _ in range(max_x + 1)] * max_y]

    for i in range(0, len(cell_contents), 3):
        x = cell_contents[i]  
        y = cell_contents[i + 2]  
        content = cell_contents[i + 1]
        result[y][x] = content

    return result

if __name__ == "__main__":
    cell_contents = get_document_cells('1TLfFu_HQ8uvIYyrfFuiWWUxb6yRTxG5cKW_NciGCefs')
    code = display_code(cell_contents)
    print(code)