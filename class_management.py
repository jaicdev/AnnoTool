class ClassManager:
    def __init__(self):
        self.classes = ["Person", "Car", "Bicycle", "Dog"]
        self.class_colors = {
            "Person": (255, 0, 0),
            "Car": (0, 255, 0),
            "Bicycle": (0, 0, 255),
            "Dog": (255, 255, 0)
        }

    def get_classes(self):
        return self.classes

    def get_color_for_class(self, class_name):
        return self.class_colors.get(class_name, (255, 255, 255))

    def add_class(self, class_name, color):
        if class_name not in self.classes:
            self.classes.append(class_name)
            self.class_colors[class_name] = color
