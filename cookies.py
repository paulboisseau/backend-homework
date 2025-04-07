from flask import Flask, request, make_response
app = Flask(__name__)

@app.route('/')
def hello_world():
    resp = make_response('Hello world')
    resp.set_cookie('nom du cookie', 'valeur du cookie')
    return resp

@app.route('/double/<int:num>')
def double(num):
    return str(2 * int(num))

# @app.route('/double/<num>')
# def double(num):
#     return {'ans': str(2 * num)}, 404, {'Content-Type': 'text/plain'}

click_counts = {}
last_session_id = 0

@app.route('/click-count')
def click_count():
    session_id = request.cookies.get('sessionId')
    if session_id :
        if session_id in click_counts:
            click_counts[session_id] += 1
            return str(click_counts.get(session_id))+ " click(s) for " + session_id
        else:
            click_counts[session_id] = 0
            return str(0) + " click(s) for " + session_id
    else:
        global last_session_id
        last_session_id += 1
        click_counts[str(last_session_id)] = 0
        resp = make_response(str(0) + " click(s) for " + str(last_session_id))
        resp.set_cookie('sessionId', str(last_session_id))
        return resp 




if __name__ == '__main__':
    app.run()


