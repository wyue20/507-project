#################################
##### Name: Yue Wang   ##########
##### Uniqname: wnyue  ##########
#################################

import requests
import json
import secrets # file that contains your API key
import sqlite3
import time
import plotly.graph_objects

api_key = secrets.API_KEY
CACHE_FILENAME = "yelp_cache.json"
# EVENT_FILENAME = "event_cache.json"
CACHE_DICT = {}
headers = {'Authorization': 'Bearer %s' % api_key}

#cache, some codes are from previous homework#
def open_cache():
	''' Opens the cache file if it exists and loads the JSON into
	the CACHE_DICT dictionary.
	if the cache file doesn't exist, creates a new cache dictionary
	
	Parameters
	----------
	None
	
	Returns
	-------
	The opened cache: dict
	'''
	try:
		cache_file = open(CACHE_FILENAME, 'r')
		cache_contents = cache_file.read()
		cache_dict = json.loads(cache_contents)
		cache_file.close()
	except:
		cache_dict = {}
	return cache_dict

def open_event_cache():
	''' Opens the cache file if it exists and loads the JSON into
	the CACHE_DICT dictionary.
	if the cache file doesn't exist, creates a new cache dictionary
	
	Parameters
	----------
	None
	
	Returns
	-------
	The opened cache: dict
	'''
	try:
		cache_file = open(EVENT_FILENAME, 'r')
		cache_contents = cache_file.read()
		cache_dict = json.loads(cache_contents)
		cache_file.close()
	except:
		cache_dict = {}
	return cache_dict

def save_cache(cache_dict):
	''' Saves the current state of the cache to disk
	
	Parameters
	----------
	cache_dict: dict
		The dictionary to save
	
	Returns
	-------
	None
	'''
	dumped_json_cache = json.dumps(cache_dict) 
	fw = open(CACHE_FILENAME,"w")
	fw.write(dumped_json_cache)
	fw.close() 

def construct_unique_key(baseurl, params):
	''' constructs a key that is guaranteed to uniquely and 
	repeatably identify an API request by its baseurl and params
	Parameters
	----------
	baseurl: string
		The URL for the API endpoint
	params: dictionary
		A dictionary of param: param_value pairs
	Returns
	-------
	string
		the unique key as a string
	'''
	param_strings = []
	connector = '_'
	for k in params.keys():
		param_strings.append(f'{k}_{params[k]}')
	param_strings.sort()
	unique_key = baseurl + connector +  connector.join(param_strings)
	return unique_key

def make_request(unique_key, params, headers, cache):
    if (unique_key in cache.keys()):
        print("Caching")
        return cache[unique_key]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(unique_key, params=params, headers=headers)
        cache[unique_key] = response.text
        save_cache(cache)
        return cache[unique_key]

CACHE_DICT = open_cache()
def search_yelp(term, location, sort_by = 'rating', limit = 50):
   baseurl = 'https://api.yelp.com/v3/businesses/search'
   params = {'term': term, 'location': location, 'sort_by':'rating', 'limit':limit} 
   response = requests.get(baseurl, params=params, headers={'Authorization': 'Bearer %s' % api_key}).json()
   make_request(baseurl, params=params, headers={'Authorization': 'Bearer %s' % api_key}, cache=CACHE_DICT)

   return response

def create_yelpfood():
   conn = sqlite3.connect('yelp.sqlite')
   cur = conn.cursor()
   create_yelp_food = '''
      CREATE TABLE IF NOT EXISTS "YELP" (
		"ID" INTEGER NOT NULL,
        "Name" TEXT NOT NULL, 
		"Category" TEXT NOT NULL,
        "Review" INTEGER NOT NULL, 
        "Rating" INTEGER NOT NULL)
	'''
   cur.execute(create_yelp_food)
   conn.commit()
   conn.close()

def create_yelpmap():
	conn = sqlite3.connect('yelp.sqlite')
	cur = conn.cursor()
	create_yelp_map = '''
	CREATE TABLE IF NOT EXISTS "MAP" (
		"ID" INTEGER NOT NULL,
		"Name" TEXT NOT NULL, 
		"Address" TEXT NOT NULL, 
		"City" TEXT NOT NULL, 
		"State" TEXT NOT NULL, 
		"Zipcode" INTEGER NOT NULL,
		"Phone" TEXT NOT NULL)
	'''
	cur.execute(create_yelp_map)
	conn.commit()
	conn.close()

def insert_database():
	insert_table = '''
		INSERT INTO YELP
		VALUES (?, ?, ?, ?, ?)
	'''
	conn = sqlite3.connect('yelp.sqlite')
	cur = conn.cursor()
	for business in place:
	   name = business['name']
	   ID = business['id'] 
	   category = business["categories"][0]['title']
	   review = business['review_count']
	   rating = business['rating']
	   cur.execute(insert_table,[ID, name, category, review, rating])
	conn.commit()
	conn.close()

