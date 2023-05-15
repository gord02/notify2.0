from flask import Flask, render_template, redirect
from flask import request

from apscheduler.schedulers.background import BackgroundScheduler

import time
import atexit
import logging

import appLogic
from logic import notify 
import main

app = Flask(__name__)
app.debug = True

# function to run web scrapping 
# def print_date_time():
    # app.logger.info(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    # print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

scheduler = BackgroundScheduler()
scheduler.add_job(func=main.check_on, trigger="interval", minutes=5)
# scheduler.add_job(func=notify.test_email, trigger="interval", minutes=5)
# scheduler.add_job(func=print_date_time, trigger="interval", minutes=5)
# scheduler.add_job(func=notify.test_email, trigger="interval", seconds=60*60*24)
# scheduler.add_job(func=print_date_time, trigger="interval", seconds=60)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST": 
        formType = request.form['type']
        email = request.form['email']
        
        if(formType == "contactForm"):
            msg = request.form['message']
            name = request.form['name']
            notify.contact(email,name, msg)
            return redirect("/")
        
        # subscribing
        else:  
            # pref = [0,0,0]  
            pref = 0 
            for x in request.form:
                if(x == "swe"):
                    pref += 1
                if(x == "ml"):
                    pref += 2
                if(x == "pm"):
                    pref += 4
            
            appLogic.join(email, pref)
            # appLogic.confirm(email, type)
            return redirect("/#subscribe")

    return render_template("index.html")


# @app.route("/join" , methods = ["GET", "POST"])

# @app.route("/update" , methods = ["GET", "POST"])
# def index():
# # this allows the page index.html to be rendered when route is accessed, html pages MUST be inside TEMPLATE folders
#     if request.method == 'GET':
#         # return render_template("update.html")
#         pass
   
#     if request.method == 'POST':
#         # call to update function 
#         email = request.form['email']
#         type = request.form['type']
#         appLogic.confirm(email, type)
#         return redirect("/")


# catch all 
@app.route("/", defaults={'u_path': ""})
@app.route("/<path:u_path>")
def catch_all(u_path):
    return render_template("catchAll.html")

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    
    
# # Test:
# # retrieval of of data to various routes 