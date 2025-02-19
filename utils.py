def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def format_bbox(x, y, w, h):
    return f"{x},{y},{w},{h}"

def compute_iou(box1, box2):
    # Intersection over Union calculation
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[0] + box1[2], box2[0] + box2[2])
    y2 = min(box1[1] + box1[3], box2[1] + box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    union = box1[2] * box1[3] + box2[2] * box2[3] - intersection
    return intersection / union if union > 0 else 0

