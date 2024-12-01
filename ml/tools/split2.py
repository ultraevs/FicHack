import os
import random
import shutil


input_dir = "datasets/type-dataset"
output_dir = "datasets/type-dataset"
categories = ["air", "ground"]
train_ratio, valid_ratio, test_ratio = 0.7, 0.15, 0.15

assert train_ratio + valid_ratio + test_ratio == 1.0, "Сумма пропорций должна быть равна 1"

for split in ["train", "valid", "test"]:
    for category in categories:
        os.makedirs(os.path.join(output_dir, split, category), exist_ok=True)

for category in categories:
    category_dir = os.path.join(input_dir, category)
    files = os.listdir(category_dir)
    random.shuffle(files)
    
    total_files = len(files)
    train_end = int(total_files * train_ratio)
    valid_end = train_end + int(total_files * valid_ratio)
    
    train_files = files[:train_end]
    valid_files = files[train_end:valid_end]
    test_files = files[valid_end:]
    
    for split, split_files in zip(["train", "valid", "test"], [train_files, valid_files, test_files]):
        for file in split_files:
            src = os.path.join(category_dir, file)
            dst = os.path.join(output_dir, split, category, file)
            shutil.copy(src, dst)