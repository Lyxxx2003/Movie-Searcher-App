# Author: LI Yuxin
# Product: CS IA main_code

# !!!
import sys

# Open the Douban Movie website for the crawler function
import webbrowser as web

# Import needed PyQt modules and files to achieve the GUI
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# Check for successful inputs or errors
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QAbstractItemView
# Choose dialog
from PyQt5.QtWidgets import QFileDialog
# Needed PyQt files
import Sign_Window_Interface
import Login_Dialog_Interface
import Main_Interface
import SetUp_Dialog
import History_Widget
import Main_Interface_Dialog
import Sign_Dialog_Interface

# Import sub-programs
# Import the sub-program, User_Database, which achieves the function of user database
import User_Database
# Import the sub-program, History_Database, which achieves the 'History' information for signed user
import History_Database
# Import the sub-program, Local_Database, which stores the database for offline users
import Local_Database
# Import the sub-program, Hash, which encrypts the inputted information that is stored in databases
import Hash
# Import the sub-program, BaiduAI, which achieves the function of photo recognition. It is an existing API
import BaiduAI_API
# Import the sub-program, Scraper_Douban_Movies_Database, to achieve the crawler function
import Scraper_Douban_Movies

# Import existing functions/modules
# Import time to get the key of local time in history database
import time
# Import numpy to get index of sort_score that contributes to the function of 'rating movies by scores'
import numpy as np

# Define all global variables that involve in the programming
# Define the global variable, count login errors
global g_login_error_counter
g_login_error_counter = 0
# Define a global variable, trace usernames(temporary)
global username
username = ''
# Define a global variable, trace usernames in hash(final)
global username_Hash_database
username_Hash_database = ''
# Define a global variable, trace filenames
global filename
filename = ''
# Define a global variable, judge whether the user is signed or unsigned. Do the function of authentification.
global sign_or_unsign_flag
sign_or_unsign_flag = False # Unsigned user
# Define a global variable, trace the information stored in the local database
global Local_Movie_Database
Local_Movie_Database = []

# Functions
# Define function spider:
# Get the information to search from user inputs & do crawler & insert information to movie database
def spider(name):
    # Function_History: Variable local_time: track users' searching time
    local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # User system_Configuration:
    # Users could change page_size to change the number of displayed results
    # The default value is page_size = 1
    if setup.lineEdit_PageSize.text() == '':
        page_size = int(1)
    else:
        page_size = int(setup.lineEdit_PageSize.text())

    # Function_crawler: Get movie information from Douban movies, store as a dictionary
    spider_result = Scraper_Douban_Movies.do_crawl_movie(name, page_size)

    # Extract the scores of every movies to prepare for a score sorting
    sort_score = []

    # Get sorted score indexes: The scores of the movies will be sorted from the lowest to the highest, and this variable outputs the indexes of movies of corresponding scores
    sort_score_index = np.argsort(sort_score)

    # Create lists to store certain movie elements in order to insert these elements into local database
    spider_result_name = []
    spider_result_scores = []
    spider_result_character = []
    spider_result_date = []
    spider_result_description = []
    spider_result_url = []

    # Check whether it is successful to retrieve needed movie lists from the Douban Movie website
    for i in range(0, page_size):
        if spider_result[i][0]['name'] == '':
            if i == 0:
                QMessageBox.warning(main_window, 'Warning', 'No movie found.', QMessageBox.Yes | QMessageBox.No)
            break
        for j in range(0, len(spider_result[i])):
            if spider_result[i][j]['name'] == '': # Double check: delete invalid crawler results
                continue
            else: # Insert every displayed movie elements into corresponding lists
                spider_result_name.append(spider_result[i][j]['name'])
                spider_result_scores.append(spider_result[i][j]['scores'])
                spider_result_character.append(spider_result[i][j]['character'])
                spider_result_date.append(spider_result[i][j]['date'])
                spider_result_description.append(spider_result[i][j]['description'])
                spider_result_url.append(spider_result[i][j]['detail_url'])
                if spider_result[i][j]['scores'] == '':
                    sort_score.append(0)
                else:
                    sort_score.append(float(spider_result[i][j]['scores']))
        # Get sorted score indexes:
        # The scores of the movies will be sorted from the lowest to the highest
        # This variable outputs the indices of movies of corresponding scores
        sort_score_index = np.argsort(sort_score)

    # Function_Result display
    Index = 0
    for i in range(0, len(spider_result_name)):
        score_index = sort_score_index[len(spider_result_name) - 1 - i]
        main_window.tableWidget_SpiderResult.insertRow(Index)
        main_window.tableWidget_SpiderResult.setItem(Index, 0, QTableWidgetItem(spider_result_name[score_index]))
        main_window.tableWidget_SpiderResult.setItem(Index, 1, QTableWidgetItem(spider_result_scores[score_index]))
        main_window.tableWidget_SpiderResult.setItem(Index, 2, QTableWidgetItem(spider_result_character[score_index]))
        main_window.tableWidget_SpiderResult.setItem(Index, 3, QTableWidgetItem(spider_result_date[score_index]))
        main_window.tableWidget_SpiderResult.setItem(Index, 4, QTableWidgetItem(spider_result_description[score_index]))
        main_window.tableWidget_SpiderResult.setItem(Index, 5, QTableWidgetItem(spider_result_url[score_index]))
        Index += 1

    if sign_or_unsign_flag == False: # Global variable sign_or_unsign_flag: User system_Registered_or_Unregistered users
        return  # variable == false: Unsigned user, will not go through the program below->No history stored

    # Function_History: Global variable filename: Track the path of uploaded photos
    global filename
    photo_url = filename

    # Function_History: Insert defined elements into history database
    for i in range(0, len(spider_result_name)):
        History_Database.sqlite_insert(username_Hash_database, local_time, photo_url, name, spider_result_name[i], spider_result_url[i])

    global Local_Movie_Database
    Local_Movie_Database = Local_Database.sqlite_list()
    COUNTER = 0
    for i in range(0, len(spider_result_name)):
        COUNTER = 0
        for j in range(0, len(Local_Movie_Database)):
            if spider_result_name[i] == Local_Movie_Database[j][4]:
                COUNTER = -1
                break
        if COUNTER < 0:
            continue
        # Function_Local_Database: Insert elements into local database for the use for offline users
        Local_Database.sqlite_insert(username_Hash_database, local_time, photo_url, name, spider_result_name[i], spider_result_scores[i], spider_result_character[i], spider_result_date[i], spider_result_description[i])

    Local_Movie_Database = Local_Database.sqlite_list()

