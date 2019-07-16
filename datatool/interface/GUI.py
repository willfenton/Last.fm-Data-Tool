#---------------------------------------------------------------------------------------------------
# Author: Will Fenton
# Date:   May 17 2019
#---------------------------------------------------------------------------------------------------

import sys
import os
import sqlite3
from functools import partial
from configparser import ConfigParser, ExtendedInterpolation

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QLabel, QTableWidgetItem, QLabel, QSizePolicy, QHeaderView
from PyQt5.QtCore import QSize, Qt

from datatool.interface.MainWindow import Ui_MainWindow
from datatool.data.db_functions import get_config

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
        self.ui.topAlbumsTableWidget.setHorizontalHeaderLabels(["", "Album", "Artist", "Plays"])
        self.ui.topSongsTableWidget.setHorizontalHeaderLabels(["", "Song", "Artist", "Album", "Plays"])
        self.ui.topArtistsTableWidget.setHorizontalHeaderLabels(["Artist", "Plays"])

        self.changePage(0)

        # Connect the buttons.
        self.ui.albumsPageButton.clicked.connect(partial(self.changePage, 0))
        self.ui.songsPageButton.clicked.connect(partial(self.changePage, 1))
        self.ui.artistsPageButton.clicked.connect(partial(self.changePage, 2))

        # Connect menubar actions
        self.ui.actionQuit.triggered.connect(self.closeApplication)
        self.ui.actionLoad_Database.triggered.connect(self.loadDatabase)

        # get config parser
        self.config_parser = get_config()
        db_path = self.config_parser.get("db", "db_path")
        self.db = sqlite3.connect(db_path)

        self.connected_to_database = True

        self.loadTopAlbumsTable()
        self.loadTopSongsTable()
        self.loadTopArtistsTable()


    def changePage(self, page):
        self.ui.topTables.setCurrentIndex(page)


    def loadDatabase(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Load Database", "", "All Files (*);;Database Files (*.db)", options=options)
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

    
    def loadTopAlbumsTable(self):
        rows = self.db.execute("SELECT album_name, artist_name, COUNT(*), image_path FROM 'user-willfenton14' GROUP BY album_name, artist_name, image_path ORDER BY COUNT(*) DESC;").fetchall()
        self.ui.topAlbumsTableWidget.setRowCount(len(rows))

        self.ui.topAlbumsTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.topAlbumsTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.topAlbumsTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.ui.topAlbumsTableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.ui.topAlbumsTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for i in range(len(rows)):
            self.ui.topAlbumsTableWidget.setItem(i, 1, QTableWidgetItem(str(rows[i][0])))
            self.ui.topAlbumsTableWidget.setItem(i, 2, QTableWidgetItem(str(rows[i][1])))
            self.ui.topAlbumsTableWidget.setItem(i, 3, QTableWidgetItem(""))
            self.ui.topAlbumsTableWidget.item(i, 3).setData(Qt.DisplayRole, int(rows[i][2]))

            pixmap = QPixmap(rows[i][3])

            label = QLabel()
            label.setPixmap(pixmap.scaled(QSize(150, 150)))

            self.ui.topAlbumsTableWidget.setCellWidget(i, 0, label)

    
    def loadTopArtistsTable(self):
        rows = self.db.execute("SELECT artist_name, COUNT(*) FROM 'user-willfenton14' GROUP BY artist_name ORDER BY COUNT(*) DESC;").fetchall()
        self.ui.topArtistsTableWidget.setRowCount(len(rows))

        self.ui.topArtistsTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.topArtistsTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.ui.topArtistsTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i in range(len(rows)):
            self.ui.topArtistsTableWidget.setItem(i, 0, QTableWidgetItem(str(rows[i][0])))
            self.ui.topArtistsTableWidget.setItem(i, 1, QTableWidgetItem(""))
            self.ui.topArtistsTableWidget.item(i, 1).setData(Qt.DisplayRole, int(rows[i][1]))

    
    def loadTopSongsTable(self):
        rows = self.db.execute("SELECT track_name, album_name, artist_name, COUNT(*), image_path FROM 'user-willfenton14' GROUP BY track_name, album_name, artist_name, image_path ORDER BY COUNT(*) DESC;").fetchall()
        self.ui.topSongsTableWidget.setRowCount(len(rows))

        self.ui.topSongsTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.topSongsTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.topSongsTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.ui.topSongsTableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.ui.topSongsTableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.ui.topSongsTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for i in range(len(rows)):
            self.ui.topSongsTableWidget.setItem(i, 1, QTableWidgetItem(str(rows[i][0])))
            self.ui.topSongsTableWidget.setItem(i, 2, QTableWidgetItem(str(rows[i][1])))
            self.ui.topSongsTableWidget.setItem(i, 3, QTableWidgetItem(str(rows[i][2])))
            self.ui.topSongsTableWidget.setItem(i, 4, QTableWidgetItem(""))
            self.ui.topSongsTableWidget.item(i, 4).setData(Qt.DisplayRole, int(rows[i][3]))

            pixmap = QPixmap(rows[i][4])

            label = QLabel()
            label.setPixmap(pixmap.scaled(QSize(150, 150)))

            self.ui.topSongsTableWidget.setCellWidget(i, 0, label)

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
