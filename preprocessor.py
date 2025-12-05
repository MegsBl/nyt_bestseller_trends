import requests
import pandas as pd
from datetime import datetime, timedelta
import config

# NYT API endpoint
url = "https://api.nytimes.com/svc/books/v3/lists/{date}/{list_name}.json"

# Setting the start and end dates
start_date = datetime(2025, 6, 1)
end_date = datetime(2025, 12,1)

lists_to_pull = ["hardcover-fiction"]

# Empty list to collect all data
all_books = []

current_date = start_date
while current_date <= end_date:
    for list_name in lists_to_pull:
        url = url.format(
            date=current_date.strftime("%Y-%m-%d"),
            list_name=list_name
        )
        response = requests.get(url, params={"api-key": config.NYT_BOOK_API})
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            for item in results['books']:
                book = {
                    "date": current_date.strftime("%Y-%m-%d"),
                    "list_name": list_name,
                    "title": item['title'],
                    "author": item['author'],
                    "publisher": item['publisher'],
                    "rank": item['rank'],
                    "weeks_on_list": item['weeks_on_list'],
                    "description": item['description']
                }
                all_books.append(book)
        elif response.status_code == 404:
            print(f"No data found for {list_name} on {current_date}")
        else:
            print(f"Error {response.status_code} on {current_date} for {list_name}")
    
    current_date += timedelta(weeks=1)

# Convert to DataFrame
df_all = pd.DataFrame(all_books)

# Save to a single CSV file
df_all.to_csv("hardcovers_nyt_bestsellers_2025.csv", index=False)


