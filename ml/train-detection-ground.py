from ultralytics import YOLO

def main():
    model = YOLO("yolo11n.pt")

    model.train(
        data="./datasets/ground-dataset/data.yaml",
        epochs=300,
        patience=25,
        imgsz=640,
        batch=64,
        lr0=0.003,
        optimizer="AdamW",
        weight_decay=0.004,
        momentum=0.937,
        device=0
    )

if __name__ == "__main__":
    main()
