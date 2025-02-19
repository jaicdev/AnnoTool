import sys
import os
import copy
import cv2
import numpy as np
import torch
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QScrollArea, QWidget, QMessageBox, QLabel, QFileDialog, QShortcut
)
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QKeySequence

# ------------------------------------------
# canvas_operations.py (AnnotationCanvas)
# ------------------------------------------
class AnnotationCanvas(QLabel):
    def __init__(self):
        super().__init__()
        self.setScaledContents(True)
        # Use a layers dictionary for annotations
        self.layers = {"default": []}
        self.current_layer = "default"
        self.current_image = None

        # Variables for drawing
        self.drawing_mode = None  # "bbox" or "mask"
        self.start_point = None
        self.end_point = None
        self.mask_points = []

    def load_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from path: {image_path}")

        if len(image.shape) == 2:
            h, w = image.shape
            qt_image = QImage(image.data, w, h, w, QImage.Format_Grayscale8)
        elif len(image.shape) == 3 and image.shape[2] == 3:
            h, w, ch = image.shape
            bytes_per_line = ch * w
            qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_BGR888)
        else:
            raise ValueError("Unsupported image format. Expected grayscale or BGR color format.")

        self.current_image = qt_image
        pixmap = QPixmap.fromImage(self.current_image)
        self.setPixmap(pixmap)
        self.adjustSize()

    def paintEvent(self, event):
        super().paintEvent(event)

        if not self.current_image:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw existing annotations from the current layer
        for annotation in self.layers.get(self.current_layer, []):
            try:
                self.draw_annotation(painter, annotation)
            except ValueError as e:
                print(f"Error drawing annotation: {e}")

        # Draw in-progress annotation if drawing
        if self.drawing_mode == "bbox" and self.start_point and self.end_point:
            pen = QPen(QColor(0, 255, 255), 2, Qt.DashLine)
            painter.setPen(pen)
            rect = QRect(self.start_point, self.end_point).normalized()
            painter.drawRect(rect)
        elif self.drawing_mode == "mask" and self.mask_points:
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)
            for i in range(1, len(self.mask_points)):
                painter.drawLine(self.mask_points[i - 1], self.mask_points[i])
        painter.end()

    def draw_annotation(self, painter, annotation):
        if "type" not in annotation:
            raise ValueError("Annotation must have a 'type' key.")
        annotation_type = annotation["type"]

        if annotation_type == "bbox":
            self._draw_bbox(painter, annotation["coords"])
        elif annotation_type == "mask":
            # Draw mask as connected points (or use polyline if desired)
            points = [QPoint(int(pt[0]), int(pt[1])) for pt in annotation["coords"]]
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)
            if points:
                painter.drawPolyline(*points)
        else:
            raise ValueError(f"Unsupported annotation type: {annotation_type}")

    def _draw_bbox(self, painter, coords):
        # Convert coordinates to integers
        x, y, w, h = map(int, coords)
        pen = QPen(QColor(0, 255, 0), 2)
        painter.setPen(pen)
        painter.drawRect(x, y, w, h)

    def set_annotations(self, annotations):
        if not isinstance(annotations, list):
            raise ValueError("Annotations must be a list.")
        self.layers[self.current_layer] = annotations
        self.update()

    def get_annotations(self):
        return self.layers.get(self.current_layer, [])

    def add_layer(self, layer_name):
        if layer_name in self.layers:
            raise ValueError(f"Layer {layer_name} already exists.")
        self.layers[layer_name] = []

    def switch_layer(self, layer_name):
        if layer_name not in self.layers:
            raise ValueError(f"Layer {layer_name} does not exist.")
        self.current_layer = layer_name
        self.update()

    # Mouse events integrated for drawing
    def mousePressEvent(self, event):
        if self.drawing_mode == "bbox" and event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = event.pos()
        elif self.drawing_mode == "mask" and event.button() == Qt.LeftButton:
            self.mask_points = [event.pos()]
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drawing_mode == "bbox" and self.start_point:
            self.end_point = event.pos()
            self.update()
        elif self.drawing_mode == "mask" and event.buttons() & Qt.LeftButton:
            self.mask_points.append(event.pos())
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.drawing_mode == "bbox" and self.start_point and event.button() == Qt.LeftButton:
            rect = QRect(self.start_point, event.pos()).normalized()
            annotation = {
                "type": "bbox",
                "coords": [rect.x(), rect.y(), rect.width(), rect.height()]
            }
            self.layers[self.current_layer].append(annotation)
            self.start_point = None
            self.end_point = None
            self.update()
        elif self.drawing_mode == "mask" and self.mask_points:
            annotation = {
                "type": "mask",
                "coords": [(p.x(), p.y()) for p in self.mask_points]
            }
            self.layers[self.current_layer].append(annotation)
            self.mask_points = []
            self.update()
        super().mouseReleaseEvent(event)

    # Optional: A simple zoom method that resizes the widget
    def zoom(self, factor):
        if self.pixmap() is not None:
            new_width = self.pixmap().width() * factor
            new_height = self.pixmap().height() * factor
            self.resize(new_width, new_height)
