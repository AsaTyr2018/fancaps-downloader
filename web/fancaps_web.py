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
            alt = "alt_scraper" in request.form
            if url:
                entry = f"ALT|{url}" if alt else url
                with open(QUEUE_FILE, "a") as f:
                    f.write(entry + "\n")
        elif "delete_url" in request.form:
            url_to_delete = request.form.get("delete_url", "").strip()
            queue = read_lines(QUEUE_FILE)
            queue = [url for url in queue if url != url_to_delete]
            write_lines(QUEUE_FILE, queue)
        return redirect(url_for("index"))

    queue = read_lines(QUEUE_FILE)
    archive = read_lines(ARCHIVE_FILE)
    return render_template("index.html", queue=queue, archive=archive)

@app.route("/log")
def view_log():
    log_path = "/var/log/fancaps-daemon.log"
    if not os.path.exists(log_path):
        return "Log file not found."

    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()[-200:]  # Tail-like behavior
        return "<br>".join(line.strip() for line in lines)
    except Exception as e:
        return f"Error reading log: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5080)
