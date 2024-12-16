from flask import Flask, render_template, request, jsonify
import os
import subprocess

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

        if choice == "1":
            command = [
                "yt-dlp",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",  # Ensure the highest quality video and audio
                "-o", os.path.join(save_path, "%(title)s.%(ext)s"),
                url
            ]
        elif choice == "2":
            command = [
                "yt-dlp",
                "-x", "--audio-format", "mp3",
                "-o", os.path.join(save_path, "%(title)s.%(ext)s"),
                url
            ]
        else:
            return jsonify({"error": "Invalid choice. Please select 1 or 2."}), 400

        subprocess.run(command, check=True)
        return jsonify({"message": f"Download complete! File saved to {save_path}"})

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"An error occurred during download: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')