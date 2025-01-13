
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

def decode_secret_message(doc_url):
    try:
        # Get credentials and build service
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

        # Parse the content to get coordinates and characters
        grid_points = []
        content = document.get('body', {}).get('content', [])
        
        print("Reading document content:")
        for element in content:
            if 'paragraph' in element:
                try:
                    paragraph = element.get('paragraph').get('elements')[0].get('textRun').get('content')
                    line = paragraph.strip()
                    
                    # Print raw cell data
                    if line:
                        print(f"\nRaw line: {line}")
                        parts = line.split('|')
                        parts = [p.strip() for p in parts if p.strip()]
                        print(f"Cells: {parts}")
                    
                    # Skip empty lines
                    if not line:
                        continue
                        
                    # Skip lines without our special characters
                    if not any(c in line for c in ['█', '▀']):
                        continue
                    
                    parts = line.split('|')
                    parts = [p.strip() for p in parts if p.strip()]
                    
                    # Process each coordinate set in the line
                    for i in range(0, len(parts), 3):
                        if i + 2 < len(parts):
                            try:
                                x = int(parts[i].strip())
                                char = parts[i + 1].strip()
                                y = int(parts[i + 2].strip())
                                if char in ['█', '▀']:  # Only accept valid characters
                                    grid_points.append((x, y, char))
                                    print(f"Added point: ({x}, {y}, {char})")
                            except (ValueError, IndexError) as e:
                                print(f"Error parsing coordinate set: {e}")
                                continue
                except (ValueError, IndexError) as e:
                    print(f"Error parsing line: {e}")
                    continue
                except AttributeError as e:
                    print(f"Error accessing paragraph content: {e}")
                    continue

        # Check if we have any valid points
        if not grid_points:
            print("No valid coordinates found in the document.")
            return

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
            
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
    finally:
        print("Document processing completed")

if __name__ == "__main__":
    # Example usage
    doc_url = input("Enter the Google Doc URL: ")
    decode_secret_message(doc_url)
