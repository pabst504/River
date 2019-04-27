import os, sys
import sqlite3
import requests
import webbrowser
import time
import pyautogui
import threading


from time import sleep
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit ,QTableWidget, QTableWidgetItem, QLabel, QListWidget
from PyQt5.QtCore import QSize



def createplaylist(playlist):
    playlist = playlist.replace(' ','')
    conn = sqlite3.connect(os.path.join('catalog.db'))
    conn.execute("CREATE TABLE IF NOT EXISTS " + playlist + "(ID text, Runtime text)")


def populate(playlist, url):

    playlist = playlist.replace(' ','')
    urlData = requests.get(url)
    htmltext = urlData.text    

    dex = htmltext.find("episodeId")
    dex2 = htmltext.find("runtime", dex)

    while(dex != -1 and dex2 != -1):
        epID = [ htmltext[dex + 11], htmltext[dex + 12], htmltext[dex + 13], htmltext[dex + 14],
                 htmltext[dex + 15], htmltext[dex + 16], htmltext[dex + 17], htmltext[dex + 18] ]
        
        rT = [htmltext[dex2 + 9], htmltext[dex2 + 10], htmltext[dex2 + 11], htmltext[dex2 + 12]]
        newID = ''.join(epID)
        newrT = ''.join(rT)
        
        dex = htmltext.find("episodeId", dex + 18)
        dex2 = htmltext.find("runtime\":", dex2 + 12)

        conn = sqlite3.connect(os.path.join('catalog.db'))
        cur = conn.cursor()
        sqlinput = "INSERT INTO "+playlist+ " (ID, Runtime) VALUES (?,?)"
        cur.execute((sqlinput) , [str(newID), str(newrT)])
        conn.commit()

def random(playlist):
 
        playlist = playlist.replace(' ','')
        conn = sqlite3.connect(os.path.join('catalog.db'))
        cur = conn.cursor()
        sqlinput = ("SELECT * FROM "+playlist+" ORDER BY RANDOM() LIMIT 1;")
        cur.execute(sqlinput)
        output = cur.fetchall()

        playTV(output)

def playTV(random):

    showID = random[0][0] 
    runtime = random[0][1]
    runtime = int(runtime)
    
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    base = 'http://www.netflix.com/watch/'
    target = ''.join([base,showID])

    webbrowser.get(chrome_path).open_new(target)
    time.sleep(10) 
    pyautogui.hotkey('command','w')

    
def populatelist(self):
    conn = sqlite3.connect(os.path.join('catalog.db'))
    cur = conn.cursor()

    cur.execute('select name from sqlite_master where type =' + " 'table'; " )

    output = cur.fetchall()

    for i in range(0, len(output)):
        self.plist.addItem(output[i][0])

def delete(ITEM):
    conn = sqlite3.connect(os.path.join('catalog.db'))
    cur = conn.cursor()
    cur.execute("drop table if exists " + ITEM)
    

class main(QMainWindow):

    ITEM = ''
    def __init__(self):
        super().__init__()
        self.title = "RIVER"
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, 400, 500)
        self.initUI()
        
    def initUI(self):


        l1 = QLabel(" Playlist Name", self)
        l2 = QLabel(" Add TV shows", self)
        l3 = QLabel(" Netflix URL", self)

        l1.move(0,0)
        l2.move(0, 50)
        l3.move(0, 85)
        

        self.playlist = QLineEdit(self)
        self.playlist.resize(200,25)
        self.playlist.move(100,0)

        self.URL = QLineEdit(self)
        self.URL.resize(200,25)
        self.URL.move(100, 85)

        

        url = QPushButton('Add', self)
        url.clicked.connect(self.clickMethod)
        url.move(300, 85)


        

        playBtn = QPushButton("Play", self)
        playBtn.clicked.connect(self.plist_play)
        playBtn.move(100, 450)



        deleteBtn = QPushButton("Delete", self)
        deleteBtn.clicked.connect(self.plist_delete)
        deleteBtn.move(0,450)

        self.crtBtn = QPushButton('Create', self)

        self.crtBtn.clicked.connect(self.crt)

        self.crtBtn.move(300 , 0)


        self.plist = QListWidget(self)
        self.plist.move(0,150)
        self.plist.resize(400,250)
        
        
        self.plist.itemClicked.connect(self.plist_item)

        populatelist(self) 


    def plist_play(self):
        global ITEM
        while True:
            random(ITEM)
        #some form of check to see if it should loop again
        
                    

    def plist_delete(self):
        global ITEM
        delete(ITEM)
        x  = self.plist.currentRow()
        self.plist.takeItem(x)
        
        
    def clickMethod(self):
        global ITEM
        x = self.URL.text()
        if ".com" not in x:
             self.URL.setText('')
        else:
            populate(ITEM, x)
            self.URL.setText('')

    def plist_item(self, item):
        global ITEM
        ITEM = str(item.text())
        
        
    def crt(self):
        ply = self.playlist.text()
        createplaylist(ply)
        self.plist.addItem(ply) 



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    mainWin = main()
    mainWin.show()
    sys.exit( app.exec_() )
