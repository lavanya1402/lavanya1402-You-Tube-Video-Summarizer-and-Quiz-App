# File: app.py
from flask import Flask, request, jsonify
import os
from src.utils import extract_audio_from_video, transcribe_audio, create_summary, create_quiz

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <!doctype html>
        <html>
        <head><title>Upload Video</title></head>
        <body>
            <h1>Upload a Video File</h1>
            <form method="POST" action="/transcribe" enctype="multipart/form-data">
                <input type="file" name="video"><br><br>
                <input type="submit" value="Summarize and Generate Quiz">
            </form>
        </body>
        </html>
    '''

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    video_path = os.path.join('uploads', video_file.filename)
    audio_path = video_path.replace(".mp4", ".mp3")

    video_file.save(video_path)

    try:
        extract_audio_from_video(video_path, audio_path)
        transcript = transcribe_audio(audio_path)
        summary = create_summary(transcript)
        quiz = create_quiz(summary)

        os.remove(video_path)
        os.remove(audio_path)

        return f"<h1>Summary</h1><p>{summary}</p><h2>Quiz</h2><pre>{quiz}</pre>"

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
