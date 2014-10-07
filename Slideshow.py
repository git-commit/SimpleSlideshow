from PyQt5 import QtWidgets, QtCore, QtGui
from os import listdir
from os.path import isfile, join
import os
import sys
import random
import time
import threading


class Slideshow(QtWidgets.QMainWindow):
    picture_types = ('.jpg', '.png', '.JPG', '.PNG', '.jpeg', '.JPEG')

    def __init__(self, sleep):
        super(Slideshow, self).__init__()
        self.scene = QtWidgets.QGraphicsScene()
        self.graphics_view = QtWidgets.QGraphicsView(self.scene)
        self.setCentralWidget(self.graphics_view)
        self.setWindowTitle('Slideshow')
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphics_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.show()

        QtWidgets.QShortcut(QtGui.QKeySequence("SPACE"), self,
                            self.nextPicture)

        self.path = os.getcwd()
        self.files = Slideshow.get_all_pictures(self.path)

        self.lock = threading.Lock()

        self.sleep = sleep
        self._stopThread = False
        self.thread = threading.Thread(target=slideTime, args=(self, self.sleep))
        self.thread.daemon = True
        self.thread.start()

    def nextPicture(self):
        self.lock.acquire()
        self.files = Slideshow.get_all_pictures(self.path)
        if self.files:
            r = random.randint(0, len(self.files) - 1)
            self._change_picture(self.files[r])
        self.lock.release()

    def _change_picture(self, file):
        pixmap = QtGui.QPixmap(os.path.join(os.getcwd(), file))
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene.clear()
        self.scene.addItem(item)
        print("Changed picture to " + str(file))
        self.graphics_view.fitInView(item, QtCore.Qt.KeepAspectRatio)

    def stopThread(self):
        return self._stopThread

    @staticmethod
    def get_all_pictures(path):
        print("Generating file list...")
        list = [f for f in listdir(path) if isfile(join(path, f))
                and os.path.splitext(f)[1] in Slideshow.picture_types]
        print("Number of files: " + str(len(list)))
        return list

    def closeEvent(self, event):
        print("Setting thread variable to false.")
        self._stopThread = True
        event.accept()  # let the window close


def slideTime(slide, delay):
    print("Starting thread")

    while not slide.stopThread():
        slide.nextPicture()
        time.sleep(delay)


def main():
    app = QtWidgets.QApplication(sys.argv)
    s = Slideshow(int(sys.argv[1]) if len(sys.argv) == 2 else 300)
    i = app.exec_()
    sys.exit(i)

if __name__ == '__main__':
    main()
