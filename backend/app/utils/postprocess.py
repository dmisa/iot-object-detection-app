import numpy as np
import tensorflow as tf

def process_detections(output_data, class_data, scores_data, original_width, original_height, category_index, confidence_threshold=0.5, iou_threshold=0.5):
    # Prepare data for NMS
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
    nms_results = tf.image.combined_non_max_suppression(
        boxes=boxes,
        scores=scores,
        max_output_size_per_class=num_detections,
        max_total_size=num_detections,
        iou_threshold=iou_threshold,
        score_threshold=confidence_threshold,
        pad_per_class=False,
        clip_boxes=False
    )

    # Extract valid detections
    valid_detections = int(nms_results.valid_detections[0].numpy())
    nms_boxes = nms_results.nmsed_boxes[0].numpy()[:valid_detections]
    nms_classes = nms_results.nmsed_classes[0].numpy().astype(np.int64)[:valid_detections]
    nms_scores = nms_results.nmsed_scores[0].numpy()[:valid_detections]

    # Convert NMS results to the desired format
    detections = []
    for i in range(valid_detections):
        ymin, xmin, ymax, xmax = nms_boxes[i]
        ymin = int(ymin * original_height)
        xmin = int(xmin * original_width)
        ymax = int(ymax * original_height)
        xmax = int(xmax * original_width)

        class_index = nms_classes[i]
        confidence = float(nms_scores[i])  # Convert to standard Python float
        label = category_index[class_index]['name'] if class_index in category_index else "unknown"

        detections.append({
            "ymin": ymin,
            "xmin": xmin,
            "ymax": ymax,
            "xmax": xmax,
            "label": label,
            "confidence": confidence  # Ensure this is a Python float
        })

    return detections