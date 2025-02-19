
import sys
from PyQt5.QtWidgets import QApplication
from annotation_tool import AnnotationTool

def main():
    try:
        app = QApplication(sys.argv)
        window = AnnotationTool()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
