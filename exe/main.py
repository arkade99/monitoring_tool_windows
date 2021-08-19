import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
import time,datetime,sys
import MouseTest
import login_api
import MouseTest
import Screenshot_final
import threading
import sys
 
class WelcomeScreen(QDialog):
    login_user_id = 0
    insert_id = 0
    user_id = 0
    mouse = 0    
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui",self)
        self.login.clicked.connect(self.gotologin)

    def gotologin(self):
        login_id = self.login_id.text()
        #print(login_id)
        login_password = self.login_password.text()
        #print(login_password)
        login_json = login_api.login_api_check(login_id,login_password)
        if(login_json["success"] == True):
            #print(login_json)
            login = Login()
            WelcomeScreen.login_user_id = login_id
            print(WelcomeScreen.login_user_id)
            WelcomeScreen.insert_id = login_json['insert_id']
            WelcomeScreen.user_id = login_json['user_id']
            #print("User Id"+WelcomeScreen.user_id)
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
            mouse = threading.Thread(name='daemon', target=login.runMouseAndScreenshot)  
            mouse.setDaemon(True)
            mouse.start()
            

        else:
            print("LogIn Failed")
            sys.exit()
        

    
        #files = {'company_code': 104,'username':login_id,'password': login_password,'in_time': image_file_descriptor}
        #url = 'http://122.163.121.176/infra_05_07_2021/desktop_api/webservice/screen_documantion'
        #r = requests.post(url, data=files)





class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui",self)
        self.logout.clicked.connect(self.gotoWelcomeScreen)
        self.settings.clicked.connect(self.gotoSetting)        

    def runMouseAndScreenshot(self):
        temp_new_time = 0
        count = 0
        duration = 0
        temp_duration =0
        old_time = 0
        curr_time = time.time()
        while True:
            temp_time = old_time
            if(duration == 0):
                old_time = datetime.datetime.fromtimestamp(time.time())
                MouseTest.insertMouseApi(temp_duration,temp_time,temp_new_time,WelcomeScreen.user_id)
            temp_duration = duration
            temp_new_time = datetime.datetime.fromtimestamp(time.time())
            duration = MouseTest.get_idle_duration()
            #print (duration)
            next_time =  time.time()
            diff = next_time - curr_time
            if(diff >= 20):
                x = time.time()
                path = r'screenshot'+WelcomeScreen.login_user_id+str(x)+'.jpeg'
                Screenshot_final.scr(path,WelcomeScreen.user_id)
                curr_time = time.time()
            self.logout.clicked.connect(self.gotoWelcomeScreen)
            self.settings.clicked.connect(self.gotoSetting)          
            time.sleep(1)

    def gotoWelcomeScreen(self):
        res = login_api.logout_api_check(WelcomeScreen.insert_id)
        if(res["success"] == True):
            welcome = WelcomeScreen()
            #print(WelcomeScreen.login_user_id)
            widget.addWidget(welcome)
            widget.setCurrentIndex(widget.currentIndex()+1)
            sys.exit()            
        else:
            #print("Failed to Logout")
            sys.exit()

    def gotoSetting(self):
        setting = Setting ()
        widget.addWidget (setting)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Setting(QDialog):
    def __init__(self):
        super(Setting, self).__init__()
        loadUi("setting.ui",self)
        self.back.clicked.connect(self.gotologin)

    def gotologin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)


#main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
welcome = WelcomeScreen()
widget.addWidget(welcome)
widget.setFixedHeight(300)
widget.setFixedWidth(300)
widget.show()
sys.exit(app.exec_())
