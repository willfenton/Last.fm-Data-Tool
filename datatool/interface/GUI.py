#!/usr/bin/python3
#---------------------------------------------------------------------------------------------------
# Author: Will Fenton
# Date:   May 17 2019
#---------------------------------------------------------------------------------------------------

import sys
import os
import sqlite3
from functools import partial

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QLabel, QTableWidgetItem, QLabel, QSizePolicy
from PyQt5.QtCore import QSize, Qt

from datatool.interface.MainWindow import Ui_MainWindow

#---------------------------------------------------------------------------------------------------

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        self.ask_before_quit = False

        self.connected_to_database = False

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # setup top table headers
        self.ui.topAlbumsTableWidget.setHorizontalHeaderLabels(["Album", "Artist", "Plays"])
        self.ui.topSongsTableWidget.setHorizontalHeaderLabels(["Song", "Artist", "Album", "Plays"])
        self.ui.topArtistsTableWidget.setHorizontalHeaderLabels(["Artist", "Plays"])

        # Connect the buttons.
        self.ui.albumsPageButton.clicked.connect(partial(self.changePage, 0))
        self.ui.songsPageButton.clicked.connect(partial(self.changePage, 1))
        self.ui.artistsPageButton.clicked.connect(partial(self.changePage, 2))

        # Connect menubar actions
        self.ui.actionQuit.triggered.connect(self.closeApplication)
        self.ui.actionLoad_Database.triggered.connect(self.loadDatabase)


    def changePage(self, page):
        self.ui.topTables.setCurrentIndex(page)


    def loadDatabase(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Load Database", "", "All Files (*);;Database Files (*.db)", options=options)
        try:
            if os.path.isfile(fileName):
                if os.path.getsize(fileName) > 100:
                    with open(fileName,"r", encoding="ISO-8859-1") as file:
                        header = file.read(100)
                        if header.startswith("SQLite format 3"):
                            self.db = sqlite3.connect(fileName)
                            self.connected_to_database = True
                            QMessageBox.information(self, "Success", "Successfully connected to the database", QMessageBox.Ok)

                            self.loadTopAlbumsTable()
                            self.loadTopSongsTable()
                            self.loadTopArtistsTable()

                        else:
                            raise Exception("wrong file format")
                else:
                    raise Exception("path too large")
            else:
                raise Exception("file doesn't exist")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {e}", QMessageBox.Ok)

    
    def loadTopAlbumsTable(self):
        rows = self.db.execute("SELECT album_name, artist_name, COUNT(*) FROM 'user-willfenton14' GROUP BY album_name, artist_name ORDER BY COUNT(*) DESC;").fetchall()
        self.ui.topAlbumsTableWidget.setRowCount(len(rows))

        # http = urllib3.PoolManager()

        for i in range(len(rows)):
            self.ui.topAlbumsTableWidget.setItem(i, 0, QTableWidgetItem(str(rows[i][0])))
            self.ui.topAlbumsTableWidget.setItem(i, 1, QTableWidgetItem(str(rows[i][1])))
            self.ui.topAlbumsTableWidget.setItem(i, 2, QTableWidgetItem(""))
            self.ui.topAlbumsTableWidget.item(i, 2).setData(Qt.DisplayRole, int(rows[i][2]))

            # image = http.request("GET", rows[i][2]).data

            # pixmap = QPixmap()
            # pixmap.loadFromData(image)

            # label = QLabel()
            # label.setPixmap(pixmap.scaled(QSize(150, 150)))

            # self.ui.topAlbumsTableWidget.setCellWidget(i, 0, label)

    
    def loadTopArtistsTable(self):
        rows = self.db.execute("SELECT artist_name, COUNT(*) FROM 'user-willfenton14' GROUP BY artist_name ORDER BY COUNT(*) DESC;").fetchall()
        self.ui.topArtistsTableWidget.setRowCount(len(rows))

        for i in range(len(rows)):
            self.ui.topArtistsTableWidget.setItem(i, 0, QTableWidgetItem(str(rows[i][0])))
            self.ui.topArtistsTableWidget.setItem(i, 1, QTableWidgetItem(""))
            self.ui.topArtistsTableWidget.item(i, 1).setData(Qt.DisplayRole, int(rows[i][1]))

    
    def loadTopSongsTable(self):
        rows = self.db.execute("SELECT track_name, album_name, artist_name, COUNT(*) FROM 'user-willfenton14' GROUP BY track_name, album_name, artist_name ORDER BY COUNT(*) DESC;").fetchall()
        self.ui.topSongsTableWidget.setRowCount(len(rows))

        for i in range(len(rows)):
            self.ui.topSongsTableWidget.setItem(i, 0, QTableWidgetItem(str(rows[i][0])))
            self.ui.topSongsTableWidget.setItem(i, 1, QTableWidgetItem(str(rows[i][1])))
            self.ui.topSongsTableWidget.setItem(i, 2, QTableWidgetItem(str(rows[i][2])))
            self.ui.topSongsTableWidget.setItem(i, 3, QTableWidgetItem(""))
            self.ui.topSongsTableWidget.item(i, 3).setData(Qt.DisplayRole, int(rows[i][3]))

    # This is triggered when the user clicks the X / close button
    def closeEvent(self, event):      
        event.ignore()      
        self.closeApplication()
        

    def closeApplication(self):
        # Asks user for confirmation before quitting the app
        if self.ask_before_quit:
            choice = QMessageBox.question(self, "Quit", "Do you really want to exit?", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                if self.connected_to_database:
                    self.db.commit()
                    self.db.close()
                sys.exit()
        else:
            if self.connected_to_database:
                    self.db.commit()
                    self.db.close()
            sys.exit()

#---------------------------------------------------------------------------------------------------
