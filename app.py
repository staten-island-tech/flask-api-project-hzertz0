from flask import Flask, render_template
import requests
import urllib.parse

app = Flask(__name__)

def get_item_list():
    try:
        response = requests.get("https://raw.githubusercontent.com/anish-shanbhag/minecraft-api/master/data/items.json" )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching item list: {e}")
        return None

@app.route("/")
def index():
    items = get_item_list()
    if items is None:
        return "Error fetching item list"
    
    item_list = [{
        'name': item['name'],
        'image': item['image']
    } for item in items]

    return render_template("index.html", items=item_list)

@app.route("/item/<path:item_name>")
def item_detail(item_name):
    items = get_item_list()
    if items is None:
        return "Error fetching item list"
    
    # Decode URL encoding
    decoded_name = urllib.parse.unquote(item_name)

    # Case-insensitive match
    item = next((i for i in items if i['name'].lower() == decoded_name.lower()), None)
    if item is None:
        return f"No item found with name: {decoded_name}"

    return render_template("item_detail.html", item=item)

if __name__ == '__main__':
    app.run(debug=True)
"""from flask import Flask, render_template
import requests
import urllib.parse

app = Flask(__name__)

def get_item_list():
    try:
        response = requests.get("https://raw.githubusercontent.com/anish-shanbhag/minecraft-api/master/data/items.json")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching item list: {e}")
        return None

def get_recipes():
    try:
        response = requests.get("https://raw.githubusercontent.com/anish-shanbhag/minecraft-api/refs/heads/master/data/recipes.json")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching recipes: {e}")
        return None

@app.route("/")
def index():
    items = get_item_list()
    if items is None:
        return "Error fetching item list"
    
    item_list = [{
        'name': item['name'],
        'image': item['image']
    } for item in items]

    return render_template("index.html", items=item_list)

@app.route("/item/<path:item_name>")
def item_detail(item_name):
    items = get_item_list()
    recipes = get_recipes()
    if items is None or recipes is None:
        return "Error fetching data"

    # Decode URL encoding
    decoded_name = urllib.parse.unquote(item_name)

    # Case-insensitive match for item
    item = next((i for i in items if i['name'].lower() == decoded_name.lower()), None)
    if item is None:
        return f"No item found with name: {decoded_name}"

    # Find the recipe for the item
    recipe = next((r for r in recipes if r['item'].lower() == decoded_name.lower()), None)
    if recipe is None:
        recipe = {"recipe": [None, None, None, None, None, None, None, None, None]}  # No recipe

    return render_template("item_detail.html", item=item, recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)
"""