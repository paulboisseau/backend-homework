from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

notes = [
    {"id": 1, "title": "Manger", "content": "Du curry et du riz", "done": False},
    {"id": 2, "title": "Envoyer l'email", "content": "Fondation", "done": True},
    {"id": 3, "title": "Sport", "content": "Courir très vite", "done": False},
]

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
            return jsonify(ok=True)

    return jsonify(ok=False, status="not_found"), 404

if __name__ == "__main__":
    app.run(debug=True)
