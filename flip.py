import requests
from selenium import webdriver
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup

## Headers for request and response
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'}

## Access the browser
# Set the path
path = 'C://chromedriver.exe'
# Setup the browser
browser = webdriver.Chrome(executable_path=path)

## Load the Flipkart webpage
## According to the search query
# load the webpage
search_query = 'laptops'.replace(' ','+')
base_url = 'https://www.flipkart.com/search?q={0}'.format(search_query)
browser.get(base_url)

## Scrape the data
# Empty lists to store the scraped data
product_names=[]
price = []
ratings = []

# Scraping code
for i in range(1, 11):
    print('Processing {0}'.format(base_url + '&page={0}'.format(i)))
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    product = soup.find_all('div', {'class':"_4rR01T"})
    cost = soup.find_all('div', {'class': '_30jeq3 _1_WHN1'})
    rating = soup.find_all('div', {'class': '_3LWZlK'})
    sleep(1)

    # Appending the scraped data to the lists and storing them
    for p in product:
        product_names.append(p.text)

    for c in cost:
        price.append((c.text)[1:])

    for r in rating:
        ratings.append(r.text)

    # Truncate the ratings list to match the length of other lists
    ratings = ratings[:len(product_names)]

## Display all the product names
for name in product_names:
    print(name)

## Display the price of each product
for p in price:
    print(p)

## Display the rating of each product
for r in ratings:
    print(r)

## Check the length of each column
print("Products: ", len(product_names))
print("Price: ", len(price))
print("Ratings: ", len(ratings))

## Defining a dictionary holding the columns
data = {
    'Product Name': product_names,
    'Price': price,
    'Rating': ratings
}

# Creating a DataFrame
df = pd.DataFrame(data)

## Getting the first 5 rows of our Scraped Data
df.head()

df.shape

## Let's convert the dataframe to CSV and Export
df.to_csv('laptops.csv', index=False)
