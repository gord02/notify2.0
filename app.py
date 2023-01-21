from flask import Flask, render_template

app = Flask(__name__)


# routes are controlled by functions, routes are called decorators and create paths 
@app.route("/")
def index():
# this allows the page index.html to be rendered when route is accessed, html pages MUST be inside TEMPLATE folders
    # return "page"
    return render_template("index.html")