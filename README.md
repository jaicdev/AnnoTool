# AnnoTool - Comprehensive Image & Video Annotation

AnnoTool is a powerful, cross-platform annotation tool built with PyQt5. It supports comprehensive image and video annotation tasks, including drawing bounding boxes, masks, ellipses, cuboids, polygons, keypoints, and more. The tool also integrates deep learning models (e.g., YOLOv8) for auto-annotation, allowing users to quickly generate annotations on their images. Additional features include undo/redo functionality, layer management, multiple export formats (COCO, Pascal VOC, YOLO), and a statistics dashboard for analyzing annotation metrics.

---

## Features

- **Image & Video Annotation:**  
  Draw bounding boxes, masks, ellipses, cuboids, polygons, and keypoints on images.

- **Auto-Annotation:**  
  Utilize YOLO-based models to auto-generate annotations for faster workflows.

- **Undo/Redo Functionality:**  
  Easily revert and reapply changes during the annotation process.

- **Layer Management:**  
  Create, switch, and manage multiple layers to organize annotations.

- **Export Formats:**  
  Export annotations in popular formats including COCO, Pascal VOC, and YOLO.

- **Hotkey Support:**  
  Use customizable hotkeys for common actions like undo, save, and image navigation.

- **Annotation Validation:**  
  Validate annotation data and calculate annotation metrics for quality control.

- **Customizable:**  
  Extend functionality with custom drawing modes and fine-tuning of deep learning models.

---

## Prerequisites

- **Python 3.7+**
- **PyQt5:** For the GUI components.
- **OpenCV:** For image processing tasks.
- **NumPy:** For array manipulations.
- **Ultralytics YOLO:** For deep learning-based auto-annotation.
- **Torch:** Required for YOLO model operations.

You can install the required Python packages using pip:

```bash
pip install pyqt5 opencv-python numpy torch ultralytics
```

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/annotool.git
   cd annotool
   ```

2. **Install Dependencies:**

   Make sure you have installed all dependencies as listed in the [Prerequisites](#prerequisites) section.

3. **Download YOLO Models:**

   The tool uses YOLOv8 models for auto-annotation. Ensure you have the following models in your project directory or update the paths in the `ModelManager` class:
   - `yolov8s.pt`
   - `yolov8s-seg.pt`

---

## Usage

1. **Run the Application:**

   Execute the main script to start the application:

   ```bash
   python main.py
   ```

2. **Load Images:**

   - Click on the **"Load Files"** button to select a folder containing images.
   - The tool supports common image formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`.

3. **Navigation:**

   - Use **"Previous"** and **"Next"** buttons to navigate through the loaded images.

4. **Annotation Tools:**

   - **Draw BBox:** Click the **"Draw BBox"** button to activate bounding box drawing mode.
   - **Draw Mask:** Click the **"Draw Mask"** button to activate segmentation mask drawing mode.
   - Use mouse events to draw and adjust annotations on the image canvas.

5. **Auto-Annotate:**

   - Select a model from the dropdown menu.
   - Click **"Auto-Annotate"** to generate annotations automatically using the selected deep learning model.

6. **Undo/Redo:**

   - Use **"Undo"** and **"Redo"** buttons (or hotkeys) to revert or reapply annotation changes.

7. **Save Annotations:**

   - Click **"Save Annotations"** to export your annotations. Files are saved in a structured folder alongside the images.

8. **Export Formats:**

   - Use the export functionalities to convert your annotations to COCO, Pascal VOC, or YOLO format as needed.

9. **Statistics Dashboard:**

   - A statistics dashboard is available to review annotation metrics, such as class distribution.

---

## Folder Structure

```plaintext
annotool/
├── annotation_tool.py      # Main application entry point
├── canvas_operations.py    # Canvas widget and drawing functionality
├── drawing_functions.py    # Drawing modes (bbox, mask, etc.)
├── file_management.py      # File handling and image navigation
├── hotkeys.py              # Hotkey management for quick actions
├── model_management.py     # YOLO model integration and auto-annotation
├── class_management.py     # Class definitions and color mappings
├── validation_tools.py     # Annotation validation and metrics calculations
├── export_formats.py       # Functions to export annotations in various formats
├── README.md               # This README file
└── requirements.txt        # List of required Python packages (optional)
```

---

## Acknowledgements

- **Ultralytics:**  
  A special thanks to Ultralytics for developing the YOLOv8 models which power the auto-annotation feature of AnnoTool. Their contributions to the computer vision community are greatly appreciated.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with clear commit messages.
4. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Happy Annotating!
