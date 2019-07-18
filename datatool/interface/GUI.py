#---------------------------------------------------------------------------------------------------
# Author: Will Fenton
# Date:   May 17 2019

# This is the actual PyQt application
# Implements the functionality for the UI compiled from QT designer
#---------------------------------------------------------------------------------------------------

import sys
import os
import sqlite3
from math import floor, sqrt
from functools import partial
from configparser import ConfigParser, ExtendedInterpolation

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QLabel, QTableWidgetItem, QLabel, QSizePolicy, QHeaderView, QInputDialog, QLineEdit
from PyQt5.QtCore import QSize, Qt

from datatool.interface.MainWindow import Ui_MainWindow
from datatool.data.db_functions import get_config, validate_username, add_user, delete_user, update_data
from datatool.data.collage import generate_collage

#---------------------------------------------------------------------------------------------------

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        self.ask_before_quit = False

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # setup top table headers
        self.ui.topSongsTableWidget.setHorizontalHeaderLabels(["", "Song", "Artist", "Album", "Plays"])
        self.ui.topArtistsTableWidget.setHorizontalHeaderLabels(["Artist", "Plays"])

        self.changePage(0)

        # Connect menubar actions
        self.ui.actionQuit.triggered.connect(self.closeApplication)
        self.ui.actionTop_Albums.triggered.connect(partial(self.topAlbumsTableLoad, 100, 150))
        self.ui.actionTop_Tracks.triggered.connect(partial(self.changePage, 1))
        self.ui.actionTop_Artists.triggered.connect(partial(self.changePage, 2))
        self.ui.actionAdd_User.triggered.connect(self.addUser)
        self.ui.actionChange_User.triggered.connect(self.changeUser)
        self.ui.actionDelete_User.triggered.connect(self.deleteUser)
        self.ui.actionUpdate_Data.triggered.connect(self.updateData)
        self.ui.actionGenerate_Collage.triggered.connect(self.generateCollage)

        # Connect buttons
        self.ui.topAlbumsLimitButton.clicked.connect(self.topAlbumsChangeLimit)
        
        # get config parser
        self.config_parser = get_config()

        # get db
        db_path = self.config_parser.get("db", "db_path")
        self.db = sqlite3.connect(db_path)

        # get last.fm api key
        self.api_key = self.config_parser.get("settings", "api_key")

        # set window icon
        # logo_path = os.path.join(self.config_parser.get("files", "resources_path"), "logo.png")
        # icon = QIcon()
        # icon.addPixmap(QPixmap(logo_path), QIcon.Normal, QIcon.Off)
        # self.ui.centralwidget.setWindowIcon(QIcon(logo_path))

        users = [row[0] for row in self.db.execute("SELECT DISTINCT username FROM Users ORDER BY timestamp ASC;")]
        if len(users) > 0:
            self.current_user = users[0]
        else:
            self.current_user = None

        self.refreshTables()


    def changePage(self, page):
        self.ui.topTables.setCurrentIndex(page)


    def addUser(self):
        username, okPressed = QInputDialog.getText(self, "Add user","Last.fm username:", QLineEdit.Normal, "")
        username = username.lower()
        if okPressed and username != "":
            if validate_username(username, self.api_key):
                if add_user(self.db, username, self.api_key):
                    QMessageBox.information(self, "Success", f"Added user:\n{username}", QMessageBox.Ok)
                    if self.current_user is None:
                        self.current_user = username
                else:
                    QMessageBox.critical(self, "Error", f"Error adding user:\n{username}", QMessageBox.Ok)
            else:
                QMessageBox.warning (self, "Warning", f"Invalid username:\n{username}", QMessageBox.Ok)


    def changeUser(self):
        users = [row[0] for row in self.db.execute("SELECT DISTINCT username FROM Users ORDER BY timestamp ASC;")]	
        if len(users) > 0:
            index = users.index(self.current_user) if self.current_user is not None else 0
            username, okPressed = QInputDialog.getItem(self, "Change user", "List of users", users, index, False) 
            if okPressed and username:
                self.current_user = username
                QMessageBox.information(self, "Changed user", f"Current user:\n{self.current_user}", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "No users", "No users to select from.", QMessageBox.Ok)
        self.refreshTables()


    def deleteUser(self):
        users = [row[0] for row in self.db.execute("SELECT DISTINCT username FROM Users ORDER BY timestamp ASC;")]	
        if len(users) > 0:
            username, okPressed = QInputDialog.getItem(self, "Delete user", "List of users", users, 0, False) 
            if okPressed and username:
                if delete_user(self.db, username, self.api_key):
                    if self.current_user == username:
                        self.current_user = None
                    QMessageBox.information(self, "Deleted user", f"Deleted user:\n{username}", QMessageBox.Ok)
                else:
                    QMessageBox.critical(self, "Error", f"Error deleting user:\n{username}", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "No users", "No users to select from.", QMessageBox.Ok)

    
    def updateData(self):
        users = [row[0] for row in self.db.execute("SELECT DISTINCT username FROM Users ORDER BY timestamp ASC;")]	
        if len(users) > 0:
            username, okPressed = QInputDialog.getItem(self, "Update data", "List of users", users, 0, False) 
            if okPressed and username:
                update_data(self.db, username, self.api_key)
                QMessageBox.information(self, "Updated data", f"Updated data for user:\n{username}", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "No users", "No users to select from.", QMessageBox.Ok)
        self.refreshTables()

    
    def generateCollage(self):
        if self.current_user is None:
            QMessageBox.information(self, "No current user", "Select a user first.", QMessageBox.Ok)
            return False
        num_albums = len(self.db.execute(f"SELECT image_path, album_name FROM [user-{self.current_user}] GROUP BY image_path, album_name;").fetchall())
        if num_albums < 1:
            QMessageBox.information(self, "Not enough albums", "Not enough albums. Have you updated data yet?", QMessageBox.Ok)
            return False
        max_size = min(floor(sqrt(num_albums)), 50)
        size, okPressed = QInputDialog.getInt(self, "Collage size","Size:", 10, 1, max_size, 1)
        if okPressed and size:
            generate_collage(self.db, self.current_user, size, size)
            QMessageBox.information(self, "Collage generated", "Collage successfully generated.", QMessageBox.Ok)


    def refreshTables(self):
        self.topAlbumsTableLoad()
        self.topArtistsTableLoad()
        self.topSongsTableLoad()

    
    def topAlbumsTableLoad(self, limit=100, image_size=150):
        # set column labels
        self.ui.topAlbumsTableWidget.setHorizontalHeaderLabels(["", "Album", "Artist", "Plays"])

        # set column resize modes
        self.ui.topAlbumsTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.ui.topAlbumsTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.topAlbumsTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.ui.topAlbumsTableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        # set row resize modes
        self.ui.topAlbumsTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # no user -> no data to display
        if self.current_user is None:
            return False

        # clear the table
        self.ui.topAlbumsTableWidget.clearContents()

        # get the total number of albums (so we don't accidentally go over it)
        num_albums = self.db.execute(f"SELECT COUNT(*) FROM (SELECT * FROM 'user-{self.current_user}' GROUP BY album_name, artist_name, image_path);").fetchone()[0]
        limit = min(limit, num_albums)
        
        # no data to display
        if num_albums < 1:
            return False

        # get the album data from the database
        rows = self.db.execute(f"SELECT album_name, artist_name, COUNT(*), image_path, MIN(unix_timestamp) FROM 'user-{self.current_user}' GROUP BY album_name, artist_name, image_path ORDER BY COUNT(*) DESC LIMIT ?;", [limit]).fetchall()
        row_count = len(rows)

        # set correct number of rows
        self.ui.topAlbumsTableWidget.setRowCount(row_count)
        self.ui.topAlbumsLimitButton.setText(f"Set Limit ({row_count})")

        # setting the data in the rows
        for i in range(len(rows)):
            album_name, artist_name, count, image_path, first_timestamp = rows[i]

            self.ui.topAlbumsTableWidget.setItem(i, 1, QTableWidgetItem(album_name))
            self.ui.topAlbumsTableWidget.setItem(i, 2, QTableWidgetItem(artist_name))

            # gotta do this so you can sort by count
            self.ui.topAlbumsTableWidget.setItem(i, 3, QTableWidgetItem(""))
            self.ui.topAlbumsTableWidget.item(i, 3).setData(Qt.DisplayRole, count)

            # create QPixmap for the album art, put it in a cell
            label = QLabel()
            album_art = QPixmap(image_path).scaled(QSize(image_size, image_size))
            label.setPixmap(album_art)
            self.ui.topAlbumsTableWidget.setCellWidget(i, 0, label)

        # display the table
        self.changePage(0)

        return True


    def topAlbumsChangeLimit(self):
        if self.current_user is None:
            return False
        
        limit, okPressed = QInputDialog.getInt(self, "Set Limit","Number of Albums:", 100, 1, 100000, 1)
        if okPressed and limit:
            self.topAlbumsTableLoad(limit)
    

    def topArtistsTableLoad(self):
        if self.current_user is None:
            return False

        rows = self.db.execute(f"SELECT artist_name, COUNT(*) FROM 'user-{self.current_user}' GROUP BY artist_name ORDER BY COUNT(*) DESC;").fetchall()
        self.ui.topArtistsTableWidget.setRowCount(len(rows))

        self.ui.topArtistsTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.topArtistsTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        self.ui.topArtistsTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i in range(len(rows)):
            self.ui.topArtistsTableWidget.setItem(i, 0, QTableWidgetItem(str(rows[i][0])))
            self.ui.topArtistsTableWidget.setItem(i, 1, QTableWidgetItem(""))
            self.ui.topArtistsTableWidget.item(i, 1).setData(Qt.DisplayRole, int(rows[i][1]))


    def topArtistsChangeLimit(self):
        if self.current_user is None:
            return False
        
        num_albums = self.db.execute(f"SELECT COUNT(*) FROM (SELECT * FROM 'user-{self.current_user}' GROUP BY album_name, artist_name, image_path);").fetchone()[0]
        limit, okPressed = QInputDialog.getInt(self, "Set Limit","Number of Albums:", 100, 1, 100000, 1)
        if okPressed and limit:
            limit = min(limit, num_albums)
            self.topArtistsTableLoad(limit)


    def topSongsTableLoad(self):
        if self.current_user is None:
            return False

        rows = self.db.execute(f"SELECT track_name, album_name, artist_name, COUNT(*), image_path FROM 'user-{self.current_user}' GROUP BY track_name, album_name, artist_name, image_path ORDER BY COUNT(*) DESC LIMIT 100;").fetchall()
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


    def topSongsChangeLimit(self):
        if self.current_user is None:
            return False
        
        num_albums = self.db.execute(f"SELECT COUNT(*) FROM (SELECT * FROM 'user-{self.current_user}' GROUP BY album_name, artist_name, image_path);").fetchone()[0]
        limit, okPressed = QInputDialog.getInt(self, "Set Limit","Number of Albums:", 100, 1, 100000, 1)
        if okPressed and limit:
            limit = min(limit, num_albums)
            self.topSongsTableLoad(limit)


    # This is triggered when the user clicks the X / close button
    def closeEvent(self, event):      
        event.ignore()      
        self.closeApplication()
        

    def closeApplication(self):
        # Asks user for confirmation before quitting the app
        if self.ask_before_quit:
            choice = QMessageBox.question(self, "Quit", "Do you really want to exit?", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                self.db.close()
                sys.exit()
        else:
            self.db.close()
            sys.exit()

#---------------------------------------------------------------------------------------------------
