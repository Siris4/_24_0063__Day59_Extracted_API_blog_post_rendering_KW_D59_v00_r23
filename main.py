from flask import Flask, render_template, jsonify
import datetime as dt
import requests

app = Flask(__name__)

MY_NAME = 'Gavin "Siris" Martin'  # defined globally for reuse in routes and/or functions

@app.route('/')
@app.route('/home')
def home():
    blog_url = "https://api.npoint.io/674f5423f73deab1e9a7"
    try:
        blog_response = requests.get(blog_url)
        blog_response.raise_for_status()  # Ensures we proceed only if the response was successful
        all_posts = blog_response.json()
        # adds the author and date to each post (since the JSON data is missing author and date metadata sections):
        for post in all_posts:
            post['author'] = "Dr. Angela Yu"
            post['date'] = dt.datetime.now().strftime("%B %d, %Y")  # uses today's date for the Blog post date
    except requests.RequestException as e:
        return jsonify({"error": "Unable to fetch blog posts", "details": str(e)}), 500
    return render_template("index.html", posts=all_posts, CURRENT_YEAR=dt.datetime.now().year)

@app.route('/about')
def about():
    return render_template('about.html', CURRENT_YEAR=dt.datetime.now().year)

@app.route('/contact')
def contact():
    return render_template('contact.html', CURRENT_YEAR=dt.datetime.now().year)

if __name__ == "__main__":
    app.run(debug=True)
