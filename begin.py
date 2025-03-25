from flask import Flask
from flask import render_template
from flask import request


app = Flask("Appli de ouf")


@app.route("/une/route/donnee")
def handler():
  name = request.args.get("name")
  age = request.args.get("age")
  return f"<h1> Hello {name} ! Tu as vraiment {age} ans ? </h1>"

