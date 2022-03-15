
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow,
                             QFileDialog, QTextEdit)
from PyQt5.uic import loadUiType

from os import path, mkdir

MAIN_CLASS, _ = loadUiType(path.join(path.dirname(__file__), 'fc.ui'))


class MainWindow(QMainWindow, MAIN_CLASS):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QMainWindow.__init__(self)

        self.setupUi(self)
        self.setWindowTitle('TxT Maker')

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')


        self.save.clicked.connect(self.grabAndSave)

    def grabAndSave(self):

        filter = "TXT (*.txt)"
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        names = file_name.getOpenFileNames(self, "Open files", None, filter)
        print(names)

        if not names:
            return

        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File')
        self.statusbar.showMessage(f"Selected {file_name}")
        if not file_name:
            return

        buffer_text = ""
        for i in names[0]:
            with open(i, 'r') as f:
                text = f.read()
                buffer_text += text

        if path.exists(file_name):
            return

        with open(file_name, 'w') as f:
            f.write(buffer_text)

        self.statusbar.showMessage(f"Saved to {file_name}")


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
