from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Load the item list once globally
ITEM_LIST_URL = "https://raw.githubusercontent.com/anish-shanbhag/minecraft-api/master/data/items.json"

@app.route("/")
def index():
    item_list = []
    for item in item_list:
        item_list.append({
            'name': item['name'],
            'image': item['image'],
            'id': item.get('namespacedId', item['name'])  # Use a fallback if namespacedId is missing
        })
    return render_template("index.html", item_list=item)

if __name__ == '__main__':
    app.run(debug=True)

