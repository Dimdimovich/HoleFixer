import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QFileDialog
from tools import stlProcessor


def center(widget):
    qr = widget.frameGeometry()
    if widget.parent() is not None:
        cp = widget.parent().frameGeometry().center()
        cp -= widget.parent().frameGeometry().topLeft()
    else:
        cp = widget.screen().availableGeometry().center()
    qr.moveCenter(cp)
    widget.move(qr.topLeft())


def create_window() -> QWidget:
    # create a new widget
    window = QWidget()
    # assign a title
    window.setWindowTitle("Chose an stl file to start")
    # set its size
    window.setGeometry(100, 100, 280, 80)
    # put in on the center of the screen
    center(window)
    return window


class STLLoaderWindow:
    def __init__(self):
        # create application
        self.app = QApplication([])

        # create the main window
        self.window = create_window()

        # add the stl button
        self.button = self.add_button()

        self.window.show()
        sys.exit(self.app.exec())

    def add_button(self) -> QPushButton:
        """

        :rtype: QPushButton
        """
        # create a button with STL title
        button = QPushButton("STL", parent=self.window)
        # set its size
        button.setGeometry(50, 50, 140, 40)
        # put in on the center of the main window
        center(button)
        button.clicked.connect(self.on_click)
        return button

    def on_click(self):
        # arise file dialog to choose an .stl file
        file_name = QFileDialog.getOpenFileName(
            parent=self.window,
            caption="Open file",
            filter="*.stl"
        )
        # process the file repairing procedure
        if file_name[0] != '':
            # hide the main window
            self.window.hide()
            # run processing
            stlProcessor.STLProcessor(file_name[0])
            # show the main window after processing
            self.window.show()
