from flask import Flask, render_template, jsonify, request, Response
import time
import threading
import queue
import json

app = Flask(__name__)

notes = [
    {"id": 1, "title": "Manger", "content": "Du curry et du riz", "done": False},
    {"id": 2, "title": "Envoyer l'email", "content": "Fondation Mines Paris", "done": True},
    {"id": 3, "title": "Sport", "content": "Courir très vite", "done": False},
]

subscriptions = []

@app.route("/events")
def events():
    def stream():
        q = queue.Queue()
        subscriptions.append(q)
        try:
            while True:
                data = q.get()
                yield f"data: {data}\n\n"
        except GeneratorExit:
            subscriptions.remove(q)

    return Response(stream(), mimetype="text/event-stream")


@app.route("/")
def index():
    return render_template("notes.html.j2", notes=notes)

@app.route("/api/notes/<int:note_id>/done", methods=["POST"])
def mark_done(note_id):
    data = request.get_json()
    if not data or "done" not in data:
        return jsonify(ok=False, status="invalid_payload"), 400

    for note in notes:
        if note["id"] == note_id:
            note["done"] = data["done"]
            for sub in subscriptions:
                sub.put(json.dumps({"type": "update", "id": note_id, "done": data["done"]}))
            return jsonify(ok=True)

    return jsonify(ok=False, status="not_found"), 404

@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    if not data or "title" not in data or "content" not in data:
        return jsonify(ok=False, status="invalid_payload"), 400
    note_id = max(note["id"] for note in notes) + 1 if notes else 1
    new_note = {
        "id": note_id,
        "title": data["title"],
        "content": data["content"],
        "done": False
    }
    notes.append(new_note)
    for sub in subscriptions:
        sub.put(json.dumps({"type": "new", "note": new_note}))
    return jsonify(ok=True, note=new_note), 201


if __name__ == "__main__":
    app.run(debug=True, port=5001)