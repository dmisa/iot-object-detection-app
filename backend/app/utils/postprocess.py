import numpy as np

def non_max_suppression(boxes, scores, iou_threshold):
    if len(boxes) == 0:
        return []

    # Convert boxes to (x1, y1, x2, y2) format
    x1 = boxes[:, 1]
    y1 = boxes[:, 0]
    x2 = boxes[:, 3]
    y2 = boxes[:, 2]

    # Compute areas of the boxes
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]  # Sort scores in descending order

    selected_indices = []
    while order.size > 0:
        i = order[0]
        selected_indices.append(i)

        # Compute IoU of the remaining boxes with the highest-scoring box
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        intersection = w * h
        union = areas[i] + areas[order[1:]] - intersection
        iou = intersection / union

        # Keep boxes with IoU below the threshold
        remaining = np.where(iou <= iou_threshold)[0]
        order = order[remaining + 1]

    return selected_indices

def process_detections(output_data, class_data, scores_data, original_width, original_height, category_index, confidence_threshold=0.5, iou_threshold=0.5):
    try:
        # Convert outputs to NumPy arrays for vectorized operations
        boxes = np.array(output_data[0])
        scores = np.array(scores_data[0])
        classes = np.array(class_data[0], dtype=int)

        # Filter detections by confidence threshold
        valid_indices = scores >= confidence_threshold
        boxes = boxes[valid_indices]
        scores = scores[valid_indices]
        classes = classes[valid_indices]

        # Scale bounding box coordinates to the original image size
        boxes[:, [0, 2]] *= original_height
        boxes[:, [1, 3]] *= original_width
        boxes = boxes.astype(int)

        # Apply Non-Maximum Suppression
        selected_indices = non_max_suppression(boxes, scores, iou_threshold)
        boxes = boxes[selected_indices]
        scores = scores[selected_indices]
        classes = classes[selected_indices]

        # Prepare detections for output
        detections = [
            {
                "ymin": int(box[0]),
                "xmin": int(box[1]),
                "ymax": int(box[2]),
                "xmax": int(box[3]),
                "label": category_index.get(cls, {"name": "unknown"})["name"],
                "confidence": float(score)
            }
            for box, cls, score in zip(boxes, classes, scores)
        ]

        return detections

    except Exception as e:
        print(f"Error in process_detections: {str(e)}")
        return []
