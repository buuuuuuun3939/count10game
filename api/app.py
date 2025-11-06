from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os


app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL is not set!")
print("Connecting to DB:", db_url)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    diff_ms = db.Column(db.Float)

with app.app_context():
    db.create_all()

@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.json
    name = data.get("name")
    diff = data.get("diff_ms")
    s = Score(name=name, diff_ms=diff)
    db.session.add(s)
    db.session.commit()
    return jsonify({"status": "ok"})

@app.route("/api/top10")
def top10():
    scores = Score.query.order_by(Score.diff_ms.asc()).limit(10).all()
    return jsonify([
        {"name": s.name, "diff_ms": s.diff_ms} for s in scores
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
