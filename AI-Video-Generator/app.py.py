from flask import Flask, request, jsonify
import os
from scripts.song_to_video import create_video
from scripts.text_to_video import create_tiktok_video

app = Flask(__name__)

@app.route("/song-to-video", methods=["POST"])
def song_to_video():
    data = request.json
    song_path = data.get("song_path", "data/input_song.mp3")
    create_video(song_path)
    return jsonify({"message": "Video generated", "video_path": "output/song_video.mp4"})

@app.route("/text-to-video", methods=["POST"])
def text_to_video():
    data = request.json
    text = data.get("text", "Hello, world!")
    create_tiktok_video(text)
    return jsonify({"message": "TikTok video generated", "video_path": "output/tiktok_video.mp4"})

if __name__ == "__main__":
    app.run(debug=True)
