# PyProject_get_subtitles
Add subtitles in videos
Состав команды: Удальцов Андрей, Тураева Маргарита, Валов Артем

Отчет о промежуточной работе:

1) Валов Артем: 
Создал api-ключ бота, реализовал его работу, добавил заготовку для основных функций бота (кнопки помощь, создать субтитры и добавить заметку в гугл календарь), осталось дождаться реализованных функций, добавить их на место заготовок, понять что требуется передавать в функции, а затем запрашивать у пользователя всё необходимое и разделять на нужное количество переменных в нужном формате

3) Тураева Маргарита:
Создала сервисный аккаунт google, настроила его, написала основу реализации функции добавления события в календарь(работающий код, но нужно ещё адаптировать этот код под бота). Ещё осталось доработать фронтенд

3) Удальцов Андрей:
Написал функцию принимающую на вход в переменную видео в формате mp4, из которого потом извлек аудио с помощью moviepy. Далее извлекаю из аудио текст с помощью SpeechRecognition. на гите лежит код, там я подробнее с комменатриями расписал что где в какой части кода происходит. Еще в процессе работаю с шумами, может быть некачественное аудио.

Подробное описание алгоритма:

  a). **Извлечение аудио из видео:**
   - Используется библиотека `moviepy` для открытия видеофайла в формате MP4.
   - Аудиодорожка извлекается из видеофайла.
   - Аудио сохраняется в отдельный файл (в формате WAV) с помощью метода `write_audiofile`.

  b). **Распознавание текста в аудио:**
   - Используется библиотека `SpeechRecognition` для распознавания речи.
   - Аудиофайл открывается с использованием `AudioFile`.
   - Речь записывается из аудиофайла с помощью `recognizer.record`.
   - Распознавание текста осуществляется с использованием Google Speech Recognition API (`recognize_google`).
   - Результат распознавания выводится на экран.

  c). **Порядок вызова:**
   - Задается путь к видеофайлу (`video_path`) и путь для сохранения извлеченного аудио (`audio_output_path`).
   - Функция `extract_audio` вызывается для извлечения аудио.
   - Функция `recognize_text` вызывается для распознавания текста в извлеченном аудио.
   - Распознанный текст выводится на экран.
