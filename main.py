
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow,
                             QFileDialog, QTextEdit)
from PyQt5.uic import loadUiType

from os import path, mkdir

MAIN_CLASS, _ = loadUiType(path.join(path.dirname(__file__), 'gui.ui'))
TAB_CLASS, _ = loadUiType(path.join(path.dirname(__file__), 'tab.ui'))

class TabWidget(QWidget, TAB_CLASS):
    def __init__(self):
        super(TabWidget, self).__init__()
        QWidget.__init__(self)
        self.setupUi(self)

class MainWindow(QMainWindow, MAIN_CLASS):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QMainWindow.__init__(self)

        self.setupUi(self)
        self.setWindowTitle('TxT Maker')

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')


        self.nextButton.clicked.connect(self.nextFile)
        self.removeButton.clicked.connect(self.removeTab)
        self.PreButton.clicked.connect(self.preTab)
        self.saveAllbtn.clicked.connect(self.saveAll)
        self.clearbtn.clicked.connect(self.clearAll)

    def saveAll(self):
        current = self.controlerTab.currentIndex()
        count = self.controlerTab.count()
        prefixText = str(self.prefixline.text())
        if count > 0 and prefixText != "":
            dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

            if dir:
                output_dir = path.join(dir, prefixText)
                if path.exists(output_dir):
                    print("Already Exist")

                else:
                    mkdir(output_dir)
                    print(f"Directory {output_dir} created.")
            else:
                return


            for i in range(0, count):
                tab_text = self.controlerTab.tabText(i)
                file_name = path.join(output_dir, f"{prefixText}_{tab_text}.txt")
                print(file_name)
                current_text_widget = self.controlerTab.widget(i).findChild(QTextEdit, "textEdit")
                current_tab_text =  current_text_widget.toPlainText()

                with open(file_name, 'w') as f:
                    f.write(current_tab_text)
                    self.statusbar.clearMessage()
                    self.statusbar.showMessage(f"Saving {tab_text}", 100)

            self.statusbar.showMessage(f"Saved to {output_dir}")




    def nextFile(self):
        numberOfTabs = self.controlerTab.count()
        current = self.controlerTab.currentIndex()
        currentName = None
        if current > -1:
            currentName = self.controlerTab.tabText(current)
            print(currentName)

        nextPage = TabWidget()

        if ((current + 1) == numberOfTabs):

            name = "0"
            if currentName != None:
                name = f"{int(currentName) + 1}"

            self.controlerTab.addTab(nextPage, name)

        else:
            nextName = self.controlerTab.tabText(current + 1)
            if (int(nextName) - int(currentName)) != 1:
                self.controlerTab.insertTab(current + 1, nextPage ,f"{int(currentName) + 1}")

        self.controlerTab.setCurrentIndex(current + 1)

        ## Setting focus
        insideTextEdit = self.controlerTab.widget(current + 1).findChild(QTextEdit, "textEdit")
        insideTextEdit.setFocus(True)


    def removeTab(self):
        current = self.controlerTab.currentIndex()
        if current > 0:
            self.controlerTab.removeTab(current)

    def preTab(self):
        current = self.controlerTab.currentIndex()
        if current > 0:
            self.controlerTab.setCurrentIndex(current - 1)

    def clearAll(self):
        self.controlerTab.clear()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


