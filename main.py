#here we write the logic of the program
import glob
import json
import random
import smtplib
import time
from pathlib import Path
from datetime  import datetime
from kivy.app import App  #main object
from kivy.uix.image import Image
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder #for connecting py file with kv file
from kivy.uix.screenmanager import ScreenManager,Screen # for managing multiple screens of application,default Screenmanager displays only one screen at a time
from kivy.core.window import Window         #to change the background color of kivy

#Window.clearcolor=(217/255.0, 231/255.0, 248/255.0,1)
Window.clearcolor=(14/255.0,33/255.0,77/255.0,1)     #rgba


Builder.load_file('design.kv')  #loading the kv file
# we need to create classes with same name as screen names in the kv
sender_email="abtdevtest@gmail.com"
to_address=""

class LoginScreen(Screen):      #inherited from the screen object
    def sign_up(self):
       
        self.manager.current="sign_up_screen"  #manager is a property of screen and current is a property of manager ,which gives the name of the necxt screen it should go

    def login(self,uname,pword):
        with open("users.json") as infile:
            users=json.load(infile)
        if uname=="" or pword=="":
            self.ids.login_wrong.text="Please enter the credentials to Login!"
        elif uname in users and users[uname]['password']==pword:
            self.manager.current="loginScreenSuccess" 
     
        else:
            self.ids.login_wrong.text="Wrong Username or Password"


    def forgot_password(self):
        self.manager.current="forgot_password"
    




class RootWidget(ScreenManager) : #root needs to be inherited from the screen manager
    pass


class SignUpScreen(Screen):
    def add_user(self,uname,pword):
        with open("users.json") as infile:
            users=json.load(infile) #loading all the content as a single dictionary
        if uname=="" or pword=="":
            self.ids.noinput.text="Please fill in the credentials to sign up!"
        elif uname in users and users[uname]['password']==pword :
            self.ids.noinput.text="Oops Looks like we already have an account with you,Try Forget password or Login."   

            

        else:
            users[uname]={'username':uname,'password':pword,'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
            with open("users.json",'w') as infile:
                json.dump(users,infile)
            self.manager.current="sign_up_page_success"
    def log_out(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"
        
    
class ForgotPassword(Screen):
    def check_user(self,uname):
       l=[]
       with open ("users.json","r") as infile:
            users=json.load(infile)
            if uname in users:
                pword1=users[uname]['password']
                #print(pword1)
                    
                self.manager.current="forgotpasswordSuccessMessage"
            else:
                print("no")
                self.manager.current="forgotpasswordFailedMessage"
    def log_out(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"
class ForgotPassSuccess(Screen):
    def back_to_home(self,email_user,uname):
        if email_user=="" or uname=="":
            self.ids.mess.text="Please enter the credentials to continue"
        else:
            with open ("users.json") as file:
                users=json.load(file)
            if uname in users:
                pword=users[uname]['password']
                to_address=email_user
                password="Pythontest123"
                message="Hi there,Please use {pwd} as password to login Thank you!".format(pwd=pword)
                server=smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login(sender_email,password)
                self.manager.current="login_screen"
                print("login success")
                server.sendmail(sender_email,to_address,message)
                print("email sent")     
            else:
                self.manager.current="login_screen"
    def log_out(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"

class ForgotPassFail(Screen):
    def new_sign_in(self):
        self.manager.transition.direction="left"
        self.manager.current="sign_up_screen"



class SignUpScreenSuccess (Screen):
    def go_to_login(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"    
   
class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"
    def get_affirm(self):
        
        available_affr=glob.glob("Affirmation/*txt")  #to load the folder with text files
        available_affr=[Path(filename).stem for filename in available_affr]     #using the pathlib libraray to obtain the anme of the file,using stem to get just the filename without any ext
        with open("Affirmation/Affirmations.txt") as file:
            quotes=file.readlines()
            
            
                
        
        self.ids.affirmation.text=random.choice(quotes)

       
class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass



class MainApp(App):     #inherited from the main app
    def build(self):    #build() is a method of App
        return RootWidget()


if __name__=="__main__":            #calling the main app
    MainApp().run()                    #calling the run() of the App