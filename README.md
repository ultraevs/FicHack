# FicHack
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)![TensorFlow](https://img.shields.io/badge/tensorflow-%23007ACC.svg?style=for-the-badge&logo=tensorflow)![Figma](https://img.shields.io/badge/figma-%2320232a.svg?style=for-the-badge&logo=figma)<img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Reverse.svg" width="150" height="auto" style="filter: invert(100%) sepia(100%) saturate(0%) hue-rotate(188deg) brightness(94%) contrast(88%);">



# [Ссылка на готовое решение](https://fic.shmyaks.ru/)

### Задача: Разработка модуля классификации опор ЛЭП

## Используемый стек технологий:
- [Python-Backend](https://github.com/ultraevs/FicHack/tree/main/python-backend) - Реализован с использованием [Python](https://www.python.org/) и фреймворка [Fast-API](https://fastapi.tiangolo.com/ru/) - Задачей модуля является обеспечение взаимодействия бекенда сайта и cv модели.
- [Frontend](https://github.com/ultraevs/FicHack/tree/main/frontend) - Реализован с использованием [React](https://ru.legacy.reactjs.org/). Задачай является предоставление красивого и функционалоного интерфейса для пользователя.
- [Deployment](https://github.com/ultraevs/FicHack/tree/main/deployment) - Реализован с использованием [Docker-Compose](https://www.docker.com/). Задачей модуля является возможность быстрого и безошибочного развертывания приложения на любом сервере.
- [CV](https://github.com/ultraevs/FicHack/tree/main/python-backend/cv) - Реализован с использованием [YOLOv8](https://docs.ultralytics.com/ru/models/yolov11/). Задачей модуля является распознавание типа документа на предоставленных фото пользователя.

## Функционал решения

- Загрузка фото.
- Распознавание ЛЭП, а также его типа.
- Возможность загрузки множества фото, а также просмотр истории.


## Как работает решение

1. API принимает изображение в формате base64, декодирует его и передает в модель.
2. Нормализация изображения:
   
   Используя результаты модели, производится определение координат углов документа.
   После этого происходит аппроксимация контура документа до четырех углов.
   На основе угловых точек определяются границы изображения.
   Выполняется перспективное преобразование (выпрямление) изображения с учетом определенных границ.
3. Классификация типа документа:

    Проводится классификация изображения с использованием предварительно обученной модели TensorFlow/Keras.
    Модель определяет тип документа на основе содержимого изображения.
4. Чтение текста с изображения:

    С помощью модели обнаружения текста определяются области с текстом на изображении.
    Каждая область текста обрезается и передается в модель для извлечения фактического текста.
    Полученные текстовые данные агрегируются и предоставляются как результат обработки.
5. Модель возвращает результат в формате json, который выводиться на фронтенд.


## Датасет:
### air:
- https://app.roboflow.com/a-c6uje/upper-lines
- https://app.roboflow.com/cocucku13/electric-lines-4
- https://app.roboflow.com/themeppci/electric-lines-2

### ground:
- https://app.roboflow.com/a-c6uje/default-lap
- https://app.roboflow.com/a-c6uje/electric-tmhb0
- https://app.roboflow.com/cocucku13/ground-lines

## Запуск решения
Необходимо создать .env файлы в папках go-backend и python-backend, в которых должны содержаться ваши данные о сервере,базе данных и почтовом аккаунте. Также в вашем nginx и postgresql на сервере нужно указать те же порты что и в коде(местами из .env)
```sh
    cd GagarinHack/deployment
    docker-compose build
    docker-compose up -d
```
