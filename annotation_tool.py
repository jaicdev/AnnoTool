from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QScrollArea, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QRect
from canvas_operations import AnnotationCanvas
from file_management import FileManager
from model_management import ModelManager
from hotkeys import HotkeyManager
from class_management import ClassManager
from validation_tools import Validator
from drawing_functions import DrawingFunctions
import copy
import cv2

class AnnotationTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AnnoTool - Comprehensive Image & Video Annotation")

        # Managers
        self.file_manager = FileManager()
        self.model_manager = ModelManager()
        self.hotkey_manager = HotkeyManager()
        self.class_manager = ClassManager()
        self.validator = Validator()

        # Annotation canvas
        self.canvas = AnnotationCanvas()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.canvas)
        self.scroll_area.setWidgetResizable(True)

        # Undo/Redo stacks
        self.undo_stack = []
        self.redo_stack = []

        # Setup UI
        self.init_ui()

    def init_ui(self):
        top_layout = QHBoxLayout()

        # Buttons and dropdowns
        self.btn_load_files = QPushButton("Load Files")
        self.btn_load_files.clicked.connect(self.load_files)
        top_layout.addWidget(self.btn_load_files)

        self.btn_prev = QPushButton("Previous")
        self.btn_prev.clicked.connect(self.show_previous)
        top_layout.addWidget(self.btn_prev)

        self.btn_next = QPushButton("Next")
        self.btn_next.clicked.connect(self.show_next)
        top_layout.addWidget(self.btn_next)

        self.btn_save = QPushButton("Save Annotations")
        self.btn_save.clicked.connect(self.save_annotations)
        top_layout.addWidget(self.btn_save)

        self.model_dropdown = QComboBox()
        self.model_dropdown.addItems(self.model_manager.get_available_models())
        self.model_dropdown.currentIndexChanged.connect(self.change_model)
        top_layout.addWidget(self.model_dropdown)

        self.btn_auto_annotate = QPushButton("Auto-Annotate")
        self.btn_auto_annotate.clicked.connect(self.auto_annotate)
        top_layout.addWidget(self.btn_auto_annotate)

        self.btn_draw_bbox = QPushButton("Draw BBox")
        self.btn_draw_bbox.clicked.connect(self.activate_draw_bbox)
        top_layout.addWidget(self.btn_draw_bbox)

        self.btn_draw_mask = QPushButton("Draw Mask")
        self.btn_draw_mask.clicked.connect(self.activate_draw_mask)
        top_layout.addWidget(self.btn_draw_mask)

        self.btn_validate = QPushButton("Validate Annotations")
        self.btn_validate.clicked.connect(self.validate_annotations)
        top_layout.addWidget(self.btn_validate)

        self.btn_undo = QPushButton("Undo")
        self.btn_undo.clicked.connect(self.undo)
        top_layout.addWidget(self.btn_undo)

        self.btn_redo = QPushButton("Redo")
        self.btn_redo.clicked.connect(self.redo)
        top_layout.addWidget(self.btn_redo)

        self.btn_zoom_in = QPushButton("Zoom In")
        self.btn_zoom_in.clicked.connect(self.zoom_in)
        top_layout.addWidget(self.btn_zoom_in)

        self.btn_zoom_out = QPushButton("Zoom Out")
        self.btn_zoom_out.clicked.connect(self.zoom_out)
        top_layout.addWidget(self.btn_zoom_out)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.scroll_area)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Load hotkeys and apply them to the main window
        self.hotkey_manager.apply_hotkeys(self)

    def push_undo(self):
        self.undo_stack.append(copy.deepcopy(self.canvas.get_annotations()))
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(copy.deepcopy(self.canvas.get_annotations()))
            self.canvas.set_annotations(self.undo_stack.pop())

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(copy.deepcopy(self.canvas.get_annotations()))
            self.canvas.set_annotations(self.redo_stack.pop())

    def load_files(self):
        files = self.file_manager.browse_and_load_files()
        if not files:
            QMessageBox.warning(self, "Error", "No files loaded.")
            return
        if files:
            self.push_undo()
            self.canvas.load_image(self.preprocess_image(self.file_manager.get_current_image()))
            self.adjust_canvas_size()

    def preprocess_image(self, image_path):
        """Resize the image to 640x640 before loading."""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from path: {image_path}")

        resized_image = cv2.resize(image, (640, 640))
        temp_path = "resized_image.jpg"
        cv2.imwrite(temp_path, resized_image)
        return temp_path

    def adjust_canvas_size(self):
        current_image = self.canvas.current_image
        if current_image:
            self.canvas.resize(640, 640)

    def show_previous(self):
        image = self.file_manager.get_previous_image()
        if image:
            self.push_undo()
            self.canvas.load_image(self.preprocess_image(image))
            self.adjust_canvas_size()

    def show_next(self):
        image = self.file_manager.get_next_image()
        if image:
            self.push_undo()
            self.canvas.load_image(self.preprocess_image(image))
            self.adjust_canvas_size()

    def save_annotations(self):
        annotations = self.canvas.get_annotations()
        if not annotations:
            QMessageBox.warning(self, "Error", "No annotations to save.")
            return

        if self.file_manager.save_annotations(annotations):
            QMessageBox.information(self, "Success", "Annotations saved successfully!")
        else:
            QMessageBox.warning(self, "Error", "Failed to save annotations.")

    def change_model(self):
        selected_model = self.model_dropdown.currentText()
        self.model_manager.set_current_model(selected_model)

    def auto_annotate(self):
        model = self.model_manager.get_model()
        if not model:
            QMessageBox.warning(self, "Error", "No model selected or model failed to load.")
            return

        image = self.canvas.get_current_image()
        if image is None:
            QMessageBox.warning(self, "Error", "No image loaded.")
            return

        self.push_undo()

        # Run model prediction
        results = model.predict(image)

        # Normalize predictions for bounding boxes and segmentation masks
        annotations = []
        for result in results:
            # Process bounding boxes
            for box in result.boxes:  # Assuming result.boxes contains bounding box data
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # Convert to integers
                cls = int(box.cls[0])  # Class ID
                annotations.append({
                    "type": "bbox",
                    "coords": [x1, y1, x2 - x1, y2 - y1],  # Convert to [x, y, width, height]
                    "class": cls
                })

            # Process segmentation masks (if available)
            if result.masks:
                for mask, cls in zip(result.masks.data, result.boxes.cls):
                    annotations.append({
                        "type": "mask",
                        "mask": mask.cpu().numpy(),  # Convert to NumPy array
                        "class": int(cls)
                    })

        print(f"Annotations: {annotations}")  # Debugging log
        self.canvas.set_annotations(annotations)

    def activate_draw_bbox(self):
        QMessageBox.information(self, "Draw BBox", "Tool to draw bounding boxes activated!")
        DrawingFunctions.enable_bbox_drawing(self.canvas)

    def activate_draw_mask(self):
        QMessageBox.information(self, "Draw Mask", "Tool to draw segmentation masks activated!")
        DrawingFunctions.enable_mask_drawing(self.canvas)

    def zoom_in(self):
        self.canvas.scale(1.2, 1.2)

    def zoom_out(self):
        self.canvas.scale(0.8, 0.8)

    def validate_annotations(self):
        annotations = self.canvas.get_annotations()
        issues = self.validator.validate(annotations)
        if issues:
            QMessageBox.warning(self, "Validation Issues", "\n".join(issues))
        else:
            QMessageBox.information(self, "Validation", "All annotations are valid!")

    def setup_statistics_dashboard(self):
        stats_button = QPushButton("Show Stats")
        stats_button.clicked.connect(self.show_annotation_stats)
        self.layout().addWidget(stats_button)

    def show_annotation_stats(self):
        annotations = self.canvas.get_annotations()
        stats = self.validator.calculate_annotation_metrics(annotations)
        stats_str = "\n".join([f"{cls}: {count}" for cls, count in stats.items()])
        QMessageBox.information(self, "Annotation Statistics", stats_str)

