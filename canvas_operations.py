
import cv2
import numpy as np
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint

class AnnotationCanvas(QLabel):
    def __init__(self):
        super().__init__()
        self.setScaledContents(True)
        self.annotations = []
        self.current_image = None
        self.layers = {}
        self.current_layer = "default"
        self.layers[self.current_layer] = []

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

        for layer, annotations in self.layers.items():
            if layer == self.current_layer:  # Only draw the current layer
                for annotation in annotations:
                    try:
                        self.draw_annotation(painter, annotation)
                    except ValueError as e:
                        print(f"Error drawing annotation: {e}")
                        
    def _draw_bbox(self, painter, coords):
        # Convert coordinates to integers
        x, y, w, h = [int(c) for c in coords]
        pen = QPen(QColor(0, 255, 0), 2)
        painter.setPen(pen)
        painter.drawRect(x, y, w, h)



    def draw_annotation(self, painter, annotation):
        if "type" not in annotation or "coords" not in annotation:
            raise ValueError("Annotation must have 'type' and 'coords' keys.")

        annotation_type = annotation["type"]
        coords = annotation["coords"]

        if annotation_type == "bbox":
            self._draw_bbox(painter, coords)
        elif annotation_type == "ellipse":
            self._draw_ellipse(painter, coords)
        elif annotation_type == "cuboid":
            self._draw_cuboid(painter, coords)
        elif annotation_type == "polygon":
            self._draw_polygon(painter, coords)
        elif annotation_type == "keypoints":
            self._draw_keypoints(painter, coords)
        else:
            raise ValueError(f"Unsupported annotation type: {annotation_type}")

    def _draw_bbox(self, painter, coords):
        x, y, w, h = coords
        pen = QPen(QColor(0, 255, 0), 2)
        painter.setPen(pen)
        painter.drawRect(x, y, w, h)

    def _draw_ellipse(self, painter, coords):
        x, y, w, h = coords
        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)
        painter.drawEllipse(x, y, w, h)

    def _draw_cuboid(self, painter, coords):
        # Example implementation for 3D cuboid drawing
        # For simplicity, treating it as a 2D projection
        points = [QPoint(*coord) for coord in coords]
        pen = QPen(QColor(0, 0, 255), 2)
        painter.setPen(pen)
        for i in range(len(points)):
            painter.drawLine(points[i], points[(i + 1) % len(points)])

    def _draw_polygon(self, painter, coords):
        points = [QPoint(pt[0], pt[1]) for pt in coords]
        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)
        painter.drawPolygon(*points)

    def _draw_keypoints(self, painter, coords):
        pen = QPen(QColor(0, 0, 255), 2)
        painter.setPen(pen)
        for pt in coords:
            painter.drawEllipse(pt[0] - 2, pt[1] - 2, 4, 4)

    def set_annotations(self, annotations):
        if not isinstance(annotations, list):
            raise ValueError("Annotations must be a list.")
        self.layers[self.current_layer] = annotations
        self.update()

    def get_annotations(self):
        return self.layers[self.current_layer]

    def add_layer(self, layer_name):
        if layer_name in self.layers:
            raise ValueError(f"Layer {layer_name} already exists.")
        self.layers[layer_name] = []

    def switch_layer(self, layer_name):
        if layer_name not in self.layers:
            raise ValueError(f"Layer {layer_name} does not exist.")
        self.current_layer = layer_name
        self.update()

    def save_template(self, template_name):
        # Save current annotations as a template
        return {template_name: self.layers[self.current_layer]}

    def apply_template(self, template):
        # Apply a saved template to the current layer
        self.layers[self.current_layer].extend(template)
        self.update()

    def group_annotations(self, annotation_indices):
        # Group selected annotations (example implementation)
        grouped_annotations = [self.layers[self.current_layer][i] for i in annotation_indices]
        group = {"type": "group", "annotations": grouped_annotations}
        self.layers[self.current_layer] = [
            anno for i, anno in enumerate(self.layers[self.current_layer]) if i not in annotation_indices
        ]
        self.layers[self.current_layer].append(group)
        self.update()

    # New Methods for Advanced Annotations
    def _draw_polyline(self, painter, coords):
        pen = QPen(QColor(0, 255, 255), 2)
        painter.setPen(pen)
        points = [QPoint(pt[0], pt[1]) for pt in coords]
        painter.drawPolyline(*points)

    def _draw_segmentation_mask(self, painter, mask):
        overlay = QPixmap(self.size())
        overlay.fill(Qt.transparent)
        mask_painter = QPainter(overlay)
        mask_painter.setOpacity(0.5)
        mask_painter.fillRect(self.rect(), QColor(0, 255, 0, 127))
        mask_painter.end()
        painter.drawPixmap(self.rect(), overlay)
    
    def toggle_layer_visibility(self, layer_name):
        self.layers[layer_name]['visible'] = not self.layers[layer_name]['visible']
        self.update()

    def lock_layer(self, layer_name, lock_status=True):
        self.layers[layer_name]['locked'] = lock_status

    def reorder_layer(self, layer_name, new_index):
        keys = list(self.layers.keys())
        keys.remove(layer_name)
        keys.insert(new_index, layer_name)
        self.layers = {key: self.layers[key] for key in keys}

    def get_current_image(self):
        import numpy as np
        from PyQt5.QtGui import QImage
        import cv2

        if self.current_image is None:
            return None

        qimage = self.current_image
        width = qimage.width()
        height = qimage.height()

        try:
            # Log detailed information about the format
            print(f"QImage Format Code: {qimage.format()}, Byte Count: {qimage.byteCount()}")

            # Handle supported formats
            if qimage.format() == QImage.Format_RGB32:
                ptr = qimage.bits()
                ptr.setsize(qimage.byteCount())
                img = np.array(ptr, dtype=np.uint8).reshape((height, qimage.bytesPerLine() // 4, 4))
                img_bgr = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
                return img_bgr
            elif qimage.format() == QImage.Format_RGB888:
                ptr = qimage.bits()
                ptr.setsize(qimage.byteCount())
                img = np.array(ptr, dtype=np.uint8).reshape((height, qimage.bytesPerLine() // 3, 3))
                img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                return img_bgr
            elif qimage.format() == QImage.Format_Grayscale8:
                ptr = qimage.bits()
                ptr.setsize(qimage.byteCount())
                img = np.array(ptr, dtype=np.uint8).reshape((height, width))
                return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

            # Handle newer or uncommon formats (like Format_BGR30)
            elif qimage.format() == 29:  # Assuming Format_BGR30
                ptr = qimage.bits()
                ptr.setsize(qimage.byteCount())
                img = np.array(ptr, dtype=np.uint8).reshape((height, qimage.bytesPerLine() // 4, 4))
                return img[:, :, :3]  # Use only the first three channels

            # Log unsupported formats and raise error
            print(f"Unsupported QImage format: {qimage.format()}")
            raise ValueError("Unsupported QImage format. Please check the image format and ensure compatibility.")
        except Exception as e:
            print(f"Error during QImage conversion: {e}")
            raise
