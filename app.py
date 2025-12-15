from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

# Simple download folder
DOWNLOAD_FOLDER = r"C:\Users\dheer\Downloads\DownloadedYT\newsongs"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>YouTube Downloader</title>
    </head>
    <body>
        <h2>YouTube Downloader</h2>
        <form id="downloadForm">
            <input type="text" name="url" id="url" placeholder="Enter YouTube URL" size="40"><br><br>
            <select name="choice" id="choice">
                <option value="1">Download MP4 (Video)</option>
                <option value="2">Download MP3 (Audio)</option>
            </select><br><br>
            <button type="submit">Download</button>
        </form>
        <div id="message" style="margin-top: 20px; font-weight: bold;"></div>
        
        <script>
            document.getElementById('downloadForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const url = document.getElementById('url').value;
                const choice = document.getElementById('choice').value;
                const messageDiv = document.getElementById('message');
                
                messageDiv.textContent = 'Downloading... Please wait.';
                messageDiv.style.color = 'blue';
                
                const formData = new FormData();
                formData.append('url', url);
                formData.append('choice', choice);
                
                try {
                    const response = await fetch('/download', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.status.includes('done')) {
                        messageDiv.textContent = result.status + ' ' + (result.message || '');
                        messageDiv.style.color = 'green';
                    } else {
                        messageDiv.textContent = result.status + (result.error ? ': ' + result.error : '');
                        messageDiv.style.color = 'red';
                    }
                } catch (error) {
                    messageDiv.textContent = 'Error: ' + error.message;
                    messageDiv.style.color = 'red';
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
    
    # Path to cookies file
    cookies_file = os.path.join(os.path.dirname(__file__), "cookies.txt")
    
    # Common options to avoid 403 errors
    common_opts = [
        "yt-dlp",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "--referer", "https://www.youtube.com/",
        "--add-header", "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "--add-header", "Accept-Language:en-us,en;q=0.5",
        "--add-header", "Sec-Fetch-Mode:navigate",
        "--extractor-args", "youtube:player_client=android",
        "--no-check-certificate",
        "--no-warnings",
        "-o", DOWNLOAD_FOLDER + r"\%(title)s.%(ext)s"
    ]
    
    # Try to use cookies from browser first, then fall back to cookies.txt
    if os.path.exists(cookies_file):
        common_opts.extend(["--cookies", cookies_file])
    else:
        # Try to extract cookies from Chrome browser
        common_opts.extend(["--cookies-from-browser", "chrome"])

    if choice == '1':
        cmd = common_opts + ["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", url]
    else:
        cmd = common_opts + ["-x", "--audio-format", "mp3", "--embed-thumbnail", url]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return jsonify({"status": "Download done!", "message": "File saved to Downloads folder"})
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return jsonify({"status": "Download failed!", "error": error_msg})

app.run(host="0.0.0.0", port=5000, debug=True)
