from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence


class HotkeyManager:
    def __init__(self):
        self.hotkeys = {
            "undo": "Ctrl+Z",
            "redo": "Ctrl+Y",
            "save": "Ctrl+S",
            "next_image": "Right",
            "prev_image": "Left",
            "toggle_drawing_mode": "Ctrl+D",
            "toggle_eraser_mode": "Ctrl+E"
        }

    def get_hotkey(self, action):
        return self.hotkeys.get(action, None)

    def set_hotkey(self, action, new_hotkey):
        if action in self.hotkeys:
            self.hotkeys[action] = new_hotkey

    def apply_hotkeys(self, parent_widget):
        parent_widget.shortcut_undo = QShortcut(QKeySequence(self.hotkeys["undo"]), parent_widget)
        parent_widget.shortcut_undo.activated.connect(parent_widget.undo)

        parent_widget.shortcut_save = QShortcut(QKeySequence(self.hotkeys["save"]), parent_widget)
        parent_widget.shortcut_save.activated.connect(parent_widget.save_annotations)
