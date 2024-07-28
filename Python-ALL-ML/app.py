from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to scrape data from VSU website
def scrape_vsu_website():
    url = 'https://www.infyz.com/'
    response = requests.get(url)
    if response.status_code != 200:
        return None, []
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract paragraphs
    paragraphs = soup.find_all('p')
    content = ' '.join([p.get_text() for p in paragraphs])
    
    # Extract image URLs
    images = []
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            # Handle relative URLs
            if img_url.startswith('/'):
                img_url = url + img_url
            images.append(img_url)
    
    return content, images

# Load the scraped data
data, images = scrape_vsu_website()

# Simple search function
def search_data(query):
    if not data:
        return "No data available.", []
    if query.lower() in data.lower():
        start_idx = data.lower().find(query.lower())
        end_idx = start_idx + 500  # Extract some surrounding text
        return data[start_idx:end_idx] + "...", images
    return "No relevant information found.", []

@app.route('/', methods=['GET', 'POST'])
def index():
    response = ""
    found_images = []
    lower_name = ""
    upper_name = ""
    if request.method == 'POST':
        query = request.form.get('query')
        response, found_images = search_data(query)
        lower_name = query.lower()
        upper_name = query.upper()
    return render_template('index.html', response=response, images=found_images, lower_name=lower_name, upper_name=upper_name)

if __name__ == '__main__':
    app.run(debug=True)