def insert_map_database():
	insert_table = '''
		INSERT INTO MAP
		VALUES (?, ?, ?, ?, ?, ?, ?)
	'''
	conn = sqlite3.connect('yelp.sqlite')
	cur = conn.cursor()
	for location in maps:
		ID = location['id'] 
		name = location['name']
		address = location['location']['address1']
		city = location['location']['city']
		state = location['location']['state']
		zipcode = location['location']['zip_code']
		phone = location['phone']
		cur.execute(insert_table,[ID, name, address, city, state, zipcode, phone])
	conn.commit()
	conn.close()

##########graph################

def scatter_for_three(all_rating, all_rev, all_name):
   fig = plotly.graph_objects.Figure()
   fig.add_trace(plotly.graph_objects.Scatter(x=all_rating, y=all_rev, text=all_name)) 

   fig.update_layout(title="Rating vs Total Review Counts",
                     xaxis_title = "Ratings of the restaurant",
                     yaxis_title = "Total Review Counts for the restaurant")
   fig.show()

def bar_chart_rating(all_rating, all_name):
   fig = plotly.graph_objects.Figure([plotly.graph_objects.Bar(x=all_rating, y=all_name)])
   fig.update_layout(title="Ratings for the Restaurant",
                     xaxis_title = "Ratings",
                     yaxis_title = "The Restaurant")
   fig.show()

def bar_chart_rev(all_rev, all_name):
   fig = plotly.graph_objects.Figure([plotly.graph_objects.Bar(x=all_rev, y=all_name)])
   fig.update_layout(title="Total Review Counts for the Restaurant",
                     xaxis_title = "Total Review Counts",
                     yaxis_title = "The Restaurant")
   fig.show()

def scatter_for_two(all_rating, all_rev):
   fig = plotly.graph_objects.Figure()
   fig.add_trace(plotly.graph_objects.Scatter(x=all_rating, y=all_rev, text=all_name)) 

   fig.update_layout(title="Raing vs Total Review Counts",
                     xaxis_title = "Ratings")
   fig.show()

if __name__ == "__main__":
	create_yelpfood()
	create_yelpmap()
	while True:
		city1 = input("Please enter a city or 'exit':")
		city = city1.strip().lower()
		if city == 'exit':
			break
		cate1 = input('Please enter a food category, be as general as possible, or "restart":')
		cate = cate1.strip().lower()
		if cate == 'restart': 
			break
		else:
			print("------------------------------------------------------------------")
			print("Below is your search result. Thanks for using the program, enjoy.")
			print("------------------------------------------------------------------") 
			place = search_yelp(term=cate, location=city)['businesses']
			count = 1
			maps = search_yelp(term=cate, location=city)['businesses']
			count = 1
			all_name = []
			all_cate = []
			all_rev = []
			all_rating = [] 
			all_add = [] 
			all_phone = []
			for businesses in place:
				insert_database()
				try:
					name = businesses['name']
					all_name.append(name)
					category = businesses["categories"][0]['title']
					all_cate.append(all_cate)
					rev_count = businesses['review_count']
					all_rev.append(rev_count)
					rating = businesses['rating']
					all_rating.append(rating)
					address = (businesses['location']['address1'])
					all_add.append(address)
					phone = businesses['phone']
					all_phone.append(phone)
					city = (businesses['location']['city'])
					state = (businesses['location']['state'])
					zipcode = (businesses['location']['zip_code'])
					print(f'[{count}] {name}. {rating}/5. {category}. {rev_count} reviews. {address} {city} {state}, {zipcode}. {phone}')
					count +=1	
				except KeyError:
					print("The relevant data is not available.")
			for location in maps:
				insert_map_database()
		print("--------------------")
		print("Data Visualization:")
		print("--------------------") 
		print(f"[1] See bar chart comparison of ratings between different restaurants for your current search result.")
		print(f"[2] See scatter graph comparison of total review counts and ratings for your current search result.")
		print(f"[3] See bar chart comparison of of total review counts and ratings for your current search result.")
		print(f"[4] See bar chart comparison of total review counts between different restaurants for your current search result")
		
		number = input("Choose data presentation method by enter the number or 'exit':")
		if number == 'exit':
			break
		number = int(number)
		if number == 1: 
			print(bar_chart_rating(all_rating, all_name))
		if number== 2:
			print(scatter_for_three(all_rating, all_rev, all_name))
		if number == 3:
			print(scatter_for_two(all_rating, all_rev))
		if number == 4:
			print(bar_chart_rev(all_rev, all_name))
