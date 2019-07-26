from flask import Flask, render_template,jsonify,url_for,redirect,request
from scanning import *
from first import *
from image_info import *
from poison_form import SubmissionForm
import subprocess
import json
import requests
import os
import signal


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfe280ba245'

to_reload = False

pid = 0
child = subprocess.Popen(['python', 'plotpoisontest.py'], stdin=subprocess.PIPE)
def get_app():
  @app.route('/')
  def first():
     name = hello()

     return render_template('index.html', title = "Home", name = name)


  @app.route('/poison', methods = ["GET", "POST"])
  def poison():
    global pid 
    global child
    pid = child.pid
    try:
      child.communicate('192.168.0.168')
    except KeyboardInterrupt:
        child.terminate()
  return "test"


  @app.route('/cut_poison')
  def cut_poison():
    global pid
    global child
    child.terminate()
    return "Hi"


  @app.route('/reload')
  def reload():
    global to_reload
    to_reload = True
    return "reloaded"

  return app

class AppReloader(object):
  def __init__(self, create_app):
    self.create_app = create_app
    self.app = create_app()

  def get_application(self):
    global to_reload
    if to_reload:
      self.app = self.create_app()
      to_reload = False

    return self.app

    def __call__(self, environ, start_response):
      app = self.get_application()
      return app(environ, start_response)


# This application object can be used in any WSGI server
# for example in gunicorn, you can run "gunicorn app"
application = AppReloader(get_app)


if __name__ == "__main__":
  app.run(host= '127.0.0.1', port = 9999, use_reloader=True,use_debugger=True,use_evalex=True)



