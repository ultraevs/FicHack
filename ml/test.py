from ultralytics import YOLO

model = YOLO('./models/air-train8.pt')

r = model('./test/air1.JPG', verbose=True, save=True, conf=0.5)

print(r)