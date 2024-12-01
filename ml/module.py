import cv2
import numpy as np
from ultralytics import YOLO
import time
from PIL import Image, ImageDraw, ImageFont
from collections import Counter

class Detector:
    def __init__(self):
        self.classificator = YOLO('./models/classify-train3.pt')
        self.ground_detector = YOLO('./models/ground-train4.pt')
        self.air_detector = YOLO('./models/air-train8.pt')
        
        self.class_names_ground = ['Другая', 'Рюмка', 'Башенная']
        self.class_names_air = ['Другая', 'Рюмка', 'Башенная']
        
        self.colors_ground = [
            (74, 74, 252),   # other
            (255, 0, 0),     # rumka
            (0, 255, 0)      # tower-type
        ]
        self.colors_air = [
            (74, 74, 252),   # other
            (255, 0, 0),     # rumka
            (0, 255, 0)      # tower-type
        ]

    def preprocess_image(self, img, target_size=(953, 536), corner_radius=12):
        h, w = img.shape[:2]
        scale = min(target_size[1] / h, target_size[0] / w)
        new_w, new_h = int(w * scale), int(h * scale)
        resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        
        canvas = np.ones((target_size[1], target_size[0], 3), dtype=np.uint8) * 255
        top = (target_size[1] - new_h) // 2
        left = (target_size[0] - new_w) // 2
        canvas[top:top+new_h, left:left+new_w] = resized_img

        img_pil = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        
        mask = Image.new('L', target_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(left, top), (left + new_w, top + new_h)], radius=corner_radius, fill=255)
        
        mask_np = np.array(mask)
        
        corners_mask = mask_np == 0
        
        canvas[corners_mask] = 255
        
        return canvas, scale, top, left

    def adjust_boxes(self, boxes, scale, top, left, img_width, img_height):
        adjusted_boxes = []
        for box in boxes:
            coords = box.xyxyn.cpu().numpy().flatten()
            x1 = int(coords[0] * img_width * scale + left)
            y1 = int(coords[1] * img_height * scale + top)
            x2 = int(coords[2] * img_width * scale + left)
            y2 = int(coords[3] * img_height * scale + top)
            adjusted_boxes.append((x1, y1, x2, y2, int(box.cls.item()), box.conf.item()))
        return adjusted_boxes

    def work(self, img):
        start_time = time.time()

        r = self.classificator(img, save=False, verbose=False)
        classname_probs = r[0].probs.top5
        classname = "ground" if classname_probs[0] > classname_probs[1] else "air"

        if classname == "ground":
            r = self.ground_detector(img, save=False, verbose=False)
            result = r[0].boxes if r[0].boxes else []
            class_names = self.class_names_ground
            class_colors = self.colors_ground
        elif classname == "air":
            r = self.air_detector(img, save=False, verbose=False, conf=0.25)
            result = r[0].boxes if r[0].boxes else []
            class_names = self.class_names_air
            class_colors = self.colors_air
        else:
            result = []
            class_names = []
            class_colors = []

        preprocessed_img, scale, top, left = self.preprocess_image(img)

        if result:
            adjusted_boxes = self.adjust_boxes(result, scale, top, left, img.shape[1], img.shape[0])
            boxes_img = self.draw_boxes(preprocessed_img, adjusted_boxes, class_colors)
            boxes_with_classes = self.draw_boxes_with_labels(preprocessed_img.copy(), adjusted_boxes, class_names=class_names, colors=class_colors, with_conf=False)
            boxes_with_classes_and_conf = self.draw_boxes_with_labels(preprocessed_img.copy(), adjusted_boxes, class_names=class_names, colors=class_colors, with_conf=True)
            avg_conf = np.mean([box.conf.item() for box in result])

            class_indices = [box.cls.item() for box in result]

            detected_class_names = [class_names[int(idx)] for idx in class_indices]
            class_counts = Counter(detected_class_names)
            sorted_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)

            objects_str = ", ".join([f"{count} {name}" for name, count in sorted_classes])

        else:
            boxes_img = preprocessed_img
            boxes_with_classes = preprocessed_img.copy()
            boxes_with_classes_and_conf = preprocessed_img.copy()
            avg_conf = 0
            objects_str = ""  # No objects detected

        time_taken = int((time.time() - start_time) * 1000)

        return {
            'images': [boxes_img, boxes_with_classes, boxes_with_classes_and_conf],
            'avg-conf': f"{avg_conf:.2f}",
            'time-taken': f"{time_taken}ms",
            'objects': objects_str  # **Modified Here**
        }

    def draw_boxes(self, img, boxes, class_colors):
        for x1, y1, x2, y2, cls, _ in boxes:
            color = class_colors[cls % len(class_colors)]
            overlay = img.copy()
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, thickness=-1)
            alpha = 0.15
            cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness=1)
        return img

    def draw_boxes_with_labels(self, img, boxes, class_names, colors, with_conf=False):
        if not class_names or not colors:
            return img

        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        try:
            font = ImageFont.truetype("tilda-sans_light.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        for x1, y1, x2, y2, cls, conf in boxes:
            if cls >= len(class_names):
                label = f"Class {cls + 1}"
                color = (0, 0, 0)
            else:
                label = class_names[cls]
                color = colors[cls % len(colors)]

            if with_conf:
                label += f" [{conf:.2f}]"

            text_bbox = draw.textbbox((0, 0), label, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            padding = 5
            rect_padding_outside = 5
            rect_padding_inside = 1

            if y1 - text_height - 2 * rect_padding_outside - padding >= 0:
                label_x = x1
                label_y = y1 - text_height - 2 * rect_padding_outside
                current_rect_padding = rect_padding_outside
            else:
                label_x = x1
                label_y = y1
                current_rect_padding = rect_padding_inside

            color_rgb = (color[2], color[1], color[0])

            draw.rectangle([x1, y1, x2, y2], outline=color_rgb, width=1)

            draw.rectangle(
                [
                    label_x,
                    label_y,
                    label_x + text_width + 2 * current_rect_padding,
                    label_y + text_height + 2 * current_rect_padding
                ],
                fill=color_rgb
            )

            brightness = (0.299 * color_rgb[0] + 0.587 * color_rgb[1] + 0.114 * color_rgb[2])
            text_color = (255, 255, 255) if brightness < 128 else (0, 0, 0)

            draw.text(
                (label_x + current_rect_padding, label_y + current_rect_padding),
                label,
                fill=text_color,
                font=font
            )

        img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        return img

    
if __name__ == "__main__":
    detector = Detector()

    img_path = './test/air2.jpg'
    img = cv2.imread(img_path)
    result = detector.work(img)

    cv2.imwrite('./output/boxes.jpg', result['images'][0])
    cv2.imwrite('./output/boxes_with_classes.jpg', result['images'][1])
    cv2.imwrite('./output/boxes_with_classes_and_conf.jpg', result['images'][2])

    # print(result)