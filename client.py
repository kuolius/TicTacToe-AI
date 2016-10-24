# Echo client program
import socket
import threading
import time
import pickle
import random
import memedit
import queue

import tkinter
from tkinter import messagebox
from tkinter import ttk


gameDown=False
waitingScreen=True
opponentScreen=False
playingScreen=False
waitOpScreen=False
controlerStarted=False
messengerRunning=False
connectScreen=False
mLeft=False
#wOSexec=False
wSexec=False
pSexec=False
oSexec=False
FPS=100
HOST = '127.0.0.1' 
MS=None
txt=""

class Win():
	def __init__(self,n):
		self.sp=[" " for i in range(n)]
	def get_sp(self,coord):
		return self.sp[coord]
	def set_sp(self,coord,yturn="x"):
		self.sp[coord]=yturn
	def set_contr(self,coord,opturn="o"):
		self.sp[coord]=opturn
		
class Application(tkinter.Tk):
	def __init__(self,master=None):
		tkinter.Tk.__init__(self,master)
		self.n=33
		self.win=[[] for i in range(self.n)]
		for i in range(self.n):
			self.win[i]=Win(self.n)
		self.f=open("load.ini","rb")
		self.load=pickle.load(self.f)
		self.messenger=None
		self.gameWin=False
		self.gameLost=False
		self.oturn=False
		self.f=open("mem.txt","rb")
		self.mem=pickle.load(self.f)
		self.que=queue.Queue()
		self.f.close()
		self.movm=[]
		self.mov=[0,0]
		self.omov=[0,0]
		self.lbound=0
		self.rbound=0
		self.ubound=0
		self.dbound=0
		self.boundwidth=0
		self.boundheight=0
		self.yturn="x"
		self.opturn="o"
		self.move=None
		self.wd=self.load[0]
		self.hg=self.load[1]
		self.menuTop=self.hg/2-10
		self.i=0
		self.j=0
		self.x=120
		self.y=120
		self.scrollWidth=self.load[2]
		self.f.close()
		self.speed=2
		self.boundX=1000-self.wd+280
		self.boundY=1000-self.hg+280
		self.animIndex=0
		self.canva=tkinter.Canvas(width=self.wd, height=self.hg)
		#self.update_map()
		self.canva.focus_force()
		self.canva.pack()
		self.protocol("WM_DELETE_WINDOW",self.terminateThreadsQue)
		self.ex=False
		self.isReady=True
		self.updateQue()
		self.menuScreenQue()
		
		
	def updateQue(self):
		if self.que.qsize()>0:
			while True:
				array=self.que.get_nowait()
				func=array[0]
				args=array[1:]
				func(*args)
				if self.que.qsize()<=0:
					break
		self.after(10,self.updateQue)
		
	
	def sdScreenQue(self):
		self.que.put([self.sdScreen])
	
	def sdScreen(self):
		global connectScreen
		connectScreen=False
		self.canva.delete("all")
		"""self.canva.create_text(self.wd/2,self.menuTop,text=HOST+" server is down.",font=('Arial',15,"bold"))
		self.canva.unbind("<Button-1>")
		self.canva.unbind('<Motion>')
		self.canva.unbind("<Enter>")
		time.sleep(.5)
		self.canva.create_text(self.wd/2,self.menuTop+20,text="Returning to menu.",font=('Arial',15,"bold"))
		time.sleep(.5)"""
		messagebox.showerror("Error 1:",HOST+" is down.")
		self.menuScreenQue()
		
	def menuScreenQue(self):
		self.que.put([self.menuScreen])
		
	def menuScreen(self):
		#self.canva.pack_forget()
		self.canva.unbind_all("<Button-1>")
		self.canva.unbind('<Motion>')
		self.canva.unbind("<Enter>")
		global HOST
		self.f=open("load.ini","rb")
		HOST=pickle.load(self.f)[3]
		#print(HOST)
		self.canva.delete("all")
		self.canva.create_text(self.wd/2,self.menuTop,text="Multiplayer",font=('Arial',15,"bold"))
		self.canva.create_text(self.wd/2,20+self.menuTop,text="Singleplayer",font=('Arial',15,"bold"))
		self.canva.create_text(self.wd/2,40+self.menuTop,text="Set ip address",font=('Arial',15,"bold"))
		self.canva.create_text(self.wd/2,60+self.menuTop,text="Resolution",font=('Arial',15,"bold"))
		self.canva.create_text(self.wd/2,80+self.menuTop,text="Exit",font=('Arial',15,"bold"))
		self.canva.pack()
		self.canva.bind('<Motion>',self.menuAnimeQue)
		self.canva.bind("<Enter>",self.menuAnimeQue)
		self.canva.bind("<Button-1>",self.findMatchQue)
	
	def menuAnimeQue(self,event):
		self.que.put([self.menuAnime,event])
	
	def menuAnime(self,event):
		for i in range(5):
			if event.x>self.wd/2-50 and event.x<self.wd/2+50 and event.y>self.menuTop-10+20*i and event.y<10+self.menuTop+20*i:
				self.canva.delete("all")
				if i==0:
					self.canva.create_text(self.wd/2,self.menuTop,text="Multiplayer",font=('Arial',17,"bold"))
				else:
					self.canva.create_text(self.wd/2,self.menuTop,text="Multiplayer",font=('Arial',15,"bold"))
				if i==1:
					self.canva.create_text(self.wd/2,20+self.menuTop,text="Singleplayer",font=('Arial',17,"bold"))
				else:
					self.canva.create_text(self.wd/2,20+self.menuTop,text="Singleplayer",font=('Arial',15,"bold"))
				if i==2:
					self.canva.create_text(self.wd/2,40+self.menuTop,text="Set ip address",font=('Arial',17,"bold"))
				else:
					self.canva.create_text(self.wd/2,40+self.menuTop,text="Set ip address",font=('Arial',15,"bold"))
				if i==3:
					self.canva.create_text(self.wd/2,60+self.menuTop,text="Resolution",font=('Arial',17,"bold"))
				else:
					self.canva.create_text(self.wd/2,60+self.menuTop,text="Resolution",font=('Arial',15,"bold"))
				if i==4:
					self.canva.create_text(self.wd/2,80+self.menuTop,text="Exit",font=('Arial',17,"bold"))
				else:
					self.canva.create_text(self.wd/2,80+self.menuTop,text="Exit",font=('Arial',15,"bold"))
	
	def findMatchQue(self,event):
		self.que.put([self.findMatch,event])
		
	def findMatch(self,event):
		global connectScreen
		if event.x>self.wd/2-50 and event.x<self.wd/2+50 and event.y>self.menuTop-10 and event.y<10+self.menuTop:
			self.canva.unbind("<Button-1>")
			self.canva.unbind('<Motion>')
			self.canva.unbind("<Enter>")
			global gameDown
			global wSexec
			gameDown=False
			wSexec=False
			connectScreen=True
			self.connectScreenQue()
			find_match()
		elif event.x>self.wd/2-50 and event.x<self.wd/2+50 and event.y>self.menuTop+10 and event.y<30+self.menuTop:
			self.canva.unbind("<Button-1>")
			self.canva.unbind('<Motion>')
			self.canva.unbind("<Enter>")
			self.singlePlayerScreenQue()
		elif event.x>self.wd/2-50 and event.x<self.wd/2+50 and event.y>self.menuTop+30 and event.y<50+self.menuTop:
			self.canva.unbind("<Button-1>")
			self.canva.unbind('<Motion>')
			self.canva.unbind("<Enter>")
			self.setIpScreenQue()
		elif event.x>self.wd/2-50 and event.x<self.wd/2+50 and event.y>self.menuTop+50 and event.y<70+self.menuTop:
			self.canva.unbind("<Button-1>")
			self.canva.unbind('<Motion>')
			self.canva.unbind("<Enter>")
			self.optionScreenQue()
		elif event.x>self.wd/2-50 and event.x<self.wd/2+50 and event.y>self.menuTop+70 and event.y<90+self.menuTop:
			self.terminateThreadsQue()
	
	def setIpScreenQue(self):
		self.que.put([self.setIpScreen])
	
	def setIpScreen(self):
		self.canva.delete("all")
		self.e=tkinter.Entry(self.canva)
		self.canva.create_window(self.wd/2,self.menuTop,window=self.e)
		self.canva.create_text(self.wd/2,20+self.menuTop,text="Save",font=('Arial',15,"bold"))
		self.canva.create_text(self.wd/2,40+self.menuTop,text="Back",font=('Arial',15,"bold"))
		self.canva.bind('<Motion>',self.setIpAnimeQue)
		self.canva.bind("<Enter>",self.setIpAnimeQue)
		self.canva.bind("<Button-1>",self.setIpQue)
	
	def singlePlayerScreenQue(self):
		self.que.put([self.singlePlayerScreen])
	
	def singlePlayerScreen(self):
		self.canva.delete("all")
		self.update_map()
		self.canva.bind_all("<Button-1>",self.mouseClickQue)
		self.canva.bind('<Motion>',self.get_mouseQue)
		self.canva.bind("<Enter>",self.get_mouseQue)
		
	def setIpQue(self,event):
		self.que.put([self.setIp,event])
	
	def setIp(self,event):
		if event.x>self.wd/2-50 and event.x<self.wd/2+50 and event.y>self.menuTop+10 and event.y<30+self.menuTop:
			self.f=open("load.ini","rb")
			matrix=pickle.load(self.f)
			self.f.close()
			self.f=open("load.ini","wb")
			pickle.dump([matrix[0],matrix[1],matrix[2],self.e.get()],self.f)
			self.f.close()
			self.menuScreenQue()
		elif event.x>self.wd/2-50 and event.x<self.wd/2+50 and event.y>self.menuTop+30 and event.y<50+self.menuTop:
			self.menuScreenQue()
		
	def setIpAnimeQue(self,event):
		self.que.put([self.setIpAnime,event])
	
	def setIpAnime(self,event):
		for i in range(1,3):
			if event.x>self.wd/2-50 and event.x<self.wd/2+50 and event.y>self.menuTop-10+20*i and event.y<10+self.menuTop+20*i:
				self.canva.delete("all")
				self.canva.create_window(self.wd/2,self.menuTop,window=self.e)
				if i==1:
					self.canva.create_text(self.wd/2,self.menuTop+20,text="Save",font=('Arial',17,"bold"))
				else:
					self.canva.create_text(self.wd/2,self.menuTop+20,text="Save",font=('Arial',15,"bold"))
				if i==2:
					self.canva.create_text(self.wd/2,40+self.menuTop,text="Back",font=('Arial',17,"bold"))
				else:
					self.canva.create_text(self.wd/2,40+self.menuTop,text="Back",font=('Arial',15,"bold"))
		
	def optionScreenQue(self):
		self.que.put([self.optionScreen])
		
	def optionScreen(self):
		self.canva.delete("all")
		self.canva.create_text(self.wd/2,self.menuTop,text="400x400",font=('Arial',15,"bold"))
		self.canva.create_text(self.wd/2,20+self.menuTop,text="600x600",font=('Arial',15,"bold"))
		self.canva.create_text(self.wd/2,40+self.menuTop,text="800x800",font=('Arial',15,"bold"))
		self.canva.create_text(self.wd/2,60+self.menuTop,text="1000x1000",font=('Arial',15,"bold"))
		self.canva.create_text(self.wd/2,80+self.menuTop,text="back",font=('Arial',15,"bold"))
		self.canva.bind('<Motion>',self.optionAnimeQue)
		self.canva.bind("<Enter>",self.optionAnimeQue)
		self.canva.bind("<Button-1>",self.setResolutionQue)
		
	def optionAnimeQue(self,event):
		self.que.put([self.optionAnime,event])
		
	def optionAnime(self,event):
		for i in range(5):
			if event.x>self.wd/2-50 and event.x<self.wd/2+50 and event.y>self.menuTop-10+20*i and event.y<10+self.menuTop+20*i:
				self.canva.delete("all")
				if i==0:
					self.canva.create_text(self.wd/2,self.menuTop,text="400x400",font=('Arial',17,"bold"))
				else:
					self.canva.create_text(self.wd/2,self.menuTop,text="400x400",font=('Arial',15,"bold"))
				if i==1:
					self.canva.create_text(self.wd/2,20+self.menuTop,text="600x600",font=('Arial',17,"bold"))
				else:
					self.canva.create_text(self.wd/2,20+self.menuTop,text="600x600",font=('Arial',15,"bold"))
				if i==2:
					self.canva.create_text(self.wd/2,40+self.menuTop,text="800x800",font=('Arial',17,"bold"))
				else:
					self.canva.create_text(self.wd/2,40+self.menuTop,text="800x800",font=('Arial',15,"bold"))
				if i==3:
					self.canva.create_text(self.wd/2,60+self.menuTop,text="1000x1000",font=('Arial',17,"bold"))
				else:
					self.canva.create_text(self.wd/2,60+self.menuTop,text="1000x1000",font=('Arial',15,"bold"))
				if i==4:
					self.canva.create_text(self.wd/2,80+self.menuTop,text="back",font=('Arial',17,"bold"))
				else:
					self.canva.create_text(self.wd/2,80+self.menuTop,text="back",font=('Arial',15,"bold"))
	
	def setResolutionQue(self,event):
		self.que.put([self.setResolution,event])
	
	def setResolution(self,event):
		for i in range(4):
			if event.x>self.wd/2-50 and event.x<self.wd/2+50 and event.y>self.menuTop-10+20*i and event.y<10+self.menuTop+20*i:
				self.wd=400+200*i
				self.hg=400+200*i
				self.menuTop=self.hg/2-10
				self.boundX=1000-self.wd+280
				self.boundY=1000-self.hg+280
				self.scrollWidth=self.wd/10
				self.canva.config(width=self.wd,height=self.hg)
				self.f=open("load.ini","rb")
				matrix=pickle.load(self.f)
				self.f.close()
				self.f=open("load.ini","wb")
				pickle.dump([self.wd,self.hg,self.scrollWidth,matrix[3]],self.f)
				self.f.close()
				self.optionScreenQue()
		if event.x>self.wd/2-50 and event.x<self.wd/2+50 and event.y>self.menuTop-10+80 and event.y<10+self.menuTop+80:
			self.menuScreenQue()
	
	def terminateThreadsQue(self):
		self.que.put([self.terminateThreads])
		
	def terminateThreads(self):
		global gameDown
		global waitingScreen
		
		gameDown=True
		waitingScreen=False
		#time.sleep(1)
		self.quit()
		
	def connectScreenQue(self):
		self.que.put([self.connectScreen])
		
	def connectScreen(self):
		if connectScreen:
			self.canva.unbind_all("<Button-1>")
			self.canva.unbind('<Motion>')
			self.canva.unbind("<Enter>")
			self.canva.delete("all")
			if self.animIndex==0:
				self.text=self.canva.create_text(self.wd/2,self.hg/10,text="Connecting to the server via "+HOST+".",font=('Arial',15,"bold"))
			elif self.animIndex==1:
				self.text=self.canva.create_text(self.wd/2,self.hg/10,text="Connecting to the server via "+HOST+"..",font=('Arial',15,"bold"))
			elif self.animIndex==2:
				self.text=self.canva.create_text(self.wd/2,self.hg/10,text="Connecting to the server via "+HOST+"...",font=('Arial',15,"bold"))
			elif self.animIndex==3:
				self.text=self.canva.create_text(self.wd/2,self.hg/10,text="Connecting to the server via "+HOST+"....",font=('Arial',15,"bold"))
			self.animIndex=(self.animIndex+1)%4
			self.canva.pack()
			self.after(1500,self.connectScreen)
	
	def waitingScreenQue(self):
		self.que.put([self.waitingScreen])
	
	def waitingScreen(self):
		global wSexec
		if waitingScreen:
			self.canva.unbind_all("<Button-1>")
			self.canva.unbind('<Motion>')
			self.canva.unbind("<Enter>")
			#while True:
			#self.canva.pack_forget()
			self.canva.delete("all")
			if self.animIndex==0:
				self.text=self.canva.create_text(self.wd/2,self.hg/10,text="Waiting for opponent.",font=('Arial',15,"bold"))
			elif self.animIndex==1:
				self.text=self.canva.create_text(self.wd/2,self.hg/10,text="Waiting for opponent..",font=('Arial',15,"bold"))
			elif self.animIndex==2:
				self.text=self.canva.create_text(self.wd/2,self.hg/10,text="Waiting for opponent...",font=('Arial',15,"bold"))
			elif self.animIndex==3:
				self.text=self.canva.create_text(self.wd/2,self.hg/10,text="Waiting for opponent....",font=('Arial',15,"bold"))
			self.animIndex=(self.animIndex+1)%4
			self.canva.pack()
			self.after(1500,self.waitingScreenQue)
			
			wSexec=True
		
	def playingScreenQue(self):
		self.que.put([self.playingScreen])
		
	def playingScreen(self):
		global pSexec
		self.canva.bind_all("<Button-1>",self.mouse_click)
		self.canva.bind('<Motion>',self.get_mouse)
		self.canva.bind("<Enter>",self.get_mouse)
		#self.canva.pack_forget()
		self.canva.delete(self.text)
		self.look_for_expand()
		self.update_map()
		self.canva.pack()
		self.o_turnQue()
		#print("playing screen")
		pSexec=True
	
	def opponentScreenQue(self):
		self.que.put([self.opponentScreen])
	
	def opponentScreen(self):
		global oSexec
		self.canva.unbind_all("<Button-1>")
		self.canva.bind('<Motion>',self.get_mouse)
		self.canva.bind("<Enter>",self.get_mouse)
		#self.canva.pack_forget()
		self.canva.delete(self.text)
		self.text=self.canva.create_text(self.wd/2,self.hg/10,text="Opponent's turn.",font=('Arial',15,"bold"))
		self.update_map()
		self.canva.pack()
		oSexec=True
		
	"""def waitOpScreen(self):
		global wOSexec
		self.canva.unbind_all("<Button-1>")
		self.canva.unbind('<Motion>')
		self.canva.unbind("<Enter>")
		self.canva.pack_forget()
		self.canva.delete("all")
		self.text=self.canva.create_text(500,100,text="Your opponent is not ready.")
		self.update_map()
		self.canva.pack()
		wOSexec=True"""
	
	def update_mapQue(self):
		self.que.put([self.update_map])
		
	def update_map(self):
		for i in range(self.wd//40+1):
			self.canva.create_line(self.i-40,40*(i-1)+self.j,self.wd,40*(i-1)+self.j)
			self.canva.create_line((i-1)*40+self.i,self.j-40,(i-1)*40+self.i,self.hg)
		for i in range(self.wd//40+1):
			for j in range(self.wd//40+1):
				if self.win[i+self.y//40].get_sp(j+self.x//40)=="x":
					self.draw_xQue(j*40,i*40)
				if self.win[i+self.y//40].get_sp(j+self.x//40)=="o":
					self.draw_oQue(j*40,i*40)
		if opponentScreen:
			self.canva.delete(self.text)
			self.text=self.canva.create_text(self.wd/2,self.hg/10,text="Opponent's turn.",font=('Arial',15,"bold"))
			
	
	def update_map_rightQue(self):
		self.que.put([self.update_map_right])

	def update_map_right(self):
		self.i+=self.speed
		self.x-=self.speed
		self.i%=40
		self.canva.pack_forget()
		self.canva.delete("all")
		self.update_mapQue()
		self.canva.pack()
	
	def update_map_leftQue(self):
		self.que.put([self.update_map_left])
		
	def update_map_left(self):
		self.i-=self.speed
		self.x+=self.speed
		self.i%=40
		self.canva.pack_forget()
		self.canva.delete("all")
		self.update_mapQue()
		self.canva.pack()
		
	def update_map_upQue(self):
		self.que.put([self.update_map_up])
		
	def update_map_up(self):
		self.j-=self.speed
		self.y+=self.speed
		self.j%=40
		self.canva.pack_forget()
		self.canva.delete("all")
		self.update_mapQue()
		self.canva.pack()
		
	def update_map_downQue(self):
		self.que.put([self.update_map_down])
		
	def update_map_down(self):
		self.j+=self.speed
		self.y-=self.speed
		self.j%=40
		self.canva.pack_forget()
		self.canva.delete("all")
		self.update_mapQue()
		self.canva.pack()
		
	def get_mouseQue(self,event):
		self.que.put([self.get_mouse,event])
	
	def get_mouse(self,event):
		time.sleep(1/(FPS*10))
		if(event.x>self.wd-self.scrollWidth and self.x<self.boundX):
			self.update_map_leftQue()
			#print(self.x)
		if(event.x<self.scrollWidth and self.x>0):
			self.update_map_rightQue()
		if(event.y<self.scrollWidth and self.y>0):
			self.update_map_downQue()
		if(event.y>self.hg-self.scrollWidth and self.y<self.boundY):
			self.update_map_upQue()

	def draw_xQue(self,x,y):
		self.que.put([self.draw_x,x,y])
		
	def draw_x(self,x,y):
		self.canva.create_line(x-self.x%40,y-self.y%40,x-self.x%40+40,y-self.y%40+40)
		self.canva.create_line(x-self.x%40+40,y-self.y%40,x-self.x%40,y-self.y%40+40)
		
	def draw_oQue(self,x,y):
		self.que.put([self.draw_o,x,y])
		
	def draw_o(self,x,y):
		self.canva.create_oval(x-self.x%40+1,y-self.y%40+1,x-self.x%40+39,y-self.y%40+39)
		
	def mouse_clickQue(self,event):
		self.que.put([self.mouse_click,event])
		
	def mouse_click(self,event):
		global playingScreen
		global opponentScreen
		if not self.oturn:
			if self.win[(event.y+self.y)//40].sp[(event.x+self.x)//40]!=" ":
				return
			self.win[(event.y+self.y)//40].set_sp((event.x+self.x)//40,self.yturn)
			self.move=[(event.y+self.y)//40,(event.x+self.x)//40]
			for i in range(self.n):
				if self.win[0].get_sp(i)!=" ":
					self.expandQue()
					break
				if self.win[self.n-2].get_sp(i)!=" ":
					self.expandQue()
					break
				if self.win[i].get_sp(0)!=" ":
					self.expandQue()
					break
				if self.win[i].get_sp(self.n-2)!=" ":
					self.expandQue()
					break
			self.update_map()
			self.canva.pack()
			self.oturn=True
			self.o_turnQue()
			playingScreen=False
			opponentScreen=True
			oSexec=False
	
	def mouseClickQue(self,event):
		self.que.put([self.mouseClick,event])
	
	def mouseClick(self,event):
		if not self.oturn:
			if self.win[(event.y+self.y)//40].sp[(event.x+self.x)//40]!=" ":
				return
			self.win[(event.y+self.y)//40].set_sp((event.x+self.x)//40,"x")
			self.move=[(event.y+self.y)//40,(event.x+self.x)//40]
			self.omov[0]=(event.y+self.y)//40
			self.omov[1]=(event.x+self.x)//40
			for i in range(self.n):
				if self.win[0].get_sp(i)!=" ":
					self.expandQue()
					break
				if self.win[self.n-2].get_sp(i)!=" ":
					self.expandQue()
					break
				if self.win[i].get_sp(0)!=" ":
					self.expandQue()
					break
				if self.win[i].get_sp(self.n-2)!=" ":
					self.expandQue()
					break
			self.update_map()
			self.canva.pack()
			self.oturn=True
			self.oTurnQue()
			
		
	def expandQue(self):
		self.que.put([self.expand])
		
	def expand(self):
		self.n+=2
		ret=[[] for i in range(self.n)]
		for i in range(self.n):
			ret[i]=Win(self.n)
		for i in range(1,self.n-1):
			for j in range(1,self.n-1):
				if self.win[i-1].get_sp(j-1)==self.yturn:
					ret[i].set_sp(j,self.yturn)
				elif self.win[i-1].get_sp(j-1)==self.opturn:
					ret[i].set_contr(j,self.opturn)
		self.win=ret
		self.x+=40
		self.y+=40
		self.boundX+=80
		self.boundY+=80
		
	def look_for_expandQue(self):
		self.que.put([self.look_for_expand])
	
	def look_for_expand(self):
		for i in range(self.n):
			if self.win[0].get_sp(i)!=" ":
				self.expand()
				break
			if self.win[self.n-2].get_sp(i)!=" ":
				self.expand()
				break
			if self.win[i].get_sp(0)!=" ":
				self.expand()
				break
			if self.win[i].get_sp(self.n-2)!=" ":
				self.expand()
				break
		self.update_map()
		
	def o_turnQue(self):
		self.que.put([self.o_turn])
		
	def o_turn(self):
		n=self.n
		win=self.win
		gameLost=self.gameLost
	
		gameWin=self.gameWin
		
		for i in range(n):
			if gameWin==True:
				break
			for j in range(n):
				if i<n-4 and win[i].get_sp(j)==self.yturn and win[i+1].get_sp(j)==self.yturn and win[i+2].get_sp(j)==self.yturn and win[i+3].get_sp(j)==self.yturn and win[i+4].get_sp(j)==self.yturn:
					gameWin=True
					break
				if j<n-4 and win[i].get_sp(j)==self.yturn and win[i].get_sp(j+1)==self.yturn and win[i].get_sp(j+2)==self.yturn and win[i].get_sp(j+3)==self.yturn and win[i].get_sp(j+4)==self.yturn:
					gameWin=True
					break
				if j<n-4 and i<n-4 and win[i].get_sp(j)==self.yturn and win[i+1].get_sp(j+1)==self.yturn and win[i+2].get_sp(j+2)==self.yturn and win[i+3].get_sp(j+3)==self.yturn and win[i+4].get_sp(j+4)==self.yturn:
					gameWin=True
					break
				if j>=4 and i<n-4 and win[i].get_sp(j)==self.yturn and win[i+1].get_sp(j-1)==self.yturn and win[i+2].get_sp(j-2)==self.yturn and win[i+3].get_sp(j-3)==self.yturn and win[i+4].get_sp(j-4)==self.yturn:
					gameWin=True
					break

		for i in range(n):
			if gameLost==True:
				break
			for j in range(n):
				if i<n-4 and win[i].get_sp(j)==self.opturn and win[i+1].get_sp(j)==self.opturn and win[i+2].get_sp(j)==self.opturn and win[i+3].get_sp(j)==self.opturn and win[i+4].get_sp(j)==self.opturn:
					gameLost=True
					break
				if j<n-4 and win[i].get_sp(j)==self.opturn and win[i].get_sp(j+1)==self.opturn and win[i].get_sp(j+2)==self.opturn and win[i].get_sp(j+3)==self.opturn and win[i].get_sp(j+4)==self.opturn:
					gameLost=True
					break
				if j<n-4 and i<n-4 and win[i].get_sp(j)==self.opturn and win[i+1].get_sp(j+1)==self.opturn and win[i+2].get_sp(j+2)==self.opturn and win[i+3].get_sp(j+3)==self.opturn and win[i+4].get_sp(j+4)==self.opturn:
					gameLost=True
					break
				if j>=4 and i<n-4 and win[i].get_sp(j)==self.opturn and win[i+1].get_sp(j-1)==self.opturn and win[i+2].get_sp(j-2)==self.opturn and win[i+3].get_sp(j-3)==self.opturn and win[i+4].get_sp(j-4)==self.opturn:
					gameLost=True
					break
		self.gameWin=gameWin
		self.win=win
		self.gameLost=gameLost
		
		self.winMessageQue()
		
		
	def winMessageQue(self):
		self.que.put([self.winMessage])
	
	def winMessage(self):
		global gameDown
		global waitingScreen
		global playingScreen
		global opponentScreen
		global wSexec
		
		if self.gameWin or self.gameLost:
			self.isReady=False
			
			if self.gameWin:
				str=messagebox.askyesno("You won!","Press Yes if you want to restart game and no if you want to quit")
			elif self.gameLost:
				str=messagebox.askyesno("You Lost!","Press Yes if you want to restart game and no if you want to quit")
			if str:
				self.clearQue()
				self.ex=True
				waitingScreen=True
				playingScreen=False
				opponentScreen=False
				wSexec=False
				self.isReady=True
				#print("clear")
				
			else:
				gameDown=True
				waitingScreen=False
				playingScreen=False
				opponentScreen=False
				self.ex=True
				self.isReady=True
				#while controler.isAlive() or respond.isAlive():
					#time.sleep(1/FPS)
				self.clear()
				self.canva.unbind_all("<Button-1>")
				self.canva.unbind('<Motion>')
				self.canva.unbind("<Enter>")
				#print("clear")
				self.menuScreenQue()
				
	def clearQue(self):
		self.que.put([self.clear])
				
	def clear(self):
		global txt
		txt=""
		#self.canva.pack_forget()
		self.canva.delete("all")
		self.n=33
		self.win=[[] for i in range(self.n)]
		for i in range(self.n):
			self.win[i]=Win(self.n)
		self.gameWin=False
		self.gameLost=False
		self.oturn=False
		self.i=0
		self.j=0
		self.x=0
		self.y=0
		#self.canva.pack()
		self.yturn="x"
		self.opturn="o"
		#print("Cleared")
	
	def oTurnQue(self):
		self.que.put([self.oTurn])
		
	def oTurn(self):
		win=self.win
		gameWin=self.gameWin
		gameLost=self.gameLost
		oturn=self.oturn
		n=self.n
		pressure=False
		#checking if win
		for i in range(n):
			if gameWin==True:
				break
			for j in range(n):
				if i<n-4 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j)=="x" and win[i+2].get_sp(j)=="x" and win[i+3].get_sp(j)=="x" and win[i+4].get_sp(j)=="x":
					gameWin=True
					break
				if j<n-4 and win[i].get_sp(j)=="x" and win[i].get_sp(j+1)=="x" and win[i].get_sp(j+2)=="x" and win[i].get_sp(j+3)=="x" and win[i].get_sp(j+4)=="x":
					gameWin=True
					break
				if j<n-4 and i<n-4 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j+1)=="x" and win[i+2].get_sp(j+2)=="x" and win[i+3].get_sp(j+3)=="x" and win[i+4].get_sp(j+4)=="x":
					gameWin=True
					break
				if j>=4 and i<n-4 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j-1)=="x" and win[i+2].get_sp(j-2)=="x" and win[i+3].get_sp(j-3)=="x" and win[i+4].get_sp(j-4)=="x":
					gameWin=True
					break
		
		#checking bounds
		o=False
		for i in range(n):
			if o:
				break
			for j in range(n):
				if self.win[j].sp[i]!=" ":
					self.lbound=i
					o=True
					break
		o=False
		for i in range(n-1,-1,-1):
			if o:
				break
			for j in range(n):
				if self.win[j].sp[i]!=" ":
					self.rbound=i
					o=True
					break
		o=False
		for i in range(n):
			if o:
				break
			for j in range(n):
				if self.win[i].sp[j]!=" ":
					self.ubound=i
					o=True
					break
		o=False
		for i in range(n-1,-1,-1):
			if o:
				break
			for j in range(n):
				if self.win[i].sp[j]!=" ":
					self.dbound=i
					o=True
					break
		temp=[]
		for i in range(self.ubound,self.dbound+1):
			temp.append([])
			for j in range(self.lbound,self.rbound+1):
				temp[i-self.ubound].append(self.win[i].sp[j])
		
		#checking 4 o in a row aggresive attack
		for i in range(n):
			if oturn==False:
				break
			for j in range(n):
				if i<n-3 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j)=="o" and  win[i+2].get_sp(j)=="o" and win[i+3].get_sp(j)=="o" and i+4<n  and win[i+4].get_sp(j)!="o"and win[i+4].get_sp(j)!="x" :
					win[i+4].set_contr(j)
					self.mov[0]=i+4
					self.mov[1]=j
					oturn=False
					break
				elif i<n-3 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j)=="o" and  win[i+2].get_sp(j)=="o" and win[i+3].get_sp(j)=="o" and i-1>=0 and win[i-1].get_sp(j)!="o"and win[i-1].get_sp(j)!="x":
					win[i-1].set_contr(j)
					self.mov[0]=i-1
					self.mov[1]=j
					oturn=False
					break
				if j<n-3 and win[i].get_sp(j)=="o" and win[i].get_sp(j+1)=="o" and win[i].get_sp(j+2)=="o" and win[i].get_sp(j+3)=="o" and j+4<n  and win[i].get_sp(j+4)!="o"and win[i].get_sp(j+4)!="x":
					win[i].set_contr(j+4)
					self.mov[0]=i
					self.mov[1]=j+4
					oturn=False
					break
				elif j<n-3 and win[i].get_sp(j)=="o" and win[i].get_sp(j+1)=="o" and win[i].get_sp(j+2)=="o" and win[i].get_sp(j+3)=="o" and j-1>=0 and win[i].get_sp(j-1)!="o"and win[i].get_sp(j-1)!="x":
					win[i].set_contr(j-1)
					self.mov[0]=i
					self.mov[1]=j-1
					oturn=False
					break
				if j<n-3 and i<n-3 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j+1)=="o" and win[i+2].get_sp(j+2)=="o" and win[i+3].get_sp(j+3)=="o" and i+4<n and j+4<n  and win[i+4].get_sp(j+4)!="o"and win[i+4].get_sp(j+4)!="x":
					win[i+4].set_contr(j+4)
					self.mov[0]=i+4
					self.mov[1]=j+4
					oturn=False
					break
				elif j<n-3 and i<n-3 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j+1)=="o" and win[i+2].get_sp(j+2)=="o" and win[i+3].get_sp(j+3)=="o" and i-1>=0 and j-1>=0 and win[i-1].get_sp(j-1)!="o"and win[i-1].get_sp(j-1)!="x":
					win[i-1].set_contr(j-1)
					self.mov[0]=i-1
					self.mov[1]=j-1
					oturn=False
					break
				if j>=3 and i<n-3 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j-1)=="o" and win[i+2].get_sp(j-2)=="o" and win[i+3].get_sp(j-3)=="o" and i+4<n and j-4>=0 and win[i+4].get_sp(j-4)!="o"and win[i+4].get_sp(j-4)!="x":
					win[i+4].set_contr(j-4)
					self.mov[0]=i+4
					self.mov[1]=j-4
					oturn=False
					break
				elif j>=3 and i<n-3 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j-1)=="o" and win[i+2].get_sp(j-2)=="o" and win[i+3].get_sp(j-3)=="o"  and i-1>=0 and j+1<n and win[i-1].get_sp(j+1)!="o"and win[i-1].get_sp(j+1)!="x":
					win[i-1].set_contr(j+1)
					self.mov[0]=i-1
					self.mov[1]=j+1
					oturn=False
					break
		#checking 4 x in a row defense
		for i in range(n):
			if oturn==False:
				break
			for j in range(n):
				if i<n-3 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j)=="x" and  win[i+2].get_sp(j)=="x" and win[i+3].get_sp(j)=="x" and i+4<n  and win[i+4].get_sp(j)!="o"and win[i+4].get_sp(j)!="x" :
					win[i+4].set_contr(j)
					self.mov[0]=i+4
					self.mov[1]=j
					oturn=False
					pressure=True
					break
				elif i<n-3 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j)=="x" and  win[i+2].get_sp(j)=="x" and win[i+3].get_sp(j)=="x" and i-1>=0 and win[i-1].get_sp(j)!="o"and win[i-1].get_sp(j)!="x":
					win[i-1].set_contr(j)
					self.mov[0]=i-1
					self.mov[1]=j
					oturn=False
					pressure=True
					break
				if j<n-3 and win[i].get_sp(j)=="x" and win[i].get_sp(j+1)=="x" and win[i].get_sp(j+2)=="x" and win[i].get_sp(j+3)=="x" and j+4<n  and win[i].get_sp(j+4)!="o"and win[i].get_sp(j+4)!="x":
					win[i].set_contr(j+4)
					self.mov[0]=i
					self.mov[1]=j+4
					oturn=False
					pressure=True
					break
				elif j<n-3 and win[i].get_sp(j)=="x" and win[i].get_sp(j+1)=="x" and win[i].get_sp(j+2)=="x" and win[i].get_sp(j+3)=="x" and j-1>=0 and win[i].get_sp(j-1)!="o"and win[i].get_sp(j-1)!="x":
					win[i].set_contr(j-1)
					self.mov[0]=i
					self.mov[1]=j-1
					oturn=False
					pressure=True
					break
				if j<n-3 and i<n-3 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j+1)=="x" and win[i+2].get_sp(j+2)=="x" and win[i+3].get_sp(j+3)=="x" and i+4<n and j+4<n  and win[i+4].get_sp(j+4)!="o"and win[i+4].get_sp(j+4)!="x":
					win[i+4].set_contr(j+4)
					self.mov[0]=i+4
					self.mov[1]=j+4
					oturn=False
					pressure=True
					break
				elif j<n-3 and i<n-3 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j+1)=="x" and win[i+2].get_sp(j+2)=="x" and win[i+3].get_sp(j+3)=="x" and i-1>=0 and j-1>=0 and win[i-1].get_sp(j-1)!="o"and win[i-1].get_sp(j-1)!="x":
					win[i-1].set_contr(j-1)
					self.mov[0]=i-1
					self.mov[1]=j-1
					oturn=False
					pressure=True
					break
					
				if j>=3 and i<n-3 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j-1)=="x" and win[i+2].get_sp(j-2)=="x" and win[i+3].get_sp(j-3)=="x" and i+4<n and j-4>=0 and win[i+4].get_sp(j-4)!="o"and win[i+4].get_sp(j-4)!="x":
					win[i+4].set_contr(j-4)
					self.mov[0]=i+4
					self.mov[1]=j-4
					oturn=False
					pressure=True
					break
				elif j>=3 and i<n-3 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j-1)=="x" and win[i+2].get_sp(j-2)=="x" and win[i+3].get_sp(j-3)=="x"  and i-1>=0 and j+1<n and win[i-1].get_sp(j+1)!="o"and win[i-1].get_sp(j+1)!="x":
					win[i-1].set_contr(j+1)
					self.mov[0]=i-1
					self.mov[1]=j+1
					oturn=False
					pressure=True
					break
					
		#agressive defense
		o=False
		b=False
		indexi=0
		indexj=0
		for matrix in self.mem:
			if oturn==False:
				break
			#checking bounds in matrix
			o=False
			stari=0
			starj=0
			for i in range(len(matrix)):
				for j in range(len(matrix[i])):
					if matrix[i][j]=="*":
						stari=i
						starj=j
			lbound=0
			rbound=0
			dbound=0
			ubound=0
			for i in range(len(matrix[0])):
				if o:
					break
				for j in range(len(matrix)):
					if matrix[j][i]!=" " and matrix[j][i]!="+" and matrix[j][i]!="*":
						lbound=i
						o=True
						break
			o=False
			for i in range(len(matrix[0])-1,-1,-1):
				if o:
					break
				for j in range(len(matrix)):
					if matrix[j][i]!=" " and matrix[j][i]!="+" and matrix[j][i]!="*":
						rbound=i
						o=True
						break
			o=False
			for i in range(len(matrix)):
				if o:
					break
				for j in range(len(matrix[0])):
					if matrix[i][j]!=" " and matrix[i][j]!="+" and matrix[i][j]!="*":
						ubound=i
						o=True
						break
			o=False
			for i in range(len(matrix)-1,-1,-1):
				if o:
					break
				for j in range(len(matrix[0])):
					if matrix[i][j]!=" " and matrix[i][j]!="+" and matrix[i][j]!="*":
						dbound=i
						o=True
						break
			if dbound-ubound>len(temp) or rbound-lbound>len(temp[0]):
				continue
				
			for istart in range(len(temp)):
				if b:
					break
				mini=0
				maxi=0
				if istart>=ubound:
					mini=ubound
				else:
					mini=istart
				if len(temp)-1-istart-(dbound-ubound)>=len(matrix)-1-dbound:
					maxi=len(matrix)-1-dbound
				else:
					maxi=len(temp)-1-istart-(dbound-ubound)
				if maxi<0:
					break
				for jstart in range(len(temp[0])):
					o=False
					minj=0
					maxj=0
					if jstart>=lbound:
						minj=lbound
					else:
						minj=jstart
					if len(temp[0])-1-jstart-(rbound-lbound)>=len(matrix[0])-1-rbound:
						maxj=len(matrix[0])-1-rbound
					else:
						maxj=len(temp[0])-1-jstart-(rbound-lbound)
					if maxj<0:
						break
					
					
					for i in range(ubound-mini,dbound+maxi+1):
						if o:
							break
						for j in range(lbound-minj,rbound+maxj+1):
							#if self.ubound+istart+i-2>=0 and self.ubound+istart+i-2<n and self.lbound+jstart+j-2>=0 and self.lbound+jstart+j-2<n:
							if matrix[i][j]=="x" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]!="x" or matrix[i][j]=="*" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]!=" " or matrix[i][j]=="+" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]=="o":
								#print(win[self.ubound+istart+i-1].sp[self.lbound+jstart+j-1],matrix[i][j],self.ubound+istart+i-1,self.lbound+jstart+j-1,i,j)
								o=True
								break
							"""if matrix[i][j]=="*" :
								indexi=self.ubound+istart+i-ubound+mini
								indexj=self.lbound+jstart+j-lbound+minj
								print(indexi,indexj)
							else:
								if matrix[i][j]=="x" or matrix[i][j]=="*":
									o=True
									break
							"""
						
					#print(o)
					if o==False:
						b=True
						indexi=self.ubound+istart+stari-ubound
						indexj=self.lbound+jstart+starj-lbound
						win[indexi].set_contr(indexj)
						self.mov[0]=indexi
						self.mov[1]=indexj
						#print(indexi,indexj)
						oturn=False
						pressure=True
						break
						
		#agressive respond
		o=False
		b=False
		indexi=0
		indexj=0
		for matrix in self.mem:
			if oturn==False:
				break
			#checking bounds in matrix
			for i in range(len(matrix)):
				for j in range(len(matrix[i])):
					if matrix[i][j]=="*":
						stari=i
						starj=j
			o=False
			lbound=0
			rbound=0
			dbound=0
			ubound=0
			for i in range(len(matrix[0])):
				if o:
					break
				for j in range(len(matrix)):
					if matrix[j][i]!=" " and matrix[j][i]!="+" and matrix[j][i]!="*":
						lbound=i
						o=True
						break
			o=False
			for i in range(len(matrix[0])-1,-1,-1):
				if o:
					break
				for j in range(len(matrix)):
					if matrix[j][i]!=" " and matrix[j][i]!="+" and matrix[j][i]!="*":
						rbound=i
						o=True
						break
			o=False
			for i in range(len(matrix)):
				if o:
					break
				for j in range(len(matrix[0])):
					if matrix[i][j]!=" " and matrix[i][j]!="+" and matrix[i][j]!="*":
						ubound=i
						o=True
						break
			o=False
			for i in range(len(matrix)-1,-1,-1):
				if o:
					break
				for j in range(len(matrix[0])):
					if matrix[i][j]!=" " and matrix[i][j]!="+" and matrix[i][j]!="*":
						dbound=i
						o=True
						break
			if dbound-ubound>len(temp) or rbound-lbound>len(temp[0]):
				continue
				
			for istart in range(len(temp)):
				if b:
					break
				mini=0
				maxi=0
				if istart>=ubound:
					mini=ubound
				else:
					mini=istart
				if len(temp)-1-istart-(dbound-ubound)>=len(matrix)-1-dbound:
					maxi=len(matrix)-1-dbound
				else:
					maxi=len(temp)-1-istart-(dbound-ubound)
				if maxi<0:
					break
				for jstart in range(len(temp[0])):
					o=False
					minj=0
					maxj=0
					if jstart>=lbound:
						minj=lbound
					else:
						minj=jstart
					if len(temp[0])-1-jstart-(rbound-lbound)>=len(matrix[0])-1-rbound:
						maxj=len(matrix[0])-1-rbound
					else:
						maxj=len(temp[0])-1-jstart-(rbound-lbound)
					if maxj<0:
						break
					
					
					for i in range(ubound-mini,dbound+maxi+1):
						if o:
							break
						for j in range(lbound-minj,rbound+maxj+1):
							#if self.ubound+istart+i-2>=0 and self.ubound+istart+i-2<n and self.lbound+jstart+j-2>=0 and self.lbound+jstart+j-2<n:
							if matrix[i][j]=="x" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]!="o" or matrix[i][j]=="*" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]!=" " or matrix[i][j]=="+" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]=="x":
								#print(win[self.ubound+istart+i-1].sp[self.lbound+jstart+j-1],matrix[i][j],self.ubound+istart+i-1,self.lbound+jstart+j-1,i,j)
								o=True
								break
							"""if matrix[i][j]=="*" :
								indexi=self.ubound+istart+i-ubound+mini
								indexj=self.lbound+jstart+j-lbound+minj
							else:
								if matrix[i][j]=="x" or matrix[i][j]=="*":
									o=True
									break
							"""
						
					#print(o)
					if o==False:
						b=True
						indexi=self.ubound+istart+stari-ubound
						indexj=self.lbound+jstart+starj-lbound
						win[indexi].set_contr(indexj)
						self.mov[0]=indexi
						self.mov[1]=indexj
						#print(indexi,indexj)
						oturn=False
						break
		
        #	checking 1 x
		if oturn:
			ocords=[]
			for i in range(n):
				for j in range(n):
					if win[i].get_sp(j)=="o" and (win[i+1].get_sp(j)==" " or win[i-1].get_sp(j)==" " or win[i].get_sp(j+1)==" " or win[i].get_sp(j-1)==" " or win[i-1].get_sp(j+1)==" " or win[i-1].get_sp(j-1)==" " or win[i+1].get_sp(j+1)==" " or win[i+1].get_sp(j-1)==" "):
						ocords.append([i,j])
			if len(ocords)!=0:
				ocord=ocords[random.randrange(len(ocords))]
				xcords=[]
				if win[ocord[0]+1].get_sp(ocord[1])==" ":
					xcords.append([ocord[0]+1,ocord[1]])
				if win[ocord[0]-1].get_sp(ocord[1])==" ":
					xcords.append([ocord[0]-1,ocord[1]])
				if win[ocord[0]].get_sp(ocord[1]+1)==" ":
					xcords.append([ocord[0],ocord[1]+1])
				if win[ocord[0]].get_sp(ocord[1]-1)==" ":
					xcords.append([ocord[0],ocord[1]-1])
				if win[ocord[0]+1].get_sp(ocord[1]+1)==" ":
					xcords.append([ocord[0]+1,ocord[1]+1])
				if win[ocord[0]+1].get_sp(ocord[1]-1)==" ":
					xcords.append([ocord[0]+1,ocord[1]-1])
				if win[ocord[0]-1].get_sp(ocord[1]+1)==" ":
					xcords.append([ocord[0]-1,ocord[1]+1])
				if win[ocord[0]-1].get_sp(ocord[1]-1)==" ":
					xcords.append([ocord[0]-1,ocord[1]-1])
				xcord=xcords[random.randrange(len(xcords))]
				#print(xcord,"XCOORD")
				win[xcord[0]].set_contr(xcord[1])
				self.mov[0]=xcord[0]
				self.mov[1]=xcord[1]
				oturn=False
			else:
				for i in range(n):
					if oturn==False:
						break
					for j in range(n):
						if win[i].get_sp(j)=="x" and j+1<n and win[i].get_sp(j+1)!="o" and win[i].get_sp(j+1)!="x":
							win[i].set_contr(j+1)
							self.mov[0]=i
							self.mov[1]=j+1
							oturn=False
							break
						elif win[i].get_sp(j)=="x" and win[i].get_sp(j-1)!="o" and win[i].get_sp(j-1)!="x":
							win[i].set_contr(j-1)
							self.mov[0]=i
							self.mov[1]=j-1
							oturn=False
							break
					
		
		

	#checking if lost

		for i in range(n):
			if gameLost==True:
				break
			for j in range(n):
				if i<n-4 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j)=="o" and win[i+2].get_sp(j)=="o" and win[i+3].get_sp(j)=="o" and win[i+4].get_sp(j)=="o":
					gameLost=True
					break
				if j<n-4 and win[i].get_sp(j)=="o" and win[i].get_sp(j+1)=="o" and win[i].get_sp(j+2)=="o" and win[i].get_sp(j+3)=="o" and win[i].get_sp(j+4)=="o":
					gameLost=True
					break
				if j<n-4 and i<n-4 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j+1)=="o" and win[i+2].get_sp(j+2)=="o" and win[i+3].get_sp(j+3)=="o" and win[i+4].get_sp(j+4)=="o":
					gameLost=True
					break
				if j>=4 and i<n-4 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j-1)=="o" and win[i+2].get_sp(j-2)=="o" and win[i+3].get_sp(j-3)=="o" and win[i+4].get_sp(j-4)=="o":
					gameLost=True
					break
		
		self.win=win
		self.gameWin=gameWin
		self.gameLost=gameLost
		self.oturn=oturn
		expand=False
		for i in range(self.n):
			if self.win[0].get_sp(i)!=" ":
				self.expand()
				expand=True
				break
			if self.win[self.n-2].get_sp(i)!=" ":
				self.expand()
				expand=True
				break
			if self.win[i].get_sp(0)!=" ":
				self.expand()
				expand=True
				break
			if self.win[i].get_sp(self.n-2)!=" ":
				self.expand()
				expand=True
				break
		self.update_map()
		
		#checking bounds
		o=False
		for i in range(n):
			if o:
				break
			for j in range(n):
				if self.win[j].sp[i]!=" ":
					self.lbound=i
					o=True
					break
		o=False
		for i in range(n-1,-1,-1):
			if o:
				break
			for j in range(n):
				if self.win[j].sp[i]!=" ":
					self.rbound=i
					o=True
					break
		o=False
		for i in range(n):
			if o:
				break
			for j in range(n):
				if self.win[i].sp[j]!=" ":
					self.ubound=i
					o=True
					break
		o=False
		for i in range(n-1,-1,-1):
			if o:
				break
			for j in range(n):
				if self.win[i].sp[j]!=" ":
					self.dbound=i
					o=True
					break
		if self.gameWin:
			pressure=True
		temp=[]
		for i in range(self.ubound-1,self.dbound+2):
			temp.append([])
			for j in range(self.lbound-1,self.rbound+2):
				temp[i-self.ubound+1].append(self.win[i].sp[j])
				
		expands=0
		if expand:
			expands=1
		if self.boundwidth>self.lbound-expands:
			self.omov[1]+=1
		if self.boundheight>self.ubound-expands:
			self.omov[0]+=1
			
		self.boundheight=self.ubound
		self.boundwidth=self.lbound
		
		self.mov[0]-=self.ubound-1
		self.mov[1]-=self.lbound-1
		self.omov[0]-=self.ubound-1
		self.omov[1]-=self.lbound-1
		if expand:
			self.mov[0]+=1
			self.mov[1]+=1
			self.omov[0]+=1
			self.omov[1]+=1
		self.movm.append([temp,[self.mov[0],self.mov[1]],[self.omov[0],self.omov[1]],pressure])
		#print(self.movm)
		
		
		if self.gameWin==True or self.gameLost==True:
			if self.gameWin==True:
				index=0
				
				for i in range(len(self.movm)-1,0,-1):
					if not self.movm[i][3]:
						index=i
						break
				#print(self.movm[index+1])
				temp=[]
				for i in range(len(self.movm[index+1][0])):
					temp.append([])
					for j in range(len(self.movm[index+1][0][0])):
						if self.movm[index+1][0][i][j]!="o"  and (i==self.movm[index+1][2][0]+1 and j==self.movm[index+1][2][1]+1 or i==self.movm[index+1][2][0]+2 and j==self.movm[index+1][2][1]+2 or i==self.movm[index+1][2][0]+3 and j==self.movm[index+1][2][1]+3 or i==self.movm[index+1][2][0]+4 and j==self.movm[index+1][2][1]+4 or i==self.movm[index+1][2][0]+1 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+2 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+3 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+4 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+1 and j==self.movm[index+1][2][1]-1 or i==self.movm[index+1][2][0]+2 and j==self.movm[index+1][2][1]-2 or i==self.movm[index+1][2][0]+3 and j==self.movm[index+1][2][1]-3 or i==self.movm[index+1][2][0]+4 and j==self.movm[index+1][2][1]-4 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-1 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-2 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-3 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-4 or i==self.movm[index+1][2][0]-1 and j==self.movm[index+1][2][1]-1 or i==self.movm[index+1][2][0]-2 and j==self.movm[index+1][2][1]-2 or i==self.movm[index+1][2][0]-3 and j==self.movm[index+1][2][1]-3 or i==self.movm[index+1][2][0]-4 and j==self.movm[index+1][2][1]-4 or i==self.movm[index+1][2][0]-1 and j==self.movm[index+1][2][1] or  i==self.movm[index+1][2][0]-2 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]-3 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]-4 and j==self.movm[index+1][2][1] or  i==self.movm[index+1][2][0]-1 and j==self.movm[index+1][2][1]+1 or  i==self.movm[index+1][2][0]-2 and j==self.movm[index+1][2][1]+2 or  i==self.movm[index+1][2][0]-3 and j==self.movm[index+1][2][1]+3 or i==self.movm[index+1][2][0]-4 and j==self.movm[index+1][2][1]+4 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+1 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+2 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+3 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+4 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]):
							if  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]:
								temp[i].append("*")
							elif self.movm[index+1][0][i][j]==" ":
								temp[i].append("+")
							else:
								temp[i].append(self.movm[index+1][0][i][j])
						else:
							if i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1] and (i==self.movm[index+1][2][0]+1 and j==self.movm[index+1][2][1]+1 or i==self.movm[index+1][2][0]+2 and j==self.movm[index+1][2][1]+2 or i==self.movm[index+1][2][0]+3 and j==self.movm[index+1][2][1]+3 or i==self.movm[index+1][2][0]+4 and j==self.movm[index+1][2][1]+4 or i==self.movm[index+1][2][0]+1 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+2 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+3 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+4 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+1 and j==self.movm[index+1][2][1]-1 or i==self.movm[index+1][2][0]+2 and j==self.movm[index+1][2][1]-2 or i==self.movm[index+1][2][0]+3 and j==self.movm[index+1][2][1]-3 or i==self.movm[index+1][2][0]+4 and j==self.movm[index+1][2][1]-4 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-1 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-2 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-3 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-4 or i==self.movm[index+1][2][0]-1 and j==self.movm[index+1][2][1]-1 or i==self.movm[index+1][2][0]-2 and j==self.movm[index+1][2][1]-2 or i==self.movm[index+1][2][0]-3 and j==self.movm[index+1][2][1]-3 or i==self.movm[index+1][2][0]-4 and j==self.movm[index+1][2][1]-4 or i==self.movm[index+1][2][0]-1 and j==self.movm[index+1][2][1] or  i==self.movm[index+1][2][0]-2 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]-3 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]-4 and j==self.movm[index+1][2][1] or  i==self.movm[index+1][2][0]-1 and j==self.movm[index+1][2][1]+1 or  i==self.movm[index+1][2][0]-2 and j==self.movm[index+1][2][1]+2 or  i==self.movm[index+1][2][0]-3 and j==self.movm[index+1][2][1]+3 or i==self.movm[index+1][2][0]-4 and j==self.movm[index+1][2][1]+4 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+1 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+2 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+3 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+4 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]):
								temp[i].append("+")
							else:
								temp[i].append(" ")
					#print("")
				lbound=0
				rbound=0
				ubound=0
				dbound=0
				#print(temp)
				o=False
				for i in range(len(temp[0])):
					if o:
						break
					for j in range(len(temp)):
						if temp[j][i]!=" ":
							lbound=i
							o=True
							break
				o=False
				for i in range(len(temp[0])-1,-1,-1):
					if o:
						break
					for j in range(len(temp)):
						if temp[j][i]!=" ":
							rbound=i
							o=True
							break
				o=False
				for i in range(len(temp)):
					if o:
						break
					for j in range(len(temp[0])):
						if temp[i][j]!=" ":
							ubound=i
							o=True
							break
				o=False
				for i in range(len(temp)-1,-1,-1):
					if o:
						break
					for j in range(len(temp[0])):
						if temp[i][j]!=" ":
							dbound=i
							o=True
							break
				#print(temp)
				#print(dbound,rbound,lbound,ubound)
				temp1=[]			
				for i in range(ubound,dbound+1):
					temp1.append([])
					for j in range(lbound,rbound+1):
						temp1[i-ubound].append(temp[i][j])
				
				
				f=open("mem.txt","wb")
				pickle.dump(self.mem+[temp1],f)
				f.close()
				memedit.clear()
			self.messageQue()
	
	def messageQue(self):
		self.que.put([self.message])
		
	def message(self):
		if self.gameWin:
			str=messagebox.askyesno("You won!","Yes if you want to restart game and no if you want to quit")
		else:
			str=messagebox.askyesno("You Lost!","Yes if you want to restart game and no if you want to quit")
		if str==True:
			self.clearQue()
			self.update_mapQue()
		else:
			self.clearQue()
			self.ex=True
			self.isReady=True
			self.canva.unbind_all("<Button-1>")
			self.canva.unbind('<Motion>')
			self.canva.unbind("<Enter>")
			self.menuScreenQue()
				
				
		


