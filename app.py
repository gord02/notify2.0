from flask import Flask, render_template

import time
import atexit
import logging
from apscheduler.schedulers.background import BackgroundScheduler


from logic import notify

app = Flask(__name__)
app.debug = True

# function to run web scrapping 
def print_date_time():
    app.logger.info(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    # print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    
# logging.debug('This is a debug message')


scheduler = BackgroundScheduler()
# scheduler.add_job(func=notify.test_email, trigger="interval", minutes=2)
scheduler.add_job(func=print_date_time, trigger="interval", minutes=2)
# scheduler.add_job(func=notify.test_email, trigger="interval", seconds=60*60*24)
# scheduler.add_job(func=print_date_time, trigger="interval", seconds=60)
scheduler.start()

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())



# routes are controlled by functions, routes are called decorators and create paths 
@app.route("/")
def index():
# this allows the page index.html to be rendered when route is accessed, html pages MUST be inside TEMPLATE folders
    # return "page"
    logging.info("Hrllo")
    app.logger.debug("Debug log level")
    app.logger.info("Program running correctly")
    app.logger.warning("Warning; low disk space!")
    app.logger.error("Error!")
    app.logger.critical("Program halt!")
    return render_template("index.html")

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)