from flask import Flask, render_template, request, jsonify
import requests
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

BREEDS = ["bulldog", "labrador", "poodle", "beagle", "retriever"]


def get_db():
    return psycopg2.connect(DATABASE_URL)


def setup_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_images (
            id SERIAL PRIMARY KEY,
            breed TEXT,
            image_url TEXT,
            saved_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html", breeds=BREEDS)


@app.route("/api/dog/<breed>")
def get_dog(breed):
    if breed not in BREEDS:
        return jsonify({"status": "error", "message": "Invalid breed"}), 400
    try:
        response = requests.get(
            f"https://dog.ceo/api/breed/{breed}/images/random", timeout=5
        )
        data = response.json()
        return jsonify({"status": "ok", "breed": breed, "image_url": data["message"]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 502


@app.route("/api/save", methods=["POST"])
def save_image():
    data = request.get_json()
    breed = data.get("breed")
    image_url = data.get("image_url")
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO saved_images (breed, image_url) VALUES (%s, %s)",
            (breed, image_url)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/saved")
def get_saved():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT breed, image_url, saved_at FROM saved_images ORDER BY saved_at DESC LIMIT 10"
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"images": [
            {"breed": r[0], "image_url": r[1], "saved_at": str(r[2])} for r in rows
        ]})
    except Exception as e:
        return jsonify({"images": [], "error": str(e)})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/status")
def status():
    try:
        conn = get_db()
        conn.close()
        db = {"ok": True, "message": "Connected"}
    except Exception as e:
        db = {"ok": False, "message": str(e)}
    try:
        r = requests.get("https://dog.ceo/api/breeds/list/all", timeout=3)
        api = {"ok": r.status_code == 200, "message": "Reachable"}
    except Exception:
        api = {"ok": False, "message": "Unreachable"}
    return jsonify({"database": db, "dog_api": api})


if __name__ == "__main__":
    setup_db()
    app.run(debug=True)