from ultralytics import YOLO

def main():
    model = YOLO("yolo11n.pt")

    model.train(
        data="./datasets/air-dataset/data.yaml",
        epochs=100,  # Увеличенное количество эпох
        patience=20,  # Увеличенное терпение для ранней остановки
        imgsz=800,  # Размер изображений
        batch=32,  # Увеличенный размер батча
        device=0,  # Использование первого GPU
        optimizer="AdamW",  # Использование оптимизатора AdamW
        lr0=0.001,  # Уменьшенный начальный learning rate
        val=True,  # Включение валидации
        augment=True,  # Включение аугментаций
        classes=None  # Используйте все классы
    )

if __name__ == "__main__":
    main()
