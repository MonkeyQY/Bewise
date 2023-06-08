[![Black Formatting](https://github.com/MonkeyQY/Bewise/actions/workflows/main.yml/badge.svg)](https://github.com/MonkeyQY/Bewise/actions/workflows/main.yml)
[![Flake8 Linting](https://github.com/MonkeyQY/Bewise/actions/workflows/flake8.yml/badge.svg)](https://github.com/MonkeyQY/Bewise/actions/workflows/flake8.yml)
# Описание
- Первая часть проекта - это решение, которое достаёт рандомные вопросы для викторины в указанном кол-ве и записывает в базу.
- Вторая часть проекта - это решение, которое позволяет загружать аудио файлы формата wav, конвертирует их в mp3 и позволяет получить их поссылке.

# Запуск проекта
- Клонировать репозиторий 
- Зайти в папку с проектом
- Если запускается сразу 2 задачи, то копировать example_env в .env и заполнить переменные
- Установить Docker и Docker-compose plugin из офф сайта
- `chmod +x run.sh`
- `./run.sh`

* - Для node_exporter нужно подгрузить дашборд в графану после запуска проекта
### Любую задачу можно вырезать с проекта и запустить так же, нужно только удалить роутер и импорты с main.py
### Это сделано для того, чтобы не дублировать 2 одинаковых репозитория с разной логикой


# Подключение к бд по ssh через pgadmin (пример)

![photo_2023-05-21 07 45 39](https://github.com/MonkeyQY/Bewise/assets/105307623/4e1582f3-cb98-4342-98e0-e27da15b2e04)



# Логирование

После запуска контейнера сделать остальные шаги:

- Для просмотра логов через графану нужно зайти на localhost:9000 и ввести логин и пароль admin
- Далее установить data source Loki, Prometheus. 
- В поле адреса Loki плагина ввести `http://loki:3100`
- Аналогично в data source prometheus адрес ввести `http://prom:9090`

# Примеры запросов:

## Task1:
### 1 enpoint
Метод POST, content-type: application/json;

`http://localhost:8000/task1/get_question_num`

С параметрами 

`{
  "questions_num": 10,
}
`

## Task2:
### 1 endpoint
Метод POST, content-type: application/json;

`http://localhost:8000/task2/add_user`

 С параметрами
`{
  "name": "test",
}`
### 2 endpoint
Метод POST, content-type: multipart/form-data;

`http://localhost:8000/task2/add_audio?user_id=user_id&api_token=api_token`

С параметрами 

`{
    "audio": audio.wav
}`

Ответ:

`{
    "url" : "http://localhost:8000/task2/record?user_id=user_id&audio_id=audio_id"
}`

### 3 endpoint
Метод GET

`http://localhost:8000/task2/record?user_id=user_id&audio_id=audio_id`

Ответ:

`audio.mp3`
