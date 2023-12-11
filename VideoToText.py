from moviepy.editor import VideoFileClip
import moviepy.editor as mp
import speech_recognition as sr

# Шаг 1: Извлечение аудио из видео
def extract_audio(video_path, audio_output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_output_path)
    video_clip.close()

# Шаг 2: Распознавание текста в аудио
def recognize_text(audio_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)

    with audio_file as source:
        audio_data = recognizer.record(source)

    text = recognizer.recognize_google(audio_data, language='ru-RU')  # Используйте свой язык при необходимости
    return text

if __name__ == "__main__":
    video_path = "ваш_файл.mp4"
    audio_output_path = "извлеченное_аудио.wav"

    # Шаг 1: Извлечение аудио из видео
    extract_audio(video_path, audio_output_path)

    # Шаг 2: Распознавание текста в аудио
    text_result = recognize_text(audio_output_path)

    print("Распознанный текст:")
    print(text_result)
