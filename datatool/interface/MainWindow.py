# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtdesigner/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1600)
        MainWindow.setMinimumSize(QtCore.QSize(1600, 1600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setSpacing(3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.topTables = QtWidgets.QStackedWidget(self.centralwidget)
        self.topTables.setLineWidth(1)
        self.topTables.setObjectName("topTables")
        self.albumsPage = QtWidgets.QWidget()
        self.albumsPage.setAutoFillBackground(False)
        self.albumsPage.setObjectName("albumsPage")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.albumsPage)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.topAlbumsTableWidget = QtWidgets.QTableWidget(self.albumsPage)
        self.topAlbumsTableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.topAlbumsTableWidget.setColumnCount(4)
        self.topAlbumsTableWidget.setObjectName("topAlbumsTableWidget")
        self.topAlbumsTableWidget.setRowCount(0)
        self.topAlbumsTableWidget.horizontalHeader().setHighlightSections(False)
        self.topAlbumsTableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.topAlbumsTableWidget.horizontalHeader().setStretchLastSection(False)
        self.topAlbumsTableWidget.verticalHeader().setSortIndicatorShown(False)
        self.topAlbumsTableWidget.verticalHeader().setStretchLastSection(False)
        self.gridLayout_2.addWidget(self.topAlbumsTableWidget, 1, 0, 1, 3)
        self.topTables.addWidget(self.albumsPage)
        self.songsPage = QtWidgets.QWidget()
        self.songsPage.setObjectName("songsPage")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.songsPage)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.topSongsTableWidget = QtWidgets.QTableWidget(self.songsPage)
        self.topSongsTableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.topSongsTableWidget.setColumnCount(5)
        self.topSongsTableWidget.setObjectName("topSongsTableWidget")
        self.topSongsTableWidget.setRowCount(0)
        self.topSongsTableWidget.horizontalHeader().setHighlightSections(False)
        self.topSongsTableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.gridLayout_3.addWidget(self.topSongsTableWidget, 0, 0, 1, 1)
        self.topTables.addWidget(self.songsPage)
        self.artistsPage = QtWidgets.QWidget()
        self.artistsPage.setObjectName("artistsPage")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.artistsPage)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.topArtistsTableWidget = QtWidgets.QTableWidget(self.artistsPage)
        self.topArtistsTableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.topArtistsTableWidget.setColumnCount(2)
        self.topArtistsTableWidget.setObjectName("topArtistsTableWidget")
        self.topArtistsTableWidget.setRowCount(0)
        self.topArtistsTableWidget.horizontalHeader().setHighlightSections(False)
        self.gridLayout_5.addWidget(self.topArtistsTableWidget, 0, 0, 1, 1)
        self.topTables.addWidget(self.artistsPage)
        self.gridLayout_4.addWidget(self.topTables, 1, 0, 1, 3)
        self.songsPageButton = QtWidgets.QPushButton(self.centralwidget)
        self.songsPageButton.setObjectName("songsPageButton")
        self.gridLayout_4.addWidget(self.songsPageButton, 0, 0, 1, 1)
        self.albumsPageButton = QtWidgets.QPushButton(self.centralwidget)
        self.albumsPageButton.setObjectName("albumsPageButton")
        self.gridLayout_4.addWidget(self.albumsPageButton, 0, 1, 1, 1)
        self.artistsPageButton = QtWidgets.QPushButton(self.centralwidget)
        self.artistsPageButton.setObjectName("artistsPageButton")
        self.gridLayout_4.addWidget(self.artistsPageButton, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_4, 1, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 17))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuUser = QtWidgets.QMenu(self.menubar)
        self.menuUser.setObjectName("menuUser")
        self.menuData = QtWidgets.QMenu(self.menubar)
        self.menuData.setObjectName("menuData")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionLoad_Database = QtWidgets.QAction(MainWindow)
        self.actionLoad_Database.setObjectName("actionLoad_Database")
        self.actionAdd_User = QtWidgets.QAction(MainWindow)
        self.actionAdd_User.setObjectName("actionAdd_User")
        self.actionChange_User = QtWidgets.QAction(MainWindow)
        self.actionChange_User.setObjectName("actionChange_User")
        self.actionDelete_User = QtWidgets.QAction(MainWindow)
        self.actionDelete_User.setObjectName("actionDelete_User")
        self.actionUpdate_Data = QtWidgets.QAction(MainWindow)
        self.actionUpdate_Data.setObjectName("actionUpdate_Data")
        self.actionGenerate_Collage = QtWidgets.QAction(MainWindow)
        self.actionGenerate_Collage.setObjectName("actionGenerate_Collage")
        self.menuFile.addAction(self.actionQuit)
        self.menuUser.addAction(self.actionAdd_User)
        self.menuUser.addAction(self.actionChange_User)
        self.menuUser.addAction(self.actionDelete_User)
        self.menuUser.addAction(self.actionUpdate_Data)
        self.menuData.addAction(self.actionGenerate_Collage)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuUser.menuAction())
        self.menubar.addAction(self.menuData.menuAction())

        self.retranslateUi(MainWindow)
        self.topTables.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Last.fm Data Tool"))
        self.topAlbumsTableWidget.setSortingEnabled(True)
        self.topSongsTableWidget.setSortingEnabled(True)
        self.topArtistsTableWidget.setSortingEnabled(True)
        self.songsPageButton.setText(_translate("MainWindow", "Top Songs"))
        self.albumsPageButton.setText(_translate("MainWindow", "Top Albums"))
        self.artistsPageButton.setText(_translate("MainWindow", "Top Artists"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuUser.setTitle(_translate("MainWindow", "User"))
        self.menuData.setTitle(_translate("MainWindow", "Stats"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionLoad_Database.setText(_translate("MainWindow", "Load Database"))
        self.actionLoad_Database.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.actionAdd_User.setText(_translate("MainWindow", "Add User"))
        self.actionChange_User.setText(_translate("MainWindow", "Change User"))
        self.actionDelete_User.setText(_translate("MainWindow", "Delete User"))
        self.actionUpdate_Data.setText(_translate("MainWindow", "Update Data"))
        self.actionGenerate_Collage.setText(_translate("MainWindow", "Generate Collage"))


