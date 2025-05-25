from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

QUEUE_FILE = "/opt/fancaps/queue.txt"
ARCHIVE_FILE = "/opt/fancaps/archive.txt"

def read_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def write_lines(path, lines):
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "add_url" in request.form:
            url = request.form.get("url", "").strip()
            if url:
                with open(QUEUE_FILE, "a") as f:
                    f.write(url + "\n")
        elif "delete_url" in request.form:
            url_to_delete = request.form.get("delete_url", "").strip()
            queue = read_lines(QUEUE_FILE)
            queue = [url for url in queue if url != url_to_delete]
            write_lines(QUEUE_FILE, queue)
        return redirect(url_for("index"))

    queue = read_lines(QUEUE_FILE)
    archive = read_lines(ARCHIVE_FILE)
    return render_template("index.html", queue=queue, archive=archive)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5080)
