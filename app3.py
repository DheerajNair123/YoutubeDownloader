from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

DOWNLOAD_FOLDER = r"C:\Users\dheer\Downloads\DownloadedYT\newsongs"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>YouTube Downloader</title>

    <style>
        * {
            box-sizing: border-box;
            font-family: "Segoe UI", system-ui, sans-serif;
        }

        body {
            margin: 0;
            height: 100vh;
            background: radial-gradient(circle at top, #ffb6b6, #f06292);
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .card {
            width: 420px;
            padding: 28px;
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(14px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.25);
            color: #2b2b2b;
        }

        h2 {
            text-align: center;
            margin-bottom: 18px;
            font-weight: 700;
        }

        input, select, button {
            width: 100%;
            padding: 12px;
            margin-top: 12px;
            border-radius: 10px;
            border: none;
            outline: none;
            font-size: 15px;
        }

        input, select {
            background: rgba(255,255,255,0.9);
        }

        button {
            background: linear-gradient(135deg, #ff4081, #ff6f61);
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }

        #message {
            margin-top: 18px;
            text-align: center;
            font-weight: 600;
        }

        footer {
            text-align: center;
            margin-top: 14px;
            font-size: 12px;
            opacity: 0.75;
        }
    </style>
</head>

<body>
    <div class="card">
        <h2>🎵 YouTube Downloader</h2>

        <form id="downloadForm">
            <input 
                type="text" 
                id="url" 
                placeholder="Paste YouTube video URL here"
                required
            >

            <select id="choice">
                <option value="1">Download MP4 (Video)</option>
                <option value="2">Download MP3 (Audio)</option>
            </select>

            <button type="submit">Start Download</button>
        </form>

        <div id="message"></div>

        <footer>
            Created with ❤️ by Dheeraj Nair
        </footer>
    </div>

<script>
    document.getElementById('downloadForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const url = document.getElementById('url').value;
        const choice = document.getElementById('choice').value;
        const message = document.getElementById('message');

        message.textContent = "Downloading... please wait ⏳";
        message.style.color = "#1e3a8a";

        const formData = new FormData();
        formData.append("url", url);
        formData.append("choice", choice);

        try {
            const response = await fetch("/download", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (result.status.includes("done")) {
                message.textContent = "✅ " + result.message;
                message.style.color = "green";
            } else {
                message.textContent = "❌ " + result.error;
                message.style.color = "darkred";
            }

        } catch (err) {
            message.textContent = "❌ Network error occurred";
            message.style.color = "darkred";
        }
    });
</script>
</body>
</html>
'''

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    choice = request.form.get('choice')

    cookies_file = os.path.join(os.path.dirname(__file__), "cookies.txt")

    common_opts = [
        "yt-dlp",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "--referer", "https://www.youtube.com/",
        "--extractor-args", "youtube:player_client=android",
        "--no-warnings",
        "-o", DOWNLOAD_FOLDER + r"\%(title)s.%(ext)s"
    ]

    if os.path.exists(cookies_file):
        common_opts.extend(["--cookies", cookies_file])
    else:
        common_opts.extend(["--cookies-from-browser", "chrome"])

    if choice == "1":
        cmd = common_opts + ["-f", "best[ext=mp4]", url]
    else:
        cmd = common_opts + ["-x", "--audio-format", "mp3", "--embed-thumbnail", url]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return jsonify({"status": "done", "message": "Download completed successfully"})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "failed", "error": e.stderr or "Unknown error"})

app.run(host="0.0.0.0", port=5000, debug=True)
