import streamlit as st
import os
import librosa
import librosa.display
import numpy as np
import moviepy.editor as mp
from moviepy.video.fx import fadein, fadeout
from gtts import gTTS

# Streamlit App UI
st.title("🎵 AI Video Generator")
st.write("Convert **songs** into background videos or **text** into TikTok-style videos!")

# Create a data folder if not exists
if not os.path.exists("data"):
    os.makedirs("data")


# 🎵 Function: Song to Video
def generate_video_from_song(song_path, output_video="song_video.mp4"):
    try:
        y, sr = librosa.load(song_path, sr=None)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)[1]

        clip = mp.ColorClip(size=(720, 1280), color=(30, 144, 255), duration=librosa.get_duration(y=y, sr=sr))
        clip = fadein.fadein(clip, 1).fx(fadeout.fadeout, 1)

        audio = mp.AudioFileClip(song_path)
        clip = clip.set_audio(audio)

        clip.write_videofile(output_video, fps=24, codec="libx264")
        return output_video
    except Exception as e:
        return str(e)


# 📜 Function: Text to Video
def generate_video_from_text(text, output_video="text_video.mp4"):
    try:
        # Convert text to speech
        tts = gTTS(text, lang="en")
        audio_path = "text_audio.mp3"
        tts.save(audio_path)

        # Create a simple background video
        clip = mp.ColorClip(size=(720, 1280), color=(255, 255, 255), duration=5)
        audio = mp.AudioFileClip(audio_path)
        clip = clip.set_audio(audio)

        clip.write_videofile(output_video, fps=24, codec="libx264")

        os.remove(audio_path)
        return output_video
    except Exception as e:
        return str(e)


# 🎶 Upload Song Feature
st.header("🎶 Upload a Song to Generate Video")
uploaded_song = st.file_uploader("Upload a song file (MP3)", type=["mp3"])

if uploaded_song:
    song_path = os.path.join("data", uploaded_song.name)
    with open(song_path, "wb") as f:
        f.write(uploaded_song.getbuffer())

    st.success("Song uploaded successfully!")
    
    if st.button("Generate Video from Song"):
        output_video = generate_video_from_song(song_path)
        st.video(output_video)
        st.download_button("Download Video", open(output_video, "rb").read(), file_name="song_video.mp4")


# 📜 Text to Video Feature
st.header("📜 Enter Text to Generate Video")
text_input = st.text_area("Enter your text here:")

if st.button("Generate Video from Text"):
    if text_input.strip():
        output_video = generate_video_from_text(text_input)
        st.video(output_video)
        st.download_button("Download Video", open(output_video, "rb").read(), file_name="text_video.mp4")
    else:
        st.warning("Please enter some text before generating the video.")

st.write("Developed with ❤️ using Streamlit, MoviePy, and Librosa")
