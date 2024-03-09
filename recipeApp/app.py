from flask import Flask, request, render_template
import requests
from urllib.parse import unquote

# To create the flask app
app = Flask(__name__)

# To replace with spoonacular api key
API_KEY = '77d93c6c6f294367abd2f2045aa89530'

# To define the route for "Home" button
@app.route('/home', methods=['GET'])
def home():
    # Renders the main page with a search query and empty recipe list
    return render_template('index.html', recipes=[], search_query='')

#define the main route for the app
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If a form is submitted
        query= request.form.get('search_query', '')
        # Perform a search for reipes with the given query
        recipes = search_recipes(query)
        # Render the main page with the search results and the search query
        return render_template('index.html', recipes=recipes, search_query=query)
    
    # else, if it's a GET request or no form has been submitted
    search_query = request.args.get('search_query', '')
    decoded_search_query = unquote(search_query)
    # Perform a search for recipes with decoded search query
    recipes = search_recipes(decoded_search_query)
    # Render the main page
    return render_template('index.html', recipes=recipes, search_query=decoded_search_query)

# Function to search for recipes based on the provided query
def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,           
    }

    # Send a GET reust to the spoonacular API with the query params
    response = requests.get(url, params=params)
    # if the API call is successful
    if response.status_code == 200:
        # Parse the API response as JSON data
        data = response.json()
        # Return the list of recipe results
        return data['results']
    #if API call is not successful
    return []
    
# Route to view a specific recipe with a given recipe ID
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    #Get the search query from the URL query parameters
    search_query = request.args.get('search_query', '')
    # Build the url to get information about the specific recipemID from the website
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': API_KEY,
    }

    # Send a GET request to the spoonacular API to get the recipe information
    response = requests.get(url, params=params)
    # If the API call is successful
    if response.status_code == 200:
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query=search_query)
    return "Recipe not found", 404

# Run the app in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)
     
