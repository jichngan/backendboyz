from flask import Flask, render_template,jsonify,url_for,redirect,request
from scanning import *
from first import *
from image_info import *
from poison_form import SubmissionForm
import subprocess
import json
import requests
import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfe280ba245'

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

@app.route('/view_scan')
def view_scan():
  subprocess.call(["python", "save_picf.py"])
  image_size = image_info()
  height = image_size["Height"]
  width = image_size["Width"]
  return render_template('plot.html', name = "New Plot", url = "/static/images/new_plot.png", height=height, width=width)


@app.route('/form', methods=["POST"])
def my_form():
  text = request.form['text']
  return text
'''
@app.route('/form', methods=["POST"])
def my_form_post():
  text = request.form['text']
  child = subprocess.Popen(['python', 'plotpoisontest.py'], stdin=subprocess.PIPE)
  try:
    child.communicate(text)
  except KeyboardInterrupt:
    child.terminate()
  return "test"
'''

@app.route('/submit', methods = ['GET', 'POST'])
def submit():
 #Add subprocess to call new server script
  form = SubmissionForm()
  return render_template('submission.html', title = "Poison", form = form)

@app.route('/about',methods = ["GET", "POST"])
def about():
  if request.method == "POST":
    output = request.form 
    result = output["ipaddress"]
    return render_template('about1.html', title = "Show IP", result = result)
  return render_template('about.html',title = "About",  blog_posts=blog_posts)


if __name__ == "__main__":
  app.run(debug=True,host= '127.0.0.1', port = 1234)



