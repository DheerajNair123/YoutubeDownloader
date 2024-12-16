from flask import Flask, render_template, request, jsonify
import os
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('indextrail.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    choice = request.form['choice']
    
    try:
        save_path = os.path.expanduser("~/Downloads/DownloadedYT")  # Default to Downloads folder

        ydl_opts = {}
        if choice == "1":
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s')
            }
        elif choice == "2":
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s')
            }
        else:
            return jsonify({"error": "Invalid choice. Please select 1 or 2."}), 400

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return jsonify({"message": f"Download complete! File saved to {save_path}"})

    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": f"An error occurred during download: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
