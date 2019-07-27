from flask import Flask, render_template,jsonify,url_for,redirect,request
from scanning import *
from image_info import *
from  shutdown import *
import subprocess
import json
import requests
import os 
import logging
import webbrowser

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/')
def index():
  return render_template('index.html', title = "Home")

@app.route('/start_scan')
def start_scan():
  devices = scan()
  return render_template('scan.html', title = "Scanning", devices = devices)


@app.route('/scan_page')
def scan_page():
  SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
  json_url = os.path.join(SITE_ROOT, 'scan.json')
  scan_data = json.load(open(json_url))
  return render_template('scan_page.html', title = "All Devices",scan_data = scan_data)


@app.route('/discover_page')
def discover_page():
  SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
  json_url = os.path.join(SITE_ROOT, 'discover.json')
  scan_data = json.load(open(json_url))
  return render_template('discover_page.html', title = "IOT Devices", scan_data = scan_data) 

@app.route('/start_discover')
def start_discover():
  r = requests.get("http://127.0.0.1:5678/discover")
  names = r.json()
  return render_template('discover.html', title = "IOT Discovery", names = names)
  

@app.route('/view_scan')
def view_scan():
  subprocess.call(["python", "save_picf.py"])
  image_size = image_info()
  height = image_size["Height"]
  width = image_size["Width"]
  return render_template('plot_graph.html', name = "New Plot", url = "static/images/new_plot.png", height=height, width=width)

@app.route('/about')
def about():
  return render_template('about.html', name = "About")

@app.route('/network_scan')
def network_scan():
  return render_template('traffic.html', name = "Traffic")

@app.route('/logoff', methods=['GET'])
def logoff():
    requests.get("http://127.0.0.1:5678/logout")
    shutdown_server()
    return render_template('logoff.html', name = "Logoff")


if __name__ == "__main__":
  url = 'http://127.0.0.1:1234'
  webbrowser.open_new(url)
  app.run(host = '127.0.0.1', port = 1234)
  #app.run(debug=True,host= '127.0.0.1', port = 1234)



