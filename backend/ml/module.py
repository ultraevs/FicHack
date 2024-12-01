import cv2
import numpy as np
import time
from collections import Counter
from typing import List, Tuple, Dict, Any, Optional

from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont


class Detector:
    """
    A detector class that utilizes YOLO models to classify images and detect objects
    in either ground or air categories. It provides functionalities to preprocess images,
    adjust bounding boxes, perform detection, and visualize the results with bounding
    boxes and labels.
    """

    def __init__(self) -> None:
        """
        Initializes the Detector with pre-trained YOLO models for classification,
        ground detection, and air detection. It also sets up class names and colors
        for visualization.
        """
        # Initialize YOLO models
        self.classificator = YOLO('ml/models/classify-train3.pt')
        self.ground_detector = YOLO('ml/models/ground-train4.pt')
        self.air_detector = YOLO('ml/models/air-train8.pt')

        # Define class names for ground and air detectors
        self.class_names_ground = ['Другая', 'Рюмка', 'Башенная']
        self.class_names_air = ['Другая', 'Рюмка', 'Башенная']

        # Define colors for each class in ground and air detectors
        self.colors_ground = [
            (74, 74, 252),   # Другая (Other)
            (255, 0, 0),     # Рюмка (Rumka)
            (0, 255, 0)      # Башенная (Tower-type)
        ]
        self.colors_air = [
            (74, 74, 252),   # Другая (Other)
            (255, 0, 0),     # Рюмка (Rumka)
            (0, 255, 0)      # Башенная (Tower-type)
        ]

    def preprocess_image(
        self, 
        img: np.ndarray, 
        target_size: Tuple[int, int] = (953, 536), 
        corner_radius: int = 12
    ) -> Tuple[np.ndarray, float, int, int]:
        """
        Preprocesses the input image by resizing it to the target size with aspect ratio preserved,
        adding padding, and applying rounded corners.

        Args:
            img (np.ndarray): The original image.
            target_size (Tuple[int, int], optional): The desired size (width, height) of the output image.
                Defaults to (953, 536).
            corner_radius (int, optional): The radius for the rounded corners. Defaults to 12.

        Returns:
            Tuple[np.ndarray, float, int, int]: A tuple containing the preprocessed image,
                the scaling factor, the top padding, and the left padding.
        """
        original_height, original_width = img.shape[:2]
        scale = min(target_size[1] / original_height, target_size[0] / original_width)
        new_width, new_height = int(original_width * scale), int(original_height * scale)

        # Resize the image while maintaining aspect ratio
        resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

        # Create a white canvas and center the resized image on it
        canvas = np.ones((target_size[1], target_size[0], 3), dtype=np.uint8) * 255
        top = (target_size[1] - new_height) // 2
        left = (target_size[0] - new_width) // 2
        canvas[top:top + new_height, left:left + new_width] = resized_img

        # Convert to PIL image for drawing rounded corners
        img_pil = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))

        # Create a mask with rounded corners
        mask = Image.new('L', target_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(
            [(left, top), (left + new_width, top + new_height)],
            radius=corner_radius,
            fill=255
        )

        # Apply the mask to the image
        mask_np = np.array(mask)
        corners_mask = mask_np == 0
        canvas[corners_mask] = 255

        return canvas, scale, top, left

    def adjust_boxes(
        self, 
        boxes: Any, 
        scale: float, 
        top: int, 
        left: int, 
        img_width: int, 
        img_height: int
    ) -> List[Tuple[int, int, int, int, int, float]]:
        """
        Adjusts the bounding box coordinates based on the scaling and padding applied during preprocessing.

        Args:
            boxes (Any): The detected boxes from the YOLO model.
            scale (float): The scaling factor applied to the image.
            top (int): The top padding added to the image.
            left (int): The left padding added to the image.
            img_width (int): The original width of the image.
            img_height (int): The original height of the image.

        Returns:
            List[Tuple[int, int, int, int, int, float]]: A list of adjusted bounding boxes with
                (x1, y1, x2, y2, class_id, confidence).
        """
        adjusted_boxes = []
        for box in boxes:
            coords = box.xyxyn.cpu().numpy().flatten()
            x1 = int(coords[0] * img_width * scale + left)
            y1 = int(coords[1] * img_height * scale + top)
            x2 = int(coords[2] * img_width * scale + left)
            y2 = int(coords[3] * img_height * scale + top)
            class_id = int(box.cls.item())
            confidence = box.conf.item()
            adjusted_boxes.append((x1, y1, x2, y2, class_id, confidence))
        return adjusted_boxes

    def work(self, img: np.ndarray) -> Dict[str, Any]:
        """
        Processes the input image by classifying it as either 'ground' or 'air' and then performing
        object detection accordingly. It also annotates the image with bounding boxes and labels.

        Args:
            img (np.ndarray): The original image to be processed.

        Returns:
            Dict[str, Any]: A dictionary containing the annotated images, average confidence,
                time taken for processing, and a summary of detected objects.
        """
        start_time = time.time()

        # Classify the image to determine which detector to use
        classification_result = self.classificator(img, save=False, verbose=False)
        classname_probs = classification_result[0].probs.top5
        classname = "ground" if classname_probs[0] > classname_probs[1] else "air"

        # Select the appropriate detector based on classification
        if classname == "ground":
            detection_result = self.ground_detector(img, save=False, verbose=False)
            boxes = detection_result[0].boxes if detection_result[0].boxes else []
            class_names = self.class_names_ground
            class_colors = self.colors_ground
        elif classname == "air":
            detection_result = self.air_detector(img, save=False, verbose=False, conf=0.25)
            boxes = detection_result[0].boxes if detection_result[0].boxes else []
            class_names = self.class_names_air
            class_colors = self.colors_air
        else:
            boxes = []
            class_names = []
            class_colors = []

        # Preprocess the image for visualization
        preprocessed_img, scale, top, left = self.preprocess_image(img)
        empty = preprocessed_img.copy()

        if boxes:
            # Adjust bounding boxes based on preprocessing
            adjusted_boxes = self.adjust_boxes(
                boxes, scale, top, left, img.shape[1], img.shape[0]
            )
            # Draw bounding boxes on the image
            boxes_img = self.draw_boxes(preprocessed_img, adjusted_boxes, class_colors)
            boxes_with_classes = self.draw_boxes_with_labels(
                preprocessed_img.copy(),
                adjusted_boxes,
                class_names=class_names,
                colors=class_colors,
                with_conf=False
            )
            boxes_with_classes_and_conf = self.draw_boxes_with_labels(
                preprocessed_img.copy(),
                adjusted_boxes,
                class_names=class_names,
                colors=class_colors,
                with_conf=True
            )
            # Calculate average confidence
            avg_conf = np.mean([box.conf.item() for box in boxes])

            # Count occurrences of each detected class
            class_indices = [box.cls.item() for box in boxes]
            detected_class_names = [class_names[int(idx)] for idx in class_indices]
            class_counts = Counter(detected_class_names)
            sorted_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)

            # Create a summary string of detected objects
            objects_str = ", ".join([f"{count} {name}" for name, count in sorted_classes])

        else:
            boxes_img = preprocessed_img
            boxes_with_classes = preprocessed_img.copy()
            boxes_with_classes_and_conf = preprocessed_img.copy()
            avg_conf = 0.0
            objects_str = ""  # No objects detected

        # Calculate time taken for processing
        time_taken = int((time.time() - start_time) * 1000)  # in milliseconds

        return {
            'images': [
                boxes_img,
                boxes_with_classes,
                boxes_with_classes_and_conf,
                empty
            ],
            'avg-conf': f"{avg_conf:.2f}",
            'time-taken': f"{time_taken}ms",
            'objects': objects_str
        }

    def draw_boxes(
        self, 
        img: np.ndarray, 
        boxes: List[Tuple[int, int, int, int, int, float]], 
        class_colors: List[Tuple[int, int, int]]
    ) -> np.ndarray:
        """
        Draws semi-transparent colored bounding boxes on the image.

        Args:
            img (np.ndarray): The image on which to draw the boxes.
            boxes (List[Tuple[int, int, int, int, int, float]]): A list of bounding boxes with
                (x1, y1, x2, y2, class_id, confidence).
            class_colors (List[Tuple[int, int, int]]): A list of colors corresponding to each class.

        Returns:
            np.ndarray: The image with drawn bounding boxes.
        """
        for x1, y1, x2, y2, cls, _ in boxes:
            color = class_colors[cls % len(class_colors)]
            overlay = img.copy()
            # Draw filled rectangle with transparency
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, thickness=-1)
            alpha = 0.15  # Transparency factor
            cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
            # Draw rectangle border
            cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness=1)
        return img

    def draw_boxes_with_labels(
        self, 
        img: np.ndarray, 
        boxes: List[Tuple[int, int, int, int, int, float]], 
        class_names: List[str], 
        colors: List[Tuple[int, int, int]], 
        with_conf: bool = False
    ) -> np.ndarray:
        """
        Draws bounding boxes with class labels (and optional confidence scores) on the image.

        Args:
            img (np.ndarray): The image on which to draw.
            boxes (List[Tuple[int, int, int, int, int, float]]): A list of bounding boxes with
                (x1, y1, x2, y2, class_id, confidence).
            class_names (List[str]): A list of class names.
            colors (List[Tuple[int, int, int]]): A list of colors corresponding to each class.
            with_conf (bool, optional): Whether to include confidence scores in the labels. Defaults to False.

        Returns:
            np.ndarray: The image with drawn bounding boxes and labels.
        """
        if not class_names or not colors:
            return img

        # Convert image to PIL format for easier text drawing
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        # Attempt to load a custom font, fallback to default if unavailable
        try:
            font = ImageFont.truetype("./ml/tilda-sans_light.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        for x1, y1, x2, y2, cls, conf in boxes:
            # Determine the label and color
            if cls >= len(class_names):
                label = f"Class {cls + 1}"
                color = (0, 0, 0)  # Default color for unknown classes
            else:
                label = class_names[cls]
                color = colors[cls % len(colors)]

            if with_conf:
                label += f" [{conf:.2f}]"

            # Calculate text size
            text_bbox = draw.textbbox((0, 0), label, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            padding = 5
            rect_padding_outside = 5
            rect_padding_inside = 1

            # Determine label position to avoid drawing outside the image
            if y1 - text_height - 2 * rect_padding_outside - padding >= 0:
                label_x = x1
                label_y = y1 - text_height - 2 * rect_padding_outside
                current_rect_padding = rect_padding_outside
            else:
                label_x = x1
                label_y = y1
                current_rect_padding = rect_padding_inside

            # Convert BGR to RGB for PIL
            color_rgb = (color[2], color[1], color[0])

            # Draw rectangle border
            draw.rectangle([x1, y1, x2, y2], outline=color_rgb, width=1)

            # Draw filled rectangle for the label background
            draw.rectangle(
                [
                    label_x,
                    label_y,
                    label_x + text_width + 2 * current_rect_padding,
                    label_y + text_height + 2 * current_rect_padding
                ],
                fill=color_rgb
            )

            # Determine text color based on background brightness
            brightness = (0.299 * color_rgb[0] + 0.587 * color_rgb[1] + 0.114 * color_rgb[2])
            text_color = (255, 255, 255) if brightness < 128 else (0, 0, 0)

            # Draw the label text
            draw.text(
                (label_x + current_rect_padding, label_y + current_rect_padding),
                label,
                fill=text_color,
                font=font
            )

        # Convert back to OpenCV format
        img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        return img


# Example usage (Uncomment the following lines to run):
# if __name__ == "__main__":
#     detector = Detector()
#
#     img_path = 'tests/air1.png'
#     img = cv2.imread(img_path)
#     result = detector.work(img)
#
#     cv2.imwrite('output/boxes.jpg', result['images'][0])
#     cv2.imwrite('output/boxes_with_classes.jpg', result['images'][1])
#     cv2.imwrite('output/boxes_with_classes_and_conf.jpg', result['images'][2])
#     cv2.imwrite('output/empty.jpg', result['images'][3])
#
#     # Print the result dictionary
#     print(result)
