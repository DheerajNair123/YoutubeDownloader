from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Linux-safe temporary directory
DOWNLOAD_FOLDER = "/tmp/downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>YouTube Downloader</title>
<style>
body {
    margin: 0;
    height: 100vh;
    background: linear-gradient(135deg, #ff9a9e, #fad0c4);
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: system-ui, sans-serif;
}
.card {
    background: white;
    padding: 24px;
    border-radius: 12px;
    width: 400px;
    box-shadow: 0 20px 40px rgba(0,0,0,.25);
}
input, select, button {
    width: 100%;
    padding: 12px;
    margin-top: 10px;
}
button {
    background: #ff4081;
    color: white;
    border: none;
    cursor: pointer;
}
#message {
    margin-top: 12px;
    font-weight: bold;
}
</style>
</head>
<body>
<div class="card">
<h2>YouTube Downloader</h2>
<form id="downloadForm">
<input id="url" placeholder="YouTube URL" required>
<select id="choice">
<option value="1">MP4 Video</option>
<option value="2">MP3 Audio</option>
</select>
<button>Download</button>
</form>
<div id="message"></div>
</div>

<script>
document.getElementById("downloadForm").addEventListener("submit", async e => {
    e.preventDefault();
    const message = document.getElementById("message");
    message.textContent = "Downloading...";
    const data = new FormData();
    data.append("url", document.getElementById("url").value);
    data.append("choice", document.getElementById("choice").value);

    const res = await fetch("/download", { method: "POST", body: data });
    const json = await res.json();

    if (json.status === "done") {
        message.textContent = "✅ " + json.message;
    } else {
        message.textContent = "❌ " + json.error;
    }
});
</script>
</body>
</html>
'''

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    choice = request.form.get("choice")

    if not url:
        return jsonify({"status": "failed", "error": "URL missing"})

    output_template = f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s"

    cmd = [
        "yt-dlp",
        "--no-warnings",
        "-o", output_template
    ]

    if choice == "2":
        cmd += ["-x", "--audio-format", "mp3"]

    cmd.append(url)

    try:
        subprocess.run(cmd, check=True)
        return jsonify({"status": "done", "message": "Download completed"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "failed", "error": "Download failed"})
