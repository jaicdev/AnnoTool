
import torch
from ultralytics import YOLO

class ModelManager:
    def __init__(self):
        self.models = {
            "YOLOv8 Detection": "yolov8s.pt",
            "YOLOv8 Segmentation": "yolov8s-seg.pt",
            "Custom Model": None,
        }
        self.current_model = None  # Initialize as None

    def get_available_models(self):
        return list(self.models.keys())

    def set_current_model(self, model_name):
        if model_name in self.models and self.models[model_name]:
            model_path = self.models[model_name]
            try:
                self.current_model = YOLO(model_path).to("cuda" if torch.cuda.is_available() else "cpu")
                print(f"Model {model_name} loaded successfully.")
            except Exception as e:
                print(f"Error loading model {model_name}: {e}")
                self.current_model = None

    def get_model(self):
        return self.current_model

    def batch_annotate(self, image_paths):
        results = []
        if not self.current_model:
            print("No model is currently loaded. Cannot annotate images.")
            return results
        for image_path in image_paths:
            results.append(self.current_model.predict(image_path))
        return results

    def fine_tune_model(self, training_data, output_path):
        # Placeholder for fine-tuning logic
        print("Fine-tuning model with provided training data...")
        # Implement fine-tuning logic here
