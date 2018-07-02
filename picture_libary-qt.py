#!/usr/bin/python3

import sys
import os
import numpy as np
import copy
import random
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDesktopWidget, QAction, qApp, \
    QMenu, QFileSystemModel, QTreeView, QSplitter, QFrame, QAbstractItemView, QListWidget, QListWidgetItem, QListView, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QTreeWidget, QWidget, QPushButton, QColumnView, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QDir, Qt, QItemSelection, QSize, QPoint

filename = None

homedir = os.path.expanduser(str("~"))

detectDir = None
workingDir = homedir + "/" + "picture_library"

# todo check these exist
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
glasses_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

# todo add a form of config.. dialog, tabs
# failback settings
if detectDir is None or len(detectDir) == 0:
    detectDir = "objects"

# check folders
if not os.path.exists(str(workingDir)):
    try:
        os.mkdir(str(workingDir))
    except:
        print("[Error]\tFailed to create" + str(workingDir))
        exit()
else:
    if not os.path.exists(str(workingDir + "/" + detectDir)):
        try:
            os.mkdir(str(workingDir + "/" + detectDir))
        except:
            print("[Error]\tFailed to create" + str(workingDir + "/" + detectDir))
            exit()


class ImageList:
    def __init__(self, filename, imgsize):
        self.filename = str(filename)
        self.imgorg = cv2.imread(self.filename)
        self.img = self.resizeImage(self.imgorg, 1000)
        self.imgsize = imgsize
        self.objectsFound = []
        self.counter = 0

    def resizeImage(self, imgorg, imgsize):
        """
        Resize an image using cv2.resize
        :param imgorg: cv2.imread
        :param imgsize: px to resize to
        :return: resized
        """
        r = float(imgsize) / imgorg.shape[1]
        dim = (imgsize, int(imgorg.shape[0] * r))
        resized = cv2.resize(imgorg, dim, interpolation=cv2.INTER_AREA)
        return resized

    def detectObjects(self):

        if face_cascade is not None:
            self.detectFaces(self.img)

    def detectFaces(self, img_gry):
        img_gry = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        foundObject = None

        # todo if config, if caaras, if faces
        faces = face_cascade.detectMultiScale(img_gry, 1.3, 6)
        if len(faces) is not 0:
            for (x, y, w, h,) in faces:
                self.counter += 1
                foundObject = "Pos_Face"
                roi_gray = img_gry[y:y + h, x:x + w]

                eyes = eye_cascade.detectMultiScale(roi_gray)
                if len(eyes) is not 0:
                    foundObject = "Face"
                    # Draw eyes?
                    # for (ex, ey, ew, eh,) in eyes:
                    # cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), rnd_col(255, 255, 255), 2)

                glasses = glasses_cascade.detectMultiScale(roi_gray)
                if len(glasses) is not 0:
                    foundObject = "Face"
                    # Draw glasses?
                    # for (gx, gy, gw, gh,) in eyes:
                    # cv2.rectangle(img, (gx, gy), (gx + gw, gy + gh), rnd_col(255, 255, 255), 2)

                self.objectsFound.append([foundObject, x, y, w, h])
                print(str(self.objectsFound))
                # draw face
                roi_color = self.img[y:y + h, x:x + w]
                cv2.rectangle(self.img, (x, y), (x + w, y + h), self.rnd_col(255, 100, 100))
                cv2.imshow(self.filename, self.img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    def rnd_col(self, r, b, g):
        if b > 0: b = b + 1
        if r > 0: r = r + 1
        if g > 0: g = g + 1
        b = random.randint(0, int(b))
        g = random.randint(0, int(g))
        r = random.randint(0, int(r))
        color = (b, g, r)
        return color


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.showMaximized()
        self.center()
        self.setWindowTitle('Picture Library')

        self.menuSystem()
        self.frameCent = QFrame()

        self.frameLeft = QFrame(self.frameCent)
        self.frameLeft.setFrameShape(QFrame.StyledPanel)
        self.frameLeft.resize(int(.33 * QDesktopWidget().screenGeometry().width()),
                              QDesktopWidget().screenGeometry().height() - 90)
        # todo add tab, files and database
        self.treeDirBuild()

        self.spliterLeft = QSplitter(self.frameCent)

        self.frameRight = QFrame(self.frameCent)
        self.frameRight.setFrameShape(QFrame.StyledPanel)
        self.frameRight.move(int(.33 * QDesktopWidget().screenGeometry().width()), 0)
        self.frameRight.resize(int(.66 * QDesktopWidget().screenGeometry().width()) - 10,
                               QDesktopWidget().screenGeometry().height() - 90)

        self.listImages = QListWidget(self.frameRight)
        self.listImages.setViewMode(QListView.IconMode)
        self.listImages.resize(int(.66 * QDesktopWidget().screenGeometry().width()),
                               QDesktopWidget().screenGeometry().height() - 90)
        self.listImages.setIconSize(QSize(150, 150))
        self.listImages.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listImages.customContextMenuRequested.connect(self.listImagesContextMenu)
        self.listImages.addAction(self.actDetectObjects)

        self.setCentralWidget(self.frameCent)

        self.statusBar().showMessage('Ready')

        self.show()

    # def treeDirClicked(self, selected, deselected):
    def treeDirClicked(self, index):

        indexItem = self.model.index(index.row(), 0, index.parent())
        workingDir = self.model.filePath(indexItem)
        self.listImages.clear()
        self.listImagesRefresh(workingDir)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def treeDirBuild(self):
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.treeDir = QTreeView(self.frameLeft)
        self.treeDir.setModel(self.model)
        self.treeDir.resize(int(.33 * QDesktopWidget().screenGeometry().width()),
                            QDesktopWidget().screenGeometry().height() - 90)
        self.treeDir.setColumnWidth(0, 300)
        # self.treeDir.selectionModel().selectionChanged.connect(self.treeDirClicked)
        self.treeDir.clicked.connect(self.treeDirClicked)
        self.treeDir.setSelectionMode(QAbstractItemView.SingleSelection)

    def onQuit(self):
        confirm = QMessageBox.question(self, "Quit?", "Are you sure you want to quit?",
                                       QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            qApp.quit()

    def menuSystem(self):

        menubar = self.menuBar()
        menuFile = menubar.addMenu('&File')
        menuWindow = menubar.addMenu('&Window')

        menuSubImport = QMenu('Import', self)

        self.actQuit = QAction(QIcon.fromTheme('exit'), '&Quit', self)
        self.actQuit.setShortcut('Ctrl+Q')
        self.actQuit.setStatusTip('Quit Application')
        self.actQuit.triggered.connect(self.onQuit)
        self.actImport = QAction('Import something', self)
        self.actStatus = QAction('Show &Statusbar', self, checkable=True)
        self.actStatus.setChecked(True)
        self.actStatus.triggered.connect(self.toggleStatus)
        self.actDetectObjects = QAction("Detect &Objects", self)
        self.actDetectObjects.triggered.connect(self.callDetectObjects)

        menuSubImport.addAction(self.actImport)
        menuFile.addMenu(menuSubImport)
        menuFile.addAction(self.actQuit)
        menuWindow.addAction(self.actStatus)

        toolbar = self.addToolBar('Quit')
        toolbar.addAction(self.actQuit)

    def listImagesContextMenu(self, pos):
        menu = QMenu(self)
        menu.addAction(self.actDetectObjects)
        menu.exec_(self.listImages.mapToGlobal(pos))

    def toggleStatus(self, state):
        if state:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    def contextMenuEvent(self, QContextMenuEvent):
        conMenu = QMenu(self)

        actDel = conMenu.addAction("Delete")
        action = conMenu.exec(self.mapToGlobal(QContextMenuEvent.pos()))

    def listImagesRefresh(self, workingDir):
        # fixme need to change to a thread, hogs GUI while file list is created
        print("List")
        files = []
        if os.path.isdir(workingDir):
            for file in os.listdir(workingDir):
                if file.endswith(".jpg"):
                    files.append(os.path.join(workingDir, file))

        for img in files:
            item = QListWidgetItem()
            icon = QIcon()
            icon.addPixmap(QPixmap(str(img)), QIcon.Normal, QIcon.On)
            item.setIcon(icon)
            item.setText(str(img))

            self.listImages.addItem(item)
        print(str(files))

    def callDetectObjects(self):
        filename = self.listImages.currentItem().text()
        if len(filename) is not 0:
            ImageList(filename, 1000).detectObjects()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Window()

    sys.exit(app.exec_())
