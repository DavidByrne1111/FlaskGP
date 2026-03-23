from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def hello_bud():
    api_url = 'https://dog.ceo/api/breeds/image/random'
    response = requests.get(api_url)
    data = response.json()

    return f'<img src="{data["message"]}" width="400">'

if __name__ == '__main__':
    app.run(debug=True)
