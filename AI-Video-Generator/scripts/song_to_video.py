import librosa
import librosa.display
import numpy as np
import moviepy.editor as mp
import cv2

def detect_beats(song_path):
    y, sr = librosa.load(song_path, sr=None)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return beat_times

def create_video(song_path, output_video="output/song_video.mp4"):
    beat_times = detect_beats(song_path)
    clip = mp.ColorClip(size=(720, 1280), color=(0, 0, 0), duration=len(beat_times))
    audio = mp.AudioFileClip(song_path)
    final_video = clip.set_audio(audio)
    final_video.write_videofile(output_video, fps=24)

# Run
create_video("data/input_song.mp3")
