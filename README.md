# FicHack
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)![TensorFlow](https://img.shields.io/badge/tensorflow-%23007ACC.svg?style=for-the-badge&logo=tensorflow)![Figma](https://img.shields.io/badge/figma-%2320232a.svg?style=for-the-badge&logo=figma)<img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Reverse.svg" width="150" height="auto" style="filter: invert(100%) sepia(100%) saturate(0%) hue-rotate(188deg) brightness(94%) contrast(88%);">



# [Ссылка на готовое решение](http://fic.shmyaks.ru/)
# [Figma](https://www.figma.com/design/GlHiFhDimaiu0QXZdXPHJ8/fic-hack?node-id=27-2&t=IlNR9lbFcYyQI9D6-1)

### Задача: Разработка модуля классификации опор ЛЭП

## Используемый стек технологий:
- [Python-Backend](https://github.com/ultraevs/FicHack/tree/main/backend) - Реализован с использованием [Python](https://www.python.org/) и фреймворка [Fast-API](https://fastapi.tiangolo.com/ru/) - Задачей модуля является обеспечение взаимодействия бекенда сайта и cv модели.
- [Frontend](https://github.com/ultraevs/FicHack/tree/main/frontend/fic-hack) - Реализован с использованием [React](https://ru.legacy.reactjs.org/). Задачай является предоставление красивого и функционалоного интерфейса для пользователя.
- [Deployment](https://github.com/ultraevs/FicHack/tree/main/deployment) - Реализован с использованием [Docker-Compose](https://www.docker.com/). Задачей модуля является возможность быстрого и безошибочного развертывания приложения на любом сервере.
- [CV](https://github.com/ultraevs/FicHack/tree/main/backend/ml) - Реализован с использованием [YOLOv11](https://docs.ultralytics.com/ru/models/yolo11/). Задачей модуля является распознавание типа документа на предоставленных фото пользователя.

## Функционал решения

- Загрузка изображений для обработки.
- Классификация опор на категории «Наземная» и «Воздушная».
- Распознавание типов опор, таких как «Рюмка» и «Башенная».
- Просмотр истории обработки изображений для авторизованных пользователей.

## Как работает решение

1. Загрузка и обработка изображений:
    - Изображения передаются в формате Base64 и декодируются на сервере.
    - Затем передаются в модель YOLOv11 для классификации.

2. Предобработка:
    - Изображения изменяются по размеру и дополняются полями для сохранения пропорций.
    - Применяются скругленные углы для стандартизации.

3. Детекция:
    - Изображения классифицируются как «Наземная» или «Воздушная» опора.
    - Для детекции используются соответствующие модели YOLO.

4. Постобработка:
    - Координаты обнаруженных объектов корректируются для визуализации.
    - Каждое обнаружение аннотируется классом и уровнем уверенности.

5. Сохранение данных:
    - Результаты сохраняются в PostgreSQL, включая метаданные и результаты классификации.

6. Ответ:
    - Бекенд возвращает JSON с деталями классификации, аннотированными изображениями и метаданными.


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
Необходимо создать .env файл формата
```sh
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=pass
    DB_HOST=ip
    DB_PORT=5432
```
в папке deployment, в которых должны содержаться ваши данные о базе данных. Также в вашем nginx и postgresql на сервере нужно указать те же порты что и в коде(местами из .env)
```sh
    cd FicHack/deployment
    docker-compose build
    docker-compose up -d
```

##  Состав команды
 - Илья Ломаев - Frontend Developer
 - Михаил Евсеев - Backend Developer
 - Артем Брежнев - Designer
 - Иван Лобода - CV
 - Костя Цой - Frontend Developer
 - Глеб Таланцев - Project Manager

## Итог
Проект представляет собой инновационное решение для классификации опор линий электропередач (ЛЭП). Его значимость заключается в интеграции современных технологий компьютерного зрения с удобным пользовательским интерфейсом. Благодаря использованию мощных инструментов, таких как YOLOv11, FastAPI, React и Docker, команда создала продукт, способный автоматически распознавать типы и категории опор с высокой точностью.

Этот проект выделяется на фоне аналогов своей гибкостью, функциональностью и модульной архитектурой, что делает его легко адаптируемым к различным сценариям использования. Решение экономит время и ресурсы для специалистов, занимаясь рутинной обработкой данных, и может быть применено в таких областях, как инвентаризация, мониторинг и анализ инфраструктуры ЛЭП.

## Возможные улучшения
Расширение функциональности:

Добавление новых категорий и подтипов опор для более точной классификации.
Включение возможности обработки видео для детекции опор в реальном времени.
Улучшение UX/UI:

Разработка мобильного приложения для упрощения работы в полевых условиях.
Визуализация результатов в формате интерактивных карт.
Технические улучшения:

Интеграция моделей на базе больших языковых моделей для анализа текста и голосовых команд.
Ускорение процесса обработки изображений с использованием аппаратного ускорения (GPU).
Автоматизация развертывания:

Добавление поддержки CI/CD для еще более быстрого и удобного развертывания.
