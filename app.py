from flask import Flask, render_template, request, jsonify, send_file
import os
import yt_dlp

app = Flask(__name__)

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

        # Ensure temp directory exists
        os.makedirs(temp_dir, exist_ok=True)

        if choice == "1":
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s')
            }
        elif choice == "2":
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s')
            }
        else:
            return jsonify({"error": "Invalid choice. Select 1 (MP4) or 2 (MP3)"}), 400

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        # Find the downloaded file
        files = os.listdir(temp_dir)
        title = info.get("title")

        downloaded = [f for f in files if title and title in f]

        if not downloaded:
            raise Exception("Downloaded file not found on server.")

        file_path = os.path.join(temp_dir, downloaded[0])

        # Send file to user (browser will download and save it locally)
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        # Send exact server error to frontend
        return jsonify({"error": f"Server download failed: {str(e)}"}), 500


if __name__ == "__main__":
    # This will NOT run in production, Gunicorn will handle the app
    app.run(debug=True, host='0.0.0.0')
