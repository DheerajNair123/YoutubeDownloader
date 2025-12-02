from flask import Flask, render_template, request, jsonify, send_file
import os
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('indextrial.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    choice = request.form['choice']

    try:
        temp_dir = "/tmp"
        ydl_opts = {}

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
            return jsonify({"error": "Invalid choice. Select 1 or 2"}), 400

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            if choice == "2":
                filename = filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"Unexpected server error: {str(e)}"}), 500



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