class Game(threading.Thread):
	def __init__(self):	
		threading.Thread.__init__(self)
	def run(self):
		global gameDown
		global app
		global messengerRunning
		app=Application()
		app.resizable(width=False,height=False)
		app.title("TicTacToe. Gamma")
		app.mainloop()
		if messengerRunning:
			messenger.terminate()
			messengerRunning=False
		gameDown=True
		
		
class Respond(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.data=[]
		self.newData=False
		self.prevData=None
	def run(self):
		global waitingScreen
		global opponentScreen
		global playingScreen
		#global waitOpScreen
		#global wOSexec
		global pSexec
		global oSexec
		global wSexec
		global gameDown  
		global MS
		global txt
		global connectScreen
		PORT = 50007              
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect((HOST, PORT))
		except ConnectionRefusedError:
			app.sdScreenQue()
			print("Refuse")
			#app.terminateThreads()
			gameDown=True
		except TimeoutError:
			app.sdScreenQue()
			print("Timeout")
			#app.terminateThreads()
			gameDown=True
		while True:
			global controlerStarted
			global mLeft
			time.sleep(1/FPS)
			if gameDown:
				print("Shutting down...")
				s.close()
				break
			try:
				self.data = pickle.loads(s.recv(1024))
			except ConnectionResetError:
				print("Connection to the server terminated.")
				app.terminateThreadsQue()
				break
			except EOFError:
				print("No response from server.")
				#app.terminateThreads()
				#break
			except ConnectionAbortedError:
				print("Connection to the server terminated.")
				app.terminateThreadsQue()
				break
			
			#print("starting ")
			if not controlerStarted:
				connectScreen=False
				start_controler()
				controlerStarted=True
			if self.data[3]!=self.prevData:
				self.newData=True
				#print(self.data)
			else:
				self.newData=False
			self.prevData=self.data[3]
			if self.data[0]!=None:
				s.sendall(pickle.dumps([1,MS,None,app.ex,app.isReady,True,messengerRunning]))
				app.win[self.data[0][0]].set_contr(self.data[0][1],app.opturn)
				
			#try:
			if app.move!=None:
				s.sendall(pickle.dumps([None,MS,app.move,app.ex,app.isReady,True,messengerRunning]))
				app.move=None
			#except NameError:
			s.sendall(pickle.dumps([None,MS,None,app.ex,app.isReady,True,messengerRunning]))
			app.ex=False
			
			if self.data[1]!=None:
				txt+=self.data[1]+"\n"
				messenger.update_chatQue()
			
			if self.data[2]==2:
				app.yturn="o"
				app.opturn="x"
				
		
			if self.data[3]!=0 :
				waitingScreen=False
				playingScreen=False
				opponentScreen=False
				#waitOpScreen=False
				if self.data[3]==1:
					playingScreen=True
					if self.newData:
						#print("update")
						pSexec=False
					app.oturn=False
				if self.data[3]==2:
					opponentScreen=True
					if self.newData:
						oSexec=False
			elif self.data[3]==0:
				waitingScreen=True
				playingScreen=False
				opponentScreen=False
				
			if self.data[4]:
				wSexec=False
			
			if self.data[5]:
				#print("p2 left")
				gameDown=True
				waitingScreen=False
				playingScreen=False
				opponentScreen=False
				txt+="Opponent has left the game. \n"
				messenger.update_chatQue()
				app.clearQue()
				s.sendall(pickle.dumps([None,MS,app.move,app.ex,app.isReady,False,messengerRunning]))
				app.menuScreenQue()
			
			if self.data[6] and not mLeft:
				txt+="Opponent has left the chat. \n"
				print("oh yeah")
				messenger.update_chatQue()
				mLeft=True
			MS=None
		print("Connection shutted down successfully.")
				
				

				

		
		
class Controler(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while True:
			global controlerStarted
			time.sleep(1/FPS)
			#if gameDown:
				#break
			if waitingScreen and not wSexec:
				app.waitingScreenQue()
			#if gameDown:
				#break
			if opponentScreen and not oSexec:
				app.opponentScreenQue()
			#if gameDown:
				#break
			if playingScreen and not pSexec:
				app.playingScreenQue()
			#if waitOpScreen and not wOSexec:
				#app.waitOpScreen()
			if gameDown:
				controlerStarted=False
				break
				
class Messenger(tkinter.Tk):
	def __init__(self):
		tkinter.Tk.__init__(self)
		
		self.canva2=tkinter.Canvas(self,width=400,height=30)
		self.canva=tkinter.Canvas(self,width=400,height=30)
		self.frm=tkinter.Frame(self,width=400,height=200)
		self.canva1=tkinter.Canvas(self.frm,width=400,height=200)
		self.send=tkinter.Button(self.canva2,text="Send",width=10,command=self.sendMsQue)
		self.entry=tkinter.Entry(self.canva,width=55)
		self.scroll=tkinter.Scrollbar(self.frm)
		self.sep=ttk.Separator(self,orient="horizontal")
		
		
		self.scroll.config(command=self.canva1.yview)
		self.canva1.config(yscrollcommand=self.scroll.set)
		self.canva1.config(scrollregion=(0,0,400,len(txt.splitlines())*19+5))
		#self.canva1.config(bg="red")
		self.canva1.yview("moveto",1)
		
		self.canva2.create_window(0,0,window=self.send)
		self.canva.create_window(0,0,window=self.entry)
		self.canva1.create_text(5,5,text=txt,anchor="nw",font=('Arial',15,"bold"))
		
		
		
		self.frm.pack()
		self.canva1.pack(side="left")
		self.entry.pack(fill="both",side="left")
		self.scroll.pack(fill="y",side="right")
		self.sep.pack(fill="x")
		self.canva.pack(side="left", fill="both")
		
		self.send.pack(fill="both")
		self.canva2.pack(side="right")
		
		self.bind("<KeyPress-Return>",self.sendMsQue)
		self.protocol("WM_DELETE_WINDOW", self.terminateQue)
		self.que=queue.Queue()
		self.updateQue()
		
	def updateQue(self):
		if self.que.qsize()>0:
			while True:
				get=self.que.get_nowait()
				func=get[0]
				args=get[1:]
				func(*args)
				if self.que.qsize()<=0:
					break
		#print("update")
		self.after(10,self.updateQue)
					
	def sendMsQue(self,event=None):
		if event==None:
			self.que.put([self.sendMs])
		else:
			self.que.put([self.sendMs,event])
	def sendMs(self,event=None):
		global MS
		global txt
		if(self.entry.get()!="" and self.entry.get()!=None):
			MS=self.entry.get()
			txt+=self.entry.get()+"\n"
			self.update_chatQue()
			
		
	def terminateQue(self):
		self.que.put([self.terminate])
		#print("terminating")
	def terminate(self):
		global messengerRunning
		messengerRunning=False
		
		self.quit()
		
	def update_chatQue(self):
		self.que.put([self.update_chat])
		
	def update_chat(self):
		self.canva1.delete("all")
		self.canva1.config(scrollregion=(0,0,400,len(txt.splitlines())*19+5))
		self.canva1.yview("moveto",1)
		self.canva1.create_text(5,5,text=txt,anchor="nw",font=('Arial',12,"bold"))
		try: 
			self.entry.delete(0,len(MS))
		except TypeError:
			pass
		#print("update")
		
class StartMessenger(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		
	def run(self):
		global messenger
		global messengerRunning
		messengerRunning=True
		messenger=Messenger()
		messenger.resizable(width=False,height=False)
		messenger.title("Messenger")
		messenger.mainloop()
		messengerRunning=False
				

	
				
			
def start_game():
	game=Game()
	game.start()
	startMessenger=StartMessenger()
	startMessenger.start()
def find_match():
	global respond
	respond=Respond()
	respond.start()

def start_controler():
	global controler
	controler=Controler()
	controler.start()
	

	#while True:
		#print(respond.isAlive(),controler.isAlive(),game.isAlive())
start_game()






	