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

@app.route('/')
def first():
  return redirect("http://127.0.0.1:1234")

pid = 0
child = subprocess.Popen(['python', 'plotpoisontest.py'], stdin=subprocess.PIPE)
 
@app.route('/poison', methods = ["GET", "POST"])
def poison():
#  child = subprocess.Popen(['python', 'plotpoisontest.py'], stdin=subprocess.PIPE)
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
  #os.kill(pid,signal.SIGINT)
  #os.kill(pid, signal.SIGHUP)
  return redirect("http://127.0.0.1:1234")


@app.route('/reload')
def reload():
  global to_reload
  to_reload = True
  return "reloaded"




if __name__ == "__main__":
  app.run(debug=True,host= '127.0.0.1', port = 9999)



