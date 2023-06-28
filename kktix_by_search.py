import csv
import requests
from bs4 import BeautifulSoup

base_url = 'https://kktix.com/events'
search_params = {'search': '喜劇', 'start_at': '2023/06/26'}

# Define the output CSV file name
output_file = 'kktix_by_search.csv'

# 'theme', 'location', 'date', 'time', 'img src', 'link', 'organizer', 'tags'
# Open the output CSV file in write mode
with open(output_file, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['theme', 'date', 'img src', 'link'])

    for page in range(1, 6):  # Fetch results for pages 1 to 5
        search_params['page'] = str(page)

        # Make the request
        response = requests.get(base_url, params=search_params)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all 開賣中 event listings on the page 
        event_listings = soup.find_all('li', class_='type-selling')

        # Iterate over each HTML element and extract the desired information
        for element in event_listings:
            event_title = element.select_one('.event-title h2').text.strip()
            event_date = element.select_one('.date').text.strip().split('(')[0]
            image_url = element.select_one('img')['src']
            event_url = element.select_one('a.cover')['href']
            writer.writerow([event_title, event_date, image_url, event_url])

print(f"CSV file '{output_file}' has been created successfully.")
