# 507-project

Informaton contained in this README:

- Please obtain your personal API key from Yelp: please visit https://www.yelp.com/developers/documentation/v3/authentication

- Required Python packages for your project to work:
- import requests
- import secrets # file that contains your API key
- import sqlite3
- import time
- import plotly.graph_objects as go

- URLs for data and documentation: https://www.yelp.com/developers/documentation/v3/business_search
https://www.yelp.com/developers/documentation/v3/business_reviews

- The program will ask for a city name and a food category in two command lines, and then return the top 50 restaurants based on the input, and the restaurant name, category, review, rating, address, city, state, zip code, the phone number will be retrieved. The restaurants are ranked by their rating scores in Yelp.com, while 5/5 is the highest, and 0/5 is the lowest. The total review number will also be presented for users to determine whether a restaurant’s rating is reliable. The reason to include the category in the result is that some restaurants might fall into a large, more general category while selling a more specific food. For example, a restaurant might fall into the category of “Mexican”, but has a more specific genre as “Breakfast & Brunch.”

- The program will allow users to use the command line to filter the results, such as only search restaurants in one city, and the result will be saved in the SQL database.
The program will use Plotly to show the comparison between restaurants, such as using a bar chart to show the rating scores. The users will be able to: 1) See a scatter graph comparison of total review counts and ratings for your current search result. 2)See a bar chart comparison of ratings between different restaurants for your current search result. 3) See a bar chart comparison of total review counts and ratings for your current search result. 4) See a bar chart comparison of total review counts between different restaurants for your current search result.

