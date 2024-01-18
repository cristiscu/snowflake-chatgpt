import csv
import requests
from bs4 import BeautifulSoup

# Define the URL of the page to scrape
url = 'https://sandbox.oxylabs.io/products'

# Add headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
}

# Send request to download the content of the page
response = requests.get(url, headers=headers)

# Ensure we have a successful response
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all game containers
    games = soup.select('div.container > div.row > div.col-3')

    # Prepare the list that will store our records
    game_list = []

    for game in games:
        # Scrape the title and price
        title = game.find('a', class_='card-header').h4.get_text(strip=True)
        price = game.find('div', class_='price-wrapper').get_text(strip=True)

        # Clean up any undesirable symbols if necessary
        title = title.replace('&amp;', '&').replace('&#39;', "'")
        price = price.replace('&amp;', '&').replace('&#39;', "'")

        # Append the title and price as a tuple into the game list
        game_list.append((title, price))

    # Write to a CSV file
    with open('6-web-scraping.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['Title', 'Price'])
        # Write the contents
        writer.writerows(game_list)

    print('Scraping completed and data saved to 6-web-scraping.csv')
else:
    print(f'Failed to retrieve web page content. Status code: {response.status_code}')
