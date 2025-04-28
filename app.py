from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Load the item list once globally
ITEM_LIST_URL = "https://raw.githubusercontent.com/anish-shanbhag/minecraft-api/master/data/items.json"

def fetch_items():
    response = requests.get(ITEM_LIST_URL)
    return response.json()

@app.route("/")
def index():
    item_list = fetch_items()
    items = []
    for item in item_list:
        items.append({
            'name': item['name'],
            'image': item['image'],
            'id': item.get('namespacedId', item['name'])  # Use a fallback if namespacedId is missing
        })
    return render_template("index.html", items=items)

@app.route("/details/<item_id>")
def item_detail(item_id):
    item_list = fetch_items()
    item = next((i for i in item_list if i.get('namespacedId', i['name']) == item_id), None)
    if item is None:
        return "Item not found", 404
    return render_template("details.html", item=item)

if __name__ == '__main__':
    app.run(debug=True)

