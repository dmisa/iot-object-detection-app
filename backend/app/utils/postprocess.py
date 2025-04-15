def process_detections(output_data, class_data, scores_data, original_width, original_height, category_index, confidence_threshold=0.5):
    detections = []
    for i, detection in enumerate(output_data[0]):  # Assuming batch size of 1
        ymin, xmin, ymax, xmax = detection
        ymin = max(0, int(ymin * original_height))
        xmin = max(0, int(xmin * original_width))
        ymax = min(original_height, int(ymax * original_height))
        xmax = min(original_width, int(xmax * original_width))

        class_index = int(class_data[0][i])
        confidence = float(scores_data[0][i])

        if confidence < confidence_threshold:
            continue

        label = category_index[class_index]['name'] if class_index in category_index else "unknown"
        detections.append({
            "ymin": ymin,
            "xmin": xmin,
            "ymax": ymax,
            "xmax": xmax,
            "label": label,
            "confidence": confidence
        })
    return detections