from PIL import Image
import os

# Пути к папкам
base_dir = "datasets/type-dataset"
folders = ["train/ground", "valid/ground", "test/ground"]
target_size = (640, 640)


def resize_images_in_folder(folder_path, size):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                with Image.open(file_path) as img:
                    img_resized = img.resize(size, Image.Resampling.LANCZOS)
                    img_resized.save(file_path)
                print(f"Изображение {filename} успешно изменено.")
            except Exception as e:
                print(f"Ошибка с файлом {filename}: {e}")

for folder in folders:
    folder_path = os.path.join(base_dir, folder)
    resize_images_in_folder(folder_path, target_size)