import json
import os
import random

dataset_dir = "train"
coco_json_path = os.path.join(dataset_dir, "_annotations.coco.json")
images_dir = os.path.join(dataset_dir, "train\images")
output_dir = os.path.join(dataset_dir, "split_dataset")

os.makedirs(output_dir, exist_ok=True)

with open(coco_json_path, "r") as f:
    coco_data = json.load(f)

images = coco_data["images"]
annotations = coco_data["annotations"]

random.shuffle(images)

train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

train_cutoff = int(len(images) * train_ratio)
val_cutoff = train_cutoff + int(len(images) * val_ratio)

train_images = images[:train_cutoff]
val_images = images[train_cutoff:val_cutoff]
test_images = images[val_cutoff:]

train_image_ids = {img["id"] for img in train_images}
val_image_ids = {img["id"] for img in val_images}
test_image_ids = {img["id"] for img in test_images}

train_annotations = [ann for ann in annotations if ann["image_id"] in train_image_ids]
val_annotations = [ann for ann in annotations if ann["image_id"] in val_image_ids]
test_annotations = [ann for ann in annotations if ann["image_id"] in test_image_ids]

def create_coco_subset(images, annotations, categories, output_path):
    coco_subset = {
        "images": images,
        "annotations": annotations,
        "categories": categories,
    }
    with open(output_path, "w") as f:
        json.dump(coco_subset, f, indent=4)

categories = coco_data["categories"]

create_coco_subset(train_images, train_annotations, categories, os.path.join(output_dir, "train.json"))
create_coco_subset(val_images, val_annotations, categories, os.path.join(output_dir, "val.json"))
create_coco_subset(test_images, test_annotations, categories, os.path.join(output_dir, "test.json"))

print("Разделение завершено!")
print(f"Train: {len(train_images)} изображений")
print(f"Val: {len(val_images)} изображений")
print(f"Test: {len(test_images)} изображений")