# When users click 'Offline' button, the system will do this operation
def offline(name):
    Index = 0
    global Local_Movie_Database
    Local_Movie_Database = Local_Database.sqlite_list()
    movie_name = []
    sort_score = []
    for i in range(0, len(Local_Movie_Database)):
        if name == Local_Movie_Database[i][3]:
            movie_name.append(Local_Movie_Database[i])

    for i in range(0, len(movie_name)):
        if movie_name[i][5] == '':
            sort_score.append(0)
        else:
            sort_score.append(float(movie_name[i][5]))

    sort_score_index = np.argsort(sort_score)

    COUNTER = 0
    # Function_Result_Display:
    # Offline users will gain results from local database.
    # But they will not be able to access the hyperlink and choose the number of the results
    for i in range(0, len(movie_name)):
        score_index = sort_score_index[len(movie_name)-1-i]
        main_window.tableWidget_SpiderResult.insertRow(Index)
        main_window.tableWidget_SpiderResult.setItem(Index, 0, QTableWidgetItem(movie_name[score_index][4]))
        main_window.tableWidget_SpiderResult.setItem(Index, 1, QTableWidgetItem(movie_name[score_index][5]))
        main_window.tableWidget_SpiderResult.setItem(Index, 2, QTableWidgetItem(movie_name[score_index][6]))
        main_window.tableWidget_SpiderResult.setItem(Index, 3, QTableWidgetItem(movie_name[score_index][7]))
        main_window.tableWidget_SpiderResult.setItem(Index, 4, QTableWidgetItem(movie_name[score_index][8]))
        main_window.tableWidget_SpiderResult.setItem(Index, 5, QTableWidgetItem('Url is not available in this module.'))
        Index += 1
        COUNTER = -1

    if COUNTER == 0:
        QMessageBox.warning(main_window, 'Warning', 'No movie found under offline condition.', QMessageBox.Yes | QMessageBox.No)

