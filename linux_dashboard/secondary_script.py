from flask import Flask, render_template,jsonify,request,redirect
from first import *
from netdiscofinal import *
import subprocess
app = Flask(__name__)

@app.route('/')
def first():
  return redirect("http://127.0.0.1:1234")


@app.route('/discover')
def find():
  a = discover()
  return jsonify(a)

@app.route('/poison_page', methods = ["GET", "POST"])
def poison_page():
  if request.method == "POST":
    output = request.form
    result = output["ipaddress"]
    return render_template('poison_page.html', title = "Poison", result = result)
  return render_template('poison_page.html', title="Poison Page")




@app.route('/index')
def index():
      user = {'username': 'Jich'}

      posts = [
{
  'author': {'username': 'John'},
    'body': 'Beautiful day in Portland!'
},
{
  'author': {'username': 'Susan'},
  'body': 'The Avengers movie was so cool!'
}
      ]
      return render_template('index.html', title='My Home', user=user, posts=posts)


if __name__ == "__main__":
  app.run(debug=True,host= '127.0.0.1', port = 5678)
