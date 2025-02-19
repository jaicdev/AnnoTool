from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor

class DrawingFunctions:

    @staticmethod
    def enable_bbox_drawing(canvas):
        canvas.drawing_mode = "bbox"
        canvas.start_point = None
        canvas.end_point = None

    @staticmethod
    def enable_mask_drawing(canvas):
        canvas.drawing_mode = "mask"
        canvas.mask_points = []

    @staticmethod
    def mousePressEvent(event, canvas):
        if canvas.drawing_mode == "bbox" and event.button() == Qt.LeftButton:
            canvas.start_point = event.pos()
        elif canvas.drawing_mode == "mask" and event.button() == Qt.LeftButton:
            canvas.mask_points = [event.pos()]

    @staticmethod
    def mouseMoveEvent(event, canvas):
        if canvas.drawing_mode == "bbox" and canvas.start_point:
            canvas.end_point = event.pos()
            canvas.update()
        elif canvas.drawing_mode == "mask" and event.buttons() & Qt.LeftButton:
            canvas.mask_points.append(event.pos())
            canvas.update()

    @staticmethod
    def mouseReleaseEvent(event, canvas):
        if canvas.drawing_mode == "bbox" and canvas.start_point and event.button() == Qt.LeftButton:
            rect = QRect(canvas.start_point, event.pos()).normalized()
            canvas.annotations.append({
                "type": "bbox",
                "coords": [rect.x(), rect.y(), rect.width(), rect.height()]
            })
            canvas.start_point = None
            canvas.end_point = None
            canvas.update()
        elif canvas.drawing_mode == "mask" and canvas.mask_points:
            canvas.annotations.append({
                "type": "mask",
                "coords": [(p.x(), p.y()) for p in canvas.mask_points]
            })
            canvas.mask_points = []
            canvas.update()

    @staticmethod
    def paintEvent(event, canvas):
        painter = QPainter(canvas)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw existing annotations
        for annotation in canvas.annotations:
            if annotation["type"] == "bbox":
                x, y, w, h = annotation["coords"]
                pen = QPen(QColor(0, 255, 0), 2)
                painter.setPen(pen)
                painter.drawRect(x, y, w, h)
            elif annotation["type"] == "mask":
                points = [QRect(p[0], p[1], 2, 2) for p in annotation["coords"]]
                pen = QPen(QColor(255, 0, 0), 2)
                painter.setPen(pen)
                for point in points:
                    painter.drawEllipse(point)

        # Draw in-progress bounding box
        if canvas.drawing_mode == "bbox" and canvas.start_point and canvas.end_point:
            pen = QPen(QColor(0, 255, 255), 2, Qt.DashLine)
            painter.setPen(pen)
            rect = QRect(canvas.start_point, canvas.end_point).normalized()
            painter.drawRect(rect)

        # Draw in-progress mask
        if canvas.drawing_mode == "mask" and canvas.mask_points:
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)
            for i in range(1, len(canvas.mask_points)):
                painter.drawLine(canvas.mask_points[i - 1], canvas.mask_points[i])

        painter.end()

