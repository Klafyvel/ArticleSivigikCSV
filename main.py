import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import matplotlib.pyplot as pl
from smallCSVParser import dict_from_file

class App(QWidget):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

        self.setWindowTitle("Plot")

        self.btn_run = QPushButton("Plot")
        self.btn_choose = QPushButton("Browse File")

        self.labels = QListWidget()

        self.v =  None

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn_choose)
        self.layout.addWidget(self.labels)
        self.layout.addWidget(self.btn_run)
        self.setLayout(self.layout)

        self.btn_choose.clicked.connect(self.choose_file)
        self.btn_run.clicked.connect(self.draw)

    @pyqtSlot()
    def choose_file(self):
        f_name = QFileDialog.getOpenFileName()
        if not f_name:
            return
        f_name = f_name[0]
        self.v = dict_from_file(f_name)
        self.labels.clear()
        for l in self.v:
            self.labels.addItem(l)
            self.v[l] = [float(i) for i in self.v[l]]
        self.btn_choose.setText(f_name)

    @pyqtSlot()
    def draw(self):
        if not self.v:
            return
        pl.close('all')
        x_label = self.labels.currentItem().text()
        X = self.v[x_label]
        pl.xlabel(x_label)
        for l in self.v:
            if l == x_label:
                continue
            pl.plot(X,self.v[l], label=l)
        pl.legend(loc="best")
        pl.show()

app = QApplication(sys.argv)
a = App()

a.show()
app.exec()