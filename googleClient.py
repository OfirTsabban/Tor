from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        search_text = request.form['search_text']
        data = {'googleText': search_text}
        headers = {'Content-Type': 'application/json'}
        response = requests.post("http://10.0.0.15:8000/search", json=data, headers=headers)
        if response.status_code == 200:
            return "Received search text: " + search_text
        else:
            return "Error processing the request. Status code: " + str(response.status_code)
    except Exception as e:
        return "An error occurred: " + str(e)

if __name__ == '__main__':
    app.run(port=9000, host="0.0.0.0", debug=False, use_reloader=False)
