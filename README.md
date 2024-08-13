### README.md

# AnnoTool

## Overview
The AnnoTool is a Python-based graphical user interface (GUI) application designed to facilitate the annotation and labeling of images and videos for object detection tasks. The tool supports a variety of models including YOLOv8 models and custom models.

## Features
- **Image and Video Annotation**: Annotate images and videos with bounding boxes, segmentation masks, and oriented bounding boxes.
- **Model Integration**: Supports YOLOv8 models and allows custom models to be loaded for predictions.
- **Zoom and Pan**: Navigate large images and videos with zoom and pan capabilities.
- **Undo/Redo Functionality**: Easily undo or redo annotation actions.
- **Multiple Annotation Modes**: Switch between detection.
- **Customizable UI**: Users can pick colors for annotations, adjust brush sizes, and use various drawing tools like polygon, circle, and brush.
- **Annotation Saving**: Save annotations in a text file with the corresponding image or video frame.
- **Keyboard Shortcuts**: Quick access to functionalities via keyboard shortcuts.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/jaicdev/AnnoTool.git
   cd AnnoTool
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. **Load Data**: Use the "Load Files" button to select images or videos for annotation.
2. **Select Mode**: Choose the mode (Detect, Segment, OBB) using the dropdown menu.
3. **Annotate**: Use the canvas to draw bounding boxes, segmentation masks, or oriented bounding boxes.
4. **Save Annotations**: After annotating, click the "Save Annotations" button to save your work.
5. **Navigation**: Use the "Next" and "Previous" buttons to navigate through frames or images.

## Keyboard Shortcuts
- `Ctrl+Z`: Undo the last action.
- `Ctrl+Y`: Redo the last undone action.
- `Right Arrow`: Move to the next frame/image.
- `Left Arrow`: Move to the previous frame/image.
- `Ctrl+S`: Save annotations.
- `Ctrl+D`: Toggle drawing segment mode.
- `Ctrl+E`: Toggle eraser mode.
- `Ctrl+V`: Verify the current annotation.
- `Ctrl+A`: Select all files in a directory.

## File Structure
- **main.py**: Entry point of the application.
- **annotation_tool.py**: Contains the core logic for the annotation tool.
- **ui_setup.py**: Handles the setup and configuration of the UI components.
- **model_management.py**: Manages loading and interacting with YOLO models.
- **image_handling.py**: Provides functions for handling images and video frames.
- **file_management.py**: Manages file selection, loading, and saving operations.
- **canvas_operations.py**: Handles drawing operations on the canvas including zoom, pan, and annotation rendering.
- **utils.py**: Contains utility functions such as progress display.

## Contributing
Contributions are welcome! Please fork this repository and submit a pull request for any features, fixes, or improvements.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