# OOPs
# Function & User system_Registration_Sign interface:
# Sign_Dialog_Interface Ui:
# After clicking the 'want to sign' button, this dialog will be shown and users can come up with their usernames and passwords
class sign_dialog_interface(Sign_Dialog_Interface.Ui_Dialog,QtWidgets.QDialog):
    # Initialize QT interface
    def __init__(self):
        super(sign_dialog_interface, self).__init__()
        self.setupUi(self)
        # Function_Sign_Hide password: change inputted password into '*******'
        self.lineEdit_Password_Sign.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_ConfirmPassword_Sign.setEchoMode(QtWidgets.QLineEdit.Password)

    # When user clicks on 'OK', following programs will operate
    def accept(self):
            # Get users' input
            UserName_Sign = self.lineEdit_Username_Sign.text()
            Password_Sign = self.lineEdit_Password_Sign.text()
            ConfirmPassword_Sign = self.lineEdit_ConfirmPassword_Sign.text()

            # Check whether the password is appropriate
            if Password_Sign != ConfirmPassword_Sign:
                # Interface_Error verification: Remind users to confirm their passwords
                QMessageBox.warning(self, 'Error', 'Please confirm your password.',
                                            QMessageBox.Yes | QMessageBox.No)
                return

            # Function_Registration_Sign_Haxi encryption: Encrypt users' information to raise data security
            UserName_Sign_Hash = Hash.UserName_Hash(UserName_Sign)
            Password_Sign_Hash = Hash.Password_Hash(Password_Sign)
            print(UserName_Sign_Hash)

            # Use a function to check whether the username is valid, whether it is signed by another user
            res_register = User_Database.sqlite_find(UserName_Sign_Hash)

            # Interface_Error verification: Remind users that their usernames have already been used
            if res_register:
                QMessageBox.warning(self, 'Error', 'Username is unavailable. Please design a new one.',
                                            QMessageBox.Yes | QMessageBox.No)
                return
            # Interface_Successful verification: Show users that they have signed their accounts successfully
            else:
                User_Database.sqlite_insert(UserName_Sign_Hash,Password_Sign_Hash) # Function_User database: Insert usernames and passwords into user database
                QMessageBox.warning(self, 'Congratulation', 'Registered successfully!', QMessageBox.Yes | QMessageBox.No)
                sign_dialog.close() # Sign interface will be automatically closed after a successful registration

# Function_Sign window: Sign_Window_Interface Ui: Users can choose 'signed', 'unsigned', and 'want to sign' buttons
class manage_sign_window(Sign_Window_Interface.Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super(manage_sign_window, self).__init__()
        self.setupUi(self)

    # Operations when the user clicks on 'signed user' button
    def signeduserLoginAccept(self):
        log_window.show() # Function_Login
        global sign_or_unsign_flag
        sign_or_unsign_flag = True # Signed user

    # Operations when the user clicks on 'unsigned user' button
    def unsigneduserMainAccept(self):
        # User system_Unsigned users:
        # Unsigned users cannot access to their history results, so the 'history' button will be disabled
        main_window.pushButton_History.setDisabled(True)
        main_window.showMaximized()
        global sign_or_unsign_flag
        sign_or_unsign_flag = False
        self.close() # After showing main interface, sign window will be closed automatically

    # Operations when the user clicks on 'want to sign' button
    def signinguserDialogAccept(self):
        sign_dialog.show() # Function_Sign

# Function_Login: Login_Interface Ui:
# When users clikc on 'signed' button, this dialog will be displayed. Users  need to input the registered 'username' and 'password'
class login_window(Login_Dialog_Interface.Ui_login,QtWidgets.QDialog):
    def __init__(self):
        super(login_window, self).__init__()
        self.setupUi(self)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)

    # Operations after the user click 'OK' button in the login interface
    def accept(self):
        # Get input username and password typed by the client
        global username
        username = self.lineEdit_user.text()
        password = self.lineEdit_password.text()

        # Function_Registration_Haxi encryption: Encrypt users' information
        username_Hash = Hash.UserName_Hash(username)
        password_Hash = Hash.UserName_Hash(password)
        global username_Hash_database
        username_Hash_database = username_Hash

        # Use a function to check whether the usernames and passwords that users input can be found in user database
        res_login = User_Database.sqlite_login(username_Hash,password_Hash)

        # Operations when usernames and passwords can be found in database
        if res_login:
            # show main window and hide login window
            main_window.showMaximized()
            main_sign_window.close()
            log_window.close()
        else:
            global g_login_error_counter
            g_login_error_counter += 1
            if (g_login_error_counter >= 3):
                # If error more than 3 times, quit
                QMessageBox.warning(self, 'Warning', 'You have typed the wrong information for three times. The system will quit.', QMessageBox.Yes | QMessageBox.No)
                quit()
            # Interface_Error verification: If passwords or usernames cannot be found in database, remind users to try again
            self.lineEdit_user.setText("")
            self.lineEdit_password.setText("")
            QMessageBox.warning(self,'Error','Username or password error! Please try again',QMessageBox.Yes | QMessageBox.No)

