# validation_tools.py
class Validator:
    def __init__(self):
        pass

    def validate(self, annotations):
        issues = []
        for i, anno in enumerate(annotations):
            if "coords" not in anno or not anno["coords"]:
                issues.append(f"Annotation {i} has no coordinates.")
            if "class" not in anno:
                issues.append(f"Annotation {i} has no class assigned.")
            if anno.get("type") == "bbox":
                x, y, w, h = anno["coords"]
                if w <= 0 or h <= 0:
                    issues.append(f"Annotation {i} has invalid bbox dimensions.")
        return issues

    # Metrics Dashboard: now correctly counts annotations per class
    def calculate_annotation_metrics(self, annotations):
        metrics = {}
        for anno in annotations:
            cls = anno.get("class", "Unknown")
            metrics[cls] = metrics.get(cls, 0) + 1
        return metrics
