from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    # Get Minecraft blocks from the API
    response = requests.get("https://raw.githubusercontent.com/anish-shanbhag/minecraft-api/master/data/items.json")
    item_list = response.json()  # This is already a list of block dicts

    items = []
    for item in item_list:
        items.append({
            'name': item['name'],
            'image': item['image']
        })

    # Pass the blocks to your index.html template
    return render_template("index.html", items=items)

if __name__ == '__main__':
    app.run(debug=True)
