from moviepy.editor import VideoFileClip
import speech_recognition as sr

# Шаг 1: Извлечение аудио из видео
def extract_audio(video_path, audio_output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_output_path)
    video_clip.close()
    return 0

# Шаг 2: Распознавание текста в аудио
def recognize_text(audio_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)
    with audio_file as source:
        audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data, language='ru-RU')  # Используйте свой язык при необходимости
    return text
