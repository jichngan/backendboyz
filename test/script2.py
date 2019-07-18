from flask import Flask, render_template,jsonify
from first import *
from netdiscofinal import *
app = Flask(__name__)

@app.route('/')
def first():
  name = hello()
  return "Welcome" + " " + name


@app.route('/discover')
def find():
  a = discover()
  return jsonify(a)



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
