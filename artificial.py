import pickle
import tkinter
from tkinter import messagebox
import random
import memedit

class Win():
	def __init__(self,n):
		self.sp=[" " for i in range(n)]
	def get_sp(self,coord):
		return self.sp[coord]
	def set_sp(self,coord):
		self.sp[coord]="x"
	def set_contr(self,coord):
		self.sp[coord]="o"

		
class Application(tkinter.Frame):
	def __init__(self,master=None):
		tkinter.Frame.__init__(self,master)
		self.n=33
		self.win=[[] for i in range(self.n)]
		for i in range(self.n):
			self.win[i]=Win(self.n)
		self.gameWin=False
		self.gameLost=False
		self.oturn=False
		self.f=open("mem.txt","rb")
		self.mem=pickle.load(self.f)
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
		self.i=0
		self.j=0
		self.x=120
		self.y=120
		self.scrollWidth=100
		self.speed=2
		self.boundX=280
		self.boundY=280
		self.pack()
		self.canva=tkinter.Canvas(width=1000, height=1000,bd=0)
		self.canva.bind_all("<Button-1>",self.mouse_click)
		self.canva.bind('<Motion>',self.get_mouse)
		self.canva.bind("<Enter>",self.get_mouse)
		self.update_map()
		self.canva.focus_force()
		self.canva.pack()
		
	def update_map(self):
		for i in range(26):
			self.canva.create_line(self.i-40,40*(i-1)+self.j,1000,40*(i-1)+self.j)
			self.canva.create_line((i-1)*40+self.i,self.j-40,(i-1)*40+self.i,1000)
		for i in range(26):
			for j in range(26):
				if self.win[i+self.y//40].get_sp(j+self.x//40)=="x":
					self.draw_x(j*40,i*40)
				if self.win[i+self.y//40].get_sp(j+self.x//40)=="o":
					self.draw_o(j*40,i*40)
		
	def update_map_right(self):
		self.i+=self.speed
		self.x-=self.speed
		self.i%=40
		self.canva.pack_forget()
		self.canva.delete("all")
		self.update_map()
		self.canva.pack()
	def update_map_left(self):
		self.i-=self.speed
		self.x+=self.speed
		self.i%=40
		self.canva.pack_forget()
		self.canva.delete("all")
		self.update_map()
		self.canva.pack()
		
	def update_map_up(self):
		self.j-=self.speed
		self.y+=self.speed
		self.j%=40
		self.canva.pack_forget()
		self.canva.delete("all")
		self.update_map()
		self.canva.pack()
	def update_map_down(self):
		self.j+=self.speed
		self.y-=self.speed
		self.j%=40
		self.canva.pack_forget()
		self.canva.delete("all")
		self.update_map()
		self.canva.pack()
	def get_mouse(self,event):
		if(event.x>1000-self.scrollWidth and self.x<self.boundX):
			self.update_map_left()
		if(event.x<self.scrollWidth and self.x>0):
			self.update_map_right()
		if(event.y<self.scrollWidth and self.y>0):
			self.update_map_down()
		if(event.y>1000-self.scrollWidth and self.y<self.boundY):
			self.update_map_up()

	
	def draw_x(self,x,y):
		self.canva.create_line(x-self.x%40,y-self.y%40,x-self.x%40+40,y-self.y%40+40)
		self.canva.create_line(x-self.x%40+40,y-self.y%40,x-self.x%40,y-self.y%40+40)
		
	def draw_o(self,x,y):
		self.canva.create_oval(x-self.x%40+1,y-self.y%40+1,x-self.x%40+39,y-self.y%40+39)
		
	def mouse_click(self,event):
		
		
		self.win[(event.y+self.y)//40].set_sp((event.x+self.x)//40)
		self.omov[0]=(event.y+self.y)//40
		self.omov[1]=(event.x+self.x)//40
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
		self.canva.pack()
		self.oturn=True
		self.o_turn()
		
	def expand(self):
		self.n+=2
		ret=[[] for i in range(self.n)]
		for i in range(self.n):
			ret[i]=Win(self.n)
		for i in range(1,self.n-1):
			for j in range(1,self.n-1):
				if self.win[i-1].get_sp(j-1)=="x":
					ret[i].set_sp(j)
				elif self.win[i-1].get_sp(j-1)=="o":
					ret[i].set_contr(j)
		self.win=ret
		self.x+=40
		self.y+=40
		self.boundX+=80
		self.boundY+=80
		
	def o_turn(self):
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
			if dbound-ubound>=len(temp) or rbound-lbound>=len(temp[0]):
				continue
				
			#temps=[]
			#for i in range(ubound,dbound+1):
				#temps.append([])
				#for j in range(lbound,rbound+1):
				#	temps[i-ubound].append(matrix[i][j])
			#print(temps)
			"""if temps==[["x"," "," "],[" ","x"," "],[" "," ","x"]]:
					print("sutampa")
					for i in matrix:
						for j in i:
							print(j,end="")
						print("")	
			"""
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
							#if temps==[["x"," "," "],[" ","x"," "],[" "," ","x"]]:
								#print(matrix[i][j],win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound],self.ubound+istart+i-2*ubound,self.lbound+jstart+j-2*lbound,i,j)
							#if self.ubound+istart+i-2>=0 and self.ubound+istart+i-2<n and self.lbound+jstart+j-2>=0 and self.lbound+jstart+j-2<n:
							if matrix[i][j]=="x" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]!="x" or matrix[i][j]=="*" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]!=" " or matrix[i][j]=="+" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]=="o":
								#print(win[self.ubound+istart+i-1].sp[self.lbound+jstart+j-1],matrix[i][j],self.ubound+istart+i-1,self.lbound+jstart+j-1,i,j)
								o=True
								#print("kitas")
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
				ocord=ocords[random.randrange(len(ocords)-1)]
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
				str=messagebox.askyesno("You won!","Yes if you want to restart game and no if you want to quit")
				if str==True:
					self.canva.pack_forget()
					self.canva.delete("all")
					self.n=33
					self.win=[[] for i in range(self.n)]
					for i in range(self.n):
						self.win[i]=Win(self.n)
					self.gameWin=False
					self.gameLost=False
					self.oturn=False
					self.f=open("mem.txt","rb")
					self.mem=pickle.load(self.f)
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
					self.i=0
					self.j=0
					self.x=0
					self.y=0
					self.scrollWidth=40
					self.speed=2
					self.boundX=280
					self.boundY=280
					self.update_map()
					self.canva.pack()
				else:
					self.quit()
			elif self.gameLost==True:
				str=messagebox.askyesno("You Lost!","Yes if you want to restart game and no if you want to quit")
				if(str==True):
					self.canva.pack_forget()
					self.canva.delete("all")
					self.n=33
					self.win=[[] for i in range(self.n)]
					for i in range(self.n):
						self.win[i]=Win(self.n)
					self.gameWin=False
					self.gameLost=False
					self.oturn=False
					self.f=open("mem.txt","rb")
					self.mem=pickle.load(self.f)
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
					self.i=0
					self.j=0
					self.x=0
					self.y=0
					self.scrollWidth=40
					self.speed=2
					self.boundX=280
					self.boundY=280
					self.update_map()
					self.canva.pack()
				else:
					self.quit()

app=Application()
app.master.title('Tic_Tac_Toe')
app.master.geometry('1000x1000')
app.mainloop()

