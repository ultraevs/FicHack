from ultralytics import YOLO

def main():
    model = YOLO('yolo11n-cls.pt')

    results = model.train(
        data='./datasets/type-dataset',
        epochs=50,
        imgsz=640,
        batch=16,
        device=0
    )

if __name__ == "__main__":
    main()