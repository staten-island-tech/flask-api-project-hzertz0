from flask import Flask, render_template
import requests
import urllib.parse

app = Flask(__name__)

# Fetch item list
def get_item_list():
    try:
        response = requests.get("https://raw.githubusercontent.com/anish-shanbhag/minecraft-api/master/data/items.json")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching item list: {e}")
        return None

# Fetch recipe list
def get_recipe_list():
    try:
        response = requests.get("https://raw.githubusercontent.com/anish-shanbhag/minecraft-api/master/data/recipes.json")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching recipe list: {e}")
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
    recipes = get_recipe_list()

    if items is None or recipes is None:
        return "Error fetching data"

    decoded_name = urllib.parse.unquote(item_name)
    item = next((i for i in items if i['name'].lower() == decoded_name.lower()), None)
    if item is None:
        return f"No item found with name: {decoded_name}"

    # Collect all recipes for this item
    item_recipes = [r for r in recipes if r['item'].lower() == item['name'].lower()]

    # Prepare recipe grids for all recipes
    recipe_grids = []
    for recipe in item_recipes:
        recipe_grid = []
        
        # Handle Shaped Recipes
        if recipe and not recipe.get('shapeless', False):
            for name in recipe['recipe']:
                if name is None:
                    recipe_grid.append(None)
                else:
                    matched = next((i for i in items if i['name'].lower() == name.lower()), None)
                    if matched:
                        recipe_grid.append({
                            'name': matched['name'],
                            'image': matched['image']
                        })
                    else:
                        recipe_grid.append({'name': name, 'image': None})

        # Handle Shapeless Recipes
        elif recipe and recipe.get('shapeless', False):
            for name in recipe['recipe']:
                if name is None:
                    recipe_grid.append(None)
                else:
                    matched = next((i for i in items if i['name'].lower() == name.lower()), None)
                    if matched:
                        recipe_grid.append({
                            'name': matched['name'],
                            'image': matched['image']
                        })
                    else:
                        recipe_grid.append({'name': name, 'image': None})

        recipe_grids.append(recipe_grid)

    return render_template("item_detail.html", item=item, recipe_grids=recipe_grids)



if __name__ == '__main__':
    app.run(debug=True)
