import os
from PIL import Image

def compress_images_to_target_size(input_folder="dataset", output_folder="dataset2", target_size_mb=20, quality_step=5):
    target_size_bytes = target_size_mb * 1024 * 1024

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".jpg") or file.lower().endswith(".jpeg"):
                input_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_file_path, input_folder)
                output_file_path = os.path.join(output_folder, relative_path)

                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                original_size = os.path.getsize(input_file_path)

                if original_size <= target_size_bytes:
                    print(f"Файл {file} уже меньше {target_size_mb} МБ, копируем без изменений.")
                    os.replace(input_file_path, output_file_path)
                    continue

                print(f"Обрабатываем файл: {file}, исходный размер: {original_size / (1024 * 1024):.2f} МБ")

                try:
                    image = Image.open(input_file_path)
                    quality = 95
                    temp_file_path = f"{output_file_path}.temp_{os.getpid()}.jpg"

                    while quality > 0:
                        image.save(temp_file_path, "JPEG", quality=quality)
                        compressed_size = os.path.getsize(temp_file_path)

                        if compressed_size <= target_size_bytes:
                            os.replace(temp_file_path, output_file_path)
                            print(f"Файл {file} успешно сжат до {compressed_size / (1024 * 1024):.2f} МБ и сохранен в {output_folder}")
                            break
                        else:
                            os.remove(temp_file_path)

                        quality -= quality_step

                    if quality <= 0:
                        print(f"Не удалось сжать {file} до {target_size_mb} МБ")

                except Exception as e:
                    print(f"Ошибка при обработке {file}: {e}")

if __name__ == "__main__":
    compress_images_to_target_size()