# User system_Registered users:
# Main_Interface Ui: Once the user passes the login process, they will go to main interface
class manage_main_window(Main_Interface.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(manage_main_window, self).__init__()
        self.setupUi(self)
        # Function_Result display: Insert tables with a defined arrangement
        self.tableWidget_SpiderResult.setColumnCount(6)
        self.tableWidget_SpiderResult.setHorizontalHeaderLabels(['name','scores','character','date','description','detail_url'])
        self.tableWidget_ShowTag.setColumnCount(1)
        self.tableWidget_ShowTag.horizontalHeader().setVisible(False)

        # Set word fonts
        self.tableWidget_SpiderResult.setFont(QFont('song', 8))
        self.tableWidget_ShowTag.setFont(QFont('song', 8))
        self.tableWidget_SpiderResult.horizontalHeader().setFont(QFont('song', 8))

    # Function_Photo input: Users can upload their movie posters after clicking on 'Choose File' button
    def ChooseFile(self):
        Index = 0 # Define a variable to track the number of photos uploaded in once
        # User system_Configuration:
        # Variable Upload_size: Users can change the number of photos they want to upload in once, the default value is 1
        if setup.lineEdit_UploadSize.text() == '':
            Upload_size = int(1)
        else:
            Upload_size = int(setup.lineEdit_UploadSize.text())

        # Get the width and height information of tag tables in order to better define the size of each tag
        width = self.tableWidget_ShowTag.width()
        height = self.tableWidget_ShowTag.height()
        self.tableWidget_ShowTag.setColumnWidth(0, width)

        # Function_Photo display: Users can see their uploaded photos
        self.tableWidget_ShowPhoto.setColumnCount(3)
        self.tableWidget_ShowPhoto.setRowCount(1)
        self.tableWidget_ShowPhoto.verticalHeader().setVisible(False)
        self.tableWidget_ShowPhoto.horizontalHeader().setVisible(False)
        self.tableWidget_ShowPhoto.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_ShowPhoto.setIconSize(QSize(width / 3, height))
        for i in range(3):
            self.tableWidget_ShowPhoto.setColumnWidth(i, width / 3)
        for j in range(1):
            self.tableWidget_ShowPhoto.setRowHeight(j, height)

        Counter = 0
        photo_words_result = [] # Variable photo_words_result: Contain the text contents disposed from uploaded photos
        while Index < Upload_size:
            Filename, filetype = QFileDialog.getOpenFileName(self, "Please choose a file", "./")
            global filename
            filename = Filename # Global variable filename: Track the path of uploaded photos and will be inserted in history database
            if len(filename) == 0:
                return

            photo = QTableWidgetItem()
            photo.setFlags(Qt.ItemIsEnabled)
            photo_icon = QIcon(filename)
            photo.setIcon(QIcon(photo_icon))
            self.tableWidget_ShowPhoto.setItem(0, Index, photo)

            # Function API: to get text contents from the photos
            words_result = BaiduAI_API.Translatephoto(filename)

            # Interface_Error verification: Check whether the text contents of photos are identifiable
            if len(words_result) == 0:
                QMessageBox.warning(self, 'Warning', 'The words on the uploaded photo are not identifiable.', QMessageBox.Yes | QMessageBox.No)
            else:
                for i in range(0, len(words_result)):
                    Counter += 1
                    photo_words_result.append(words_result[i]['words']) # Append text contends to the variable photo_words_result

            Index += 1

        # Function_Tag display: Display text contents in a tag form. Users can click on their interested tags as a searching object
        self.tableWidget_ShowTag.setRowCount(Counter)
        for i in range(Counter):
            self.tableWidget_ShowTag.setRowHeight(i, height / Counter)
            self.tableWidget_ShowTag.setItem(i, 0, QTableWidgetItem(photo_words_result[i]))

    # Do crawler based on selected tag
    def s_open_tag(self, QTableWidgetItem_P):
        tag = QTableWidgetItem_P.text()
        # User system_Choose identities: Check whether users click 'offline' button
        if setup.radioButton_Offlineusers.isChecked():
            offline(tag)
        else:
            spider(tag)

    # Function_Type input: Users can type in the information they would like to search
    def TypeText(self):
        main_window_dialog.show() # Users can type in their information in main_window_dialog interface

    # Function_History: For signed users, when they click on 'History' button, history results will be displayed
    def History(self):
        user_history_db = []
        # Set tables in a defined arrangement to better display the results
        history_result.tableWidget_Historyresult.setColumnCount(6)
        history_result.tableWidget_Historyresult.setHorizontalHeaderLabels(['username', 'local_time', 'photo_url', 'tag', 'movie_name', 'movie_url'])
        history_result.tableWidget_Historyresult.horizontalHeader().setFont(QFont('song', 8))
        history_result.tableWidget_Historyresult.setFont(QFont('song', 8))
        history_result.showMaximized()
        history_db_list = History_Database.sqlite_list()
        for i in range(0,len(history_db_list)):
            # Select history movie results of a particular user from history database
            if history_db_list[i][0] == username_Hash_database:
                user_history_db.append(history_db_list[i])
            else: # Interface_Error verification: Remind users that they haven't had history results yet
                history_result.tableWidget_Historyresult.setItem(0, 0, QTableWidgetItem('No history found.'))

        history_result.tableWidget_Historyresult.setRowCount(0)
        history_result.tableWidget_Historyresult.clearContents() # Redundant history results will be removed each time

        # Display results
        for j in range(0, len(user_history_db)):
            history_result.tableWidget_Historyresult.insertRow(j)
            global username
            history_result.tableWidget_Historyresult.setItem(j, 0, QTableWidgetItem(username))
            history_result.tableWidget_Historyresult.setItem(j, 1, QTableWidgetItem(user_history_db[len(user_history_db)-j-1][1]))
            history_result.tableWidget_Historyresult.setItem(j, 2, QTableWidgetItem(user_history_db[len(user_history_db)-j-1][2]))
            history_result.tableWidget_Historyresult.setItem(j, 3, QTableWidgetItem(user_history_db[len(user_history_db)-j-1][3]))
            history_result.tableWidget_Historyresult.setItem(j, 4, QTableWidgetItem(user_history_db[len(user_history_db)-j-1][4]))
            history_result.tableWidget_Historyresult.setItem(j, 5, QTableWidgetItem(user_history_db[len(user_history_db)-j-1][5]))

    # Function_Hyperlink: Users can click the hyperlinks of their displaying results to get detailed information and watching address
    def s_open_url(self,QTableWidgetItem_P):
        # Get hyperlink
        Url_result = QTableWidgetItem_P.text()
        if Url_result.startswith('http'):
            web.open(Url_result) # Use webbrowser to open the hyperlink in an online situation

    # Function_Configuration: When user clicks on 'Configuration' button, this dialog shows
    def SetUp(self):
        setup.show()

# Function_Type input:
# Main_Interface_Dialog QT:
# When uses click on 'Type text' button on the main interface, this dialog will be shown
class main_interface_dialog(Main_Interface_Dialog.Ui_Dialog,QtWidgets.QDialog):
    def __init__(self):
        super(main_interface_dialog, self).__init__()
        self.setupUi(self)

    # When user clicks on 'OK' button, the following program will be operated
    def accept(self):
        self.close()
        # Get the information users want to search
        moviename = self.lineEdit_Usertypein.text()
        if setup.radioButton_Offlineusers.isChecked():
            offline(moviename)
        # Function_crawler: Do crawler
        else:
            spider(moviename)

# Function_Configuration: Setup_Dialog Ui: When users click on 'Configuration' button, this dialog will be shown
class setup_dialog(SetUp_Dialog.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self):
        super(setup_dialog, self).__init__()
        self.setupUi(self)

# Function_History: History_Widget Ui: When users click on 'History' button, this widget will be shown
class history_result(History_Widget.Ui_Form, QtWidgets.QWidget):
    def __init__(self):
        super(history_result, self).__init__()
        self.setupUi(self)

    def s_open_url(self,QTableWidgetItem_P):
        Url_result = QTableWidgetItem_P.text()
        if Url_result.startswith('http'):
            web.open(Url_result)

# main command
if __name__ == '__main__':
    print("start")
    app = QtWidgets.QApplication(sys.argv)

    main_sign_window = manage_sign_window()

    main_sign_window.show()

    log_window = login_window()

    main_window = manage_main_window()

    main_window_dialog = main_interface_dialog()

    history_result = history_result()

    setup = setup_dialog()

    sign_dialog = sign_dialog_interface()

    Connect_to_userdatabase_cursor = User_Database.sqlite_creat_table()

    User_sqlite_list = User_Database.sqlite_list()

    Connect_to_localdatabase_cursor = Local_Database.sqlite_creat_table()

    Local_sqlite_list = Local_Database.sqlite_list()

    Connect_to_historydatabase_cursor = History_Database.sqlite_creat_table()

    History_sqlite_list = History_Database.sqlite_list()

    sys.exit(app.exec_())
