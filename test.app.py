from flask import Flask, request, make_response

app = Flask(__name__)
@app.route('/')
def hello_world():
    resp = make_response('Hello world')
    resp.set_cookie('nom du cookie', 'valeur du cookie')
    return resp

if __name__ == '__main__':
    app.run()