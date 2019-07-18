from flask import Flask, render_template,jsonify,url_for,redirect
from first import *
from scanning import *
import subprocess
import json
import requests
import os 

app = Flask(__name__)

#Test Posts

blog_posts = [
  {
    'author': 'Jich',
    'title': 'Blog Post 1',
    'content': 'Jich\'s first post',
    'date_posted': '4 July 2019'
  },
  {
    'author': 'John',
    'title': 'Blog Post 2',
    'content': 'John\'s first post',
    'date_posted': '5 July 2019'
  }
]


@app.route('/')
def first():
  name = hello()

  return render_template('index.html', title = "Home", name = name)


@app.route('/start_scan')
def start_scan():
  devices = scan()
  r = requests.get("http://127.0.0.1:5678/discover")
  names = r.json()
  return render_template('scan.html', title = "Scanning", devices = devices,names = names)


@app.route('/scan_page')
def scan_page():
  SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
  json_url = os.path.join(SITE_ROOT, 'scan.json')
  scan_data = json.load(open(json_url))
  return render_template('scan_page.html', title = "Scan",scan_data = scan_data)

@app.route('/discover')
def discover():
  r = requests.get("http://127.0.0.1:5678/discover")
  names = r.json()
  return render_template('discover.html', title = "Discover", names = names)
  #return redirect("http://127.0.0.1:5678/discover")


@app.route('/about')
def about():
  return render_template('about.html',title = "About",  blog_posts=blog_posts)


if __name__ == "__main__":
  app.run(debug=True,host= '127.0.0.1', port = 1234)



