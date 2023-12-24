import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Функция для создания изображения с текстом
def create_text_image(text, font_size, image_size):
    image = Image.new("RGBA", image_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Установка размера шрифта
    font = ImageFont.truetype("arial.ttf", font_size)

    # Рассчитываем позицию текста
    text_width, text_height = draw.textsize(text, font)
    x = (image_size[0] - text_width) // 2
    y = (image_size[1] - text_height)

    # Добавляем текст на изображение
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

    # Преобразуем изображение к 3-канальному формату
    image = image.convert("RGB")

    return np.array(image)

# Функция для добавления текста в видео
def add_text_to_video(video_path, text, font_size, output_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_size = (int(cap.get(3)), int(cap.get(4)))

    # Создаем изображение с текстом
    text_image = create_text_image(text, font_size, frame_size)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Добавляем текст кадр за кадром
        alpha = 1  # Коэффициент прозрачности для плавного появления
        text_image_with_alpha = cv2.addWeighted(
            np.zeros_like(frame), 1 - alpha, text_image, alpha, 0
        )
        frame_with_text = cv2.addWeighted(frame, 1, text_image_with_alpha, 1, 0)

        # Записываем кадр в выходное видео
        out.write(frame_with_text)

    cap.release()
    out.release()

if __name__ == "__main__":
    video_path = "video.mp4"
    output_path = "result.mp4"
    text = 'число три входит в сложные слова в разных формах'
    font_size = 30

    add_text_to_video(video_path, text, font_size, output_path)
