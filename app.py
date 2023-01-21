from flask import Flask, render_template

import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# function to run web scrapping 
def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=60)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())



# routes are controlled by functions, routes are called decorators and create paths 
@app.route("/")
def index():
# this allows the page index.html to be rendered when route is accessed, html pages MUST be inside TEMPLATE folders
    # return "page"
    return render_template("index.html")