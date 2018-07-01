#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDesktopWidget, QAction, qApp, \
    QMenu, QFileSystemModel, QTreeView, QVBoxLayout, QHBoxLayout, QGridLayout, QSplitter, QFrame, \
    QTreeWidget, QWidget, QPushButton, QColumnView, QAbstractItemView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDir, Qt, QItemSelection


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.showMaximized()
        self.center()
        self.setWindowTitle('Picture Library')

        self.frameLeft = QFrame()
        self.frameLeft.setFrameShape(QFrame.StyledPanel)
        self.frameLeft.resize(int(.33 * QDesktopWidget().screenGeometry().width()),
                              QDesktopWidget().screenGeometry().height() - 90)
        self.treeDir()

        self.frameRight = QFrame()
        self.frameRight.setFrameShape(QFrame.StyledPanel)
        self.frameRight.resize(int(.66 * QDesktopWidget().screenGeometry().width()),
                               QDesktopWidget().screenGeometry().height() - 90)

        self.spliterLeft = QSplitter(self.frameLeft)

        self.setCentralWidget(self.frameLeft)

        self.menuSystem()
        self.statusBar().showMessage('Ready')

        self.show()

    def treeDirClicked(self, selected, deselected):
        print("CLICKED")
        # print(str(QFileSystemModel.fileInfo(self.model, self.treeDir.selectionModel().selectedIndex())))
        # index = self.treeDir.selectionModel().selectedIndexes()
        # print(self.treeDir.selectionModel().model().data(self.treeDir.selectionModel().selectedIndexes()))

        indexes = self.treeDir.selectionModel().selectedIndexes()[0]
        data = self.treeDir.selectionModel().model()
        # for index in indexes:
        print(str(data.data(indexes)))

        QMessageBox.question(self, "Clicked", "Something was clicked\n" + str(self.sender().currentIndex),
                             QMessageBox.Ok)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def treeDir(self):
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.treeDir = QTreeView(self.frameLeft)
        self.treeDir.setModel(self.model)
        self.treeDir.resize(int(.33 * QDesktopWidget().screenGeometry().width()),
                            QDesktopWidget().screenGeometry().height() - 90)
        self.treeDir.setColumnWidth(0, 300)
        self.treeDir.selectionModel().selectionChanged.connect(self.treeDirClicked)
        self.treeDir.setSelectionMode(QAbstractItemView.SingleSelection)
        self.frameLeft.adjustSize()

    def onQuit(self):
        confirm = QMessageBox.question(self, "Quit?", "Are you sure you want to quit?",
                                       QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            qApp.quit()

    def menuSystem(self):

        """
        btnQuit = QPushButton('Quit', self)
        btnQuit.clicked.connect(self.onQuit)
        btnQuit.resize(btnQuit.sizeHint())
        btnQuit.move(5, 50)
        """

        menubar = self.menuBar()
        menuFile = menubar.addMenu('&File')
        menuWindow = menubar.addMenu('&Window')

        menuSubImport = QMenu('Import', self)

        actQuit = QAction(QIcon.fromTheme('exit'), '&Quit', self)
        actQuit.setShortcut('Ctrl+Q')
        actQuit.setStatusTip('Quit Application')
        actQuit.triggered.connect(self.onQuit)
        actImport = QAction('Import something', self)
        actStatus = QAction('Show &Statusbar', self, checkable=True)
        actStatus.setChecked(True)
        actStatus.triggered.connect(self.toggleStatus)

        menuSubImport.addAction(actImport)
        menuFile.addMenu(menuSubImport)
        menuFile.addAction(actQuit)
        menuWindow.addAction(actStatus)

        toolbar = self.addToolBar('Quit')
        toolbar.addAction(actQuit)

    def toggleStatus(self, state):
        if state:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    def contextMenuEvent(self, QContextMenuEvent):
        conMenu = QMenu(self)

        actDel = conMenu.addAction("Delete")
        action = conMenu.exec(self.mapToGlobal(QContextMenuEvent.pos()))

    """
    def treeDir(self):

        self.model = QFileSystemModel()
        self.model.setRootPath('')
        self.tree = QTreeView()
        self.tree.setModel(self.model)

        # layout.addWidget(self.tree)
    """


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Window()

    sys.exit(app.exec_())
