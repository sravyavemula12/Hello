import string
import random
import json
import os
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)
url_mapping_file = 'url_mappings.json'

# Load or initialize the URL mappings
if os.path.exists(url_mapping_file):
    with open(url_mapping_file, 'r') as file:
        url_mappings = json.load(file)
else:
    url_mappings = {}

def save_mappings():
    with open(url_mapping_file, 'w') as file:
        json.dump(url_mappings, file)

def generate_short_url():
    chars = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choice(chars) for _ in range(6))
        if short_url not in url_mappings:
            return short_url

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('long_url')
    if not long_url:
        return jsonify({"error": "Missing 'long_url' parameter"}), 400

    short_url = generate_short_url()
    url_mappings[short_url] = long_url
    save_mappings()
    
    return jsonify({"short_url": short_url})

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = url_mappings.get(short_url)
    if not long_url:
        return jsonify({"error": "URL not found"}), 404
    
    return redirect(long_url)

@app.route('/mappings', methods=['GET'])
def get_mappings():
    return jsonify(url_mappings)

if __name__ == "__main__":
    app.run(debug=True)
