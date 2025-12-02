from flask import Flask, render_template, request, jsonify, send_file
import os
import yt_dlp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('indextrial.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    choice = request.form.get('choice')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        temp_dir = "/tmp"
        os.makedirs(temp_dir, exist_ok=True)

        if choice == "1":
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'impersonate': 'chrome110',  # ✅ bypass bot blocking
                'nocheckcertificate': True,
                'headers': {  # ✅ PUT IT HERE
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110 Safari/537.36'
                }
            }
        elif choice == "2":
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'impersonate': 'chrome110',  # ✅ bypass bot blocking
                'nocheckcertificate': True,
                'headers': {  # ✅ AND ALSO HERE
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110 Safari/537.36'
                }
            }
        else:
            return jsonify({"error": "Invalid choice. Select 1 or 2"}), 400

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        # Detect the downloaded file safely
        files = os.listdir(temp_dir)
        title = info.get("title")

        downloaded = [f for f in files if title and title in f]

        if not downloaded:
            raise Exception("Downloaded file not found on server.")

        file_path = os.path.join(temp_dir, downloaded[0])
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"Server download failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')

