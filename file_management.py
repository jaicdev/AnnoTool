import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class FileManager:
    def __init__(self):
        self.files = []
        self.index = -1

    def browse_and_load_files(self):
        # Open a dialog for the user to select a folder
        folder = QFileDialog.getExistingDirectory(None, "Select Folder", "")
        if not folder:
            QMessageBox.warning(None, "No Folder Selected", "Please select a valid folder containing images.")
            self.files = []
            self.index = -1
            return []

        # Filter for image files in the selected folder
        exts = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
        try:
            self.files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(exts)]
            self.index = 0 if self.files else -1
            if not self.files:
                QMessageBox.warning(None, "No Images Found", "No supported image files found in the selected folder.")
        except Exception as e:
            QMessageBox.critical(None, "Error Loading Files", f"An error occurred while loading files: {str(e)}")
            self.files = []
            self.index = -1

        return self.files

    def get_current_image(self):
        if self.index < 0 or self.index >= len(self.files):
            QMessageBox.warning(None, "No Image Available", "No image is currently loaded.")
            return None
        return self.files[self.index]

    def get_next_image(self):
        if self.index < len(self.files) - 1:
            self.index += 1
            return self.get_current_image()
        QMessageBox.information(None, "No More Images", "You have reached the last image.")
        return None

    def get_previous_image(self):
        if self.index > 0:
            self.index -= 1
            return self.get_current_image()
        QMessageBox.information(None, "No More Images", "You are at the first image.")
        return None

    def save_annotations(self, annotations):
        if self.index == -1 or not self.files:
            QMessageBox.warning(None, "No Image Selected", "Please select an image before saving annotations.")
            return False

        # Use a structured naming convention for annotation files
        image_path = self.files[self.index]
        annotation_filename = os.path.splitext(os.path.basename(image_path))[0] + "_annotations.txt"
        annotations_dir = os.path.join(os.path.dirname(image_path), "annotations")
        os.makedirs(annotations_dir, exist_ok=True)
        anno_path = os.path.join(annotations_dir, annotation_filename)

        try:
            with open(anno_path, "w") as f:
                for anno in annotations:
                    f.write(f"{anno}\n")
            QMessageBox.information(None, "Success", f"Annotations saved successfully: {anno_path}")
            return True
        except Exception as e:
            QMessageBox.critical(None, "Error Saving Annotations", f"Failed to save annotations: {str(e)}")
            return False

