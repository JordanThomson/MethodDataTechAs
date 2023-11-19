# This is the backend

from flask import Blueprint, render_template, request, flash
import requests
import json
import os

views = Blueprint('views', __name__)

# Home page
@views.route('/')
def home():
    return render_template("home.html")

#Character page
@views.route('/characters', methods=['GET', 'POST'])
def characters():
    char_info1 = None
    char_info2 = None
    if request.method == 'POST':
        charName1 = request.form.get('characterName1')
        charName2 = request.form.get('characterName2')
        char_info1 = get_person_info(charName1)
        char_info2 = get_person_info(charName2)
    return render_template("characters.html", char_info1=char_info1, char_info2=char_info2)


def get_person_info(name):
    baseurl = 'https://swapi.dev/api/'
    endpoint = 'people/'
    cache_file = 'cache.txt'
    
    # Check if the cache file exists
    if os.path.exists(cache_file):
        # Load the cache
        with open(cache_file, 'r') as f:
            cache = json.load(f)
    else:
        # Initialize an empty cache
        cache = {}
    
    # Check if the person is in the cache
    if name in cache:
        return cache[name]
    
    # Construct the URL for the person search
    search_url = f'{baseurl}{endpoint}?search={name}'
    
    try:
        # Send a GET request to the API to search for the person
        response = requests.get(search_url)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Check if any results were found
        if data['count'] == 0:
            return None  # Return None if no person found
        else:
            # Get the URL of the first result
            person_url = data['results'][0]['url']
            
            # Send a GET request to the person's URL
            person_response = requests.get(person_url)
            person_response.raise_for_status()
            person_data = person_response.json()
            
            # Fetch film titles using a list comprehension
            films = []
            for film_url in person_data['films']:
                film_response = requests.get(film_url)
                film_data = film_response.json()
                films.append(film_data['title'])
            
            # Fetch homeworld name
            homeworld_url = person_data['homeworld']
            homeworld_response = requests.get(homeworld_url)
            homeworld_data = homeworld_response.json()
            homeworld_name = homeworld_data['name']
            
            # Return the person's information
            person_info = {
                'name': person_data['name'],
                'birth_year': person_data['birth_year'],
                'eye_color': person_data['eye_color'],
                'gender': person_data['gender'],
                'hair_color': person_data['hair_color'],
                'height': int(person_data['height']) if person_data['height'] != 'unknown' else -1,
                'mass': int(person_data['mass']) if person_data['mass'] != 'unknown' else -1,
                'skin_color': person_data['skin_color'],
                'homeworld': homeworld_name,
                'films': films
            }
            
            # Add the person to the cache and save it
            cache[name] = person_info
            with open(cache_file, 'w') as f:
                json.dump(cache, f)
            
            return person_info
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None  # Return None in case of an error
