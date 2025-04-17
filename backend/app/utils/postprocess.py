import numpy as np

def non_max_suppression(boxes, scores, iou_threshold, score_threshold):
    # Convert to NumPy arrays if necessary
    boxes = np.array(boxes)
    scores = np.array(scores)

    # Initialize a list to keep track of the selected indices
    selected_indices = []

    # Sort the boxes by their confidence scores (in descending order)
    sorted_indices = np.argsort(scores)[::-1]

    while len(sorted_indices) > 0:
        # Pick the box with the highest score and remove it from the list
        current_index = sorted_indices[0]
        selected_indices.append(current_index)
        sorted_indices = sorted_indices[1:]

        # Get the coordinates of the picked box
        box = boxes[current_index]
        x1, y1, x2, y2 = box

        # Calculate the area of the picked box
        box_area = (x2 - x1) * (y2 - y1)

        # Calculate the intersection-over-union (IoU) for the remaining boxes
        remaining_boxes = boxes[sorted_indices]
        xx1 = np.maximum(x1, remaining_boxes[:, 0])
        yy1 = np.maximum(y1, remaining_boxes[:, 1])
        xx2 = np.minimum(x2, remaining_boxes[:, 2])
        yy2 = np.minimum(y2, remaining_boxes[:, 3])

        # Calculate intersection area
        intersection_width = np.maximum(0, xx2 - xx1)
        intersection_height = np.maximum(0, yy2 - yy1)
        intersection_area = intersection_width * intersection_height

        # Calculate union area
        remaining_boxes_area = (remaining_boxes[:, 2] - remaining_boxes[:, 0]) * (remaining_boxes[:, 3] - remaining_boxes[:, 1])
        union_area = box_area + remaining_boxes_area - intersection_area

        if(union_area == 0).all():
            break
        # Calculate IoU
        iou = np.where(union_area > 0, intersection_area / union_area, 0)

        # Keep only the boxes with IoU less than the threshold
        keep_indices = np.where(iou <= iou_threshold)[0]

        # Update the sorted indices
        sorted_indices = sorted_indices[keep_indices]

    return selected_indices

def process_detections(output_data, class_data, scores_data, original_width, original_height, category_index, confidence_threshold=0.5, iou_threshold=0.5):
    try:
        num_detections = len(output_data[0])  # Assuming batch size of 1
        boxes = np.zeros([1, num_detections, len(category_index), 4])  # Shape: [batch_size, num_boxes, num_classes, 4]
        scores = np.zeros([1, num_detections, len(category_index)])  # Shape: [batch_size, num_boxes, num_classes]

        for i in range(num_detections):
            ymin, xmin, ymax, xmax = output_data[0][i]
            class_index = int(class_data[0][i])
            confidence = float(scores_data[0][i])

            # Skip low-confidence detections
            if confidence < confidence_threshold:
                continue

            # Scale bounding box coordinates to the original image size
            ymin = max(0, ymin)
            xmin = max(0, xmin)
            ymax = min(1, ymax)
            xmax = min(1, xmax)

            # Assign the box and score to the appropriate class
            boxes[0, i, class_index, :] = [ymin, xmin, ymax, xmax]
            scores[0, i, class_index] = confidence

        # Apply Non-Maximum Suppression
        selected_indices = non_max_suppression(boxes[0].reshape(-1, 4), scores[0].reshape(-1), iou_threshold, confidence_threshold)

        # Extract valid detections
        detections = []
        for index in selected_indices:
            class_index = index % len(category_index)
            ymin, xmin, ymax, xmax = boxes[0].reshape(-1, 4)[index]

            ymin = int(ymin * original_height)
            xmin = int(xmin * original_width)
            ymax = int(ymax * original_height)
            xmax = int(xmax * original_width)

            confidence = float(scores[0].reshape(-1)[index])  # Convert to standard Python float
            label = category_index.get(class_index, {"name": "unknown"})['name']

            detections.append({
                "ymin": ymin,
                "xmin": xmin,
                "ymax": ymax,
                "xmax": xmax,
                "label": label,
                "confidence": confidence  # Ensure this is a Python float
            })

        return detections

    except Exception as e:
        print(f"Error in process_detections: {str(e)}")
        return []
