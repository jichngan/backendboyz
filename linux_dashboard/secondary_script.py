'''
This is the secondary server to run the Netdisco code as that code must be executed in Python3 
'''
from flask import Flask, render_template,jsonify,request,redirect
from netdiscofinal import *
from shutdown import *
import requests
import logging
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)



@app.route('/')
def first():
  return redirect("http://127.0.0.1:1234")


@app.route('/discover')
def find():
  a = discover()
  return jsonify(a)

@app.route('/logout', methods = ["GET"])
def logoff():
  shutdown_server()
  return 'Second server down'

if __name__ == "__main__":
  app.run(debug=True,host= '127.0.0.1', port = 5678)
