from gtts import gTTS
import moviepy.editor as mp
import requests

def generate_voice(text, output_audio="output/audio.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(output_audio)

def fetch_video_background():
    url = "https://source.unsplash.com/720x1280/?nature,abstract"
    response = requests.get(url)
    with open("output/background.jpg", "wb") as file:
        file.write(response.content)

def create_tiktok_video(text):
    generate_voice(text)
    fetch_video_background()
    audio = mp.AudioFileClip("output/audio.mp3")
    background = mp.ImageClip("output/background.jpg").set_duration(audio.duration)
    final_video = background.set_audio(audio)
    final_video.write_videofile("output/tiktok_video.mp4", fps=24)

# Run
create_tiktok_video("This is an AI-generated video!")
