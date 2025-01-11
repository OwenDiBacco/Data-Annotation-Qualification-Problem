
import requests
import pandas as pd
from io import StringIO

def decode_secret_message(doc_url):
    # Get the content from Google Doc
    response = requests.get(doc_url)
    if response.status_code != 200:
        raise Exception("Failed to fetch document")

    # Parse the CSV data using pandas
    df = pd.read_csv(StringIO(response.text))

    # Find grid dimensions
    max_x = df['x'].max()
    max_y = df['y'].max()

    # Create empty grid filled with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Fill in the characters at their coordinates
    for _, row in df.iterrows():
        x, y, char = int(row['x']), int(row['y']), row['character']
        grid[y][x] = char

    # Print the grid
    for row in grid:
        print(''.join(row))

if __name__ == "__main__":
    try:
        decode_secret_message('https://docs.google.com/document/u/0/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZmCSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub?pli=1')
    except Exception as e:
        print(f"Error: {e}")
