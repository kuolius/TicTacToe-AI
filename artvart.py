import pickle
import random
import time
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

		
class Game:
	def __init__(self):
		self.n=33
		self.win=[[] for i in range(self.n)]
		for i in range(self.n):
			self.win[i]=Win(self.n)
		self.gameWin=False
		self.gameLost=False
		self.oturn=True
		self.xturn=False
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
		self.end=False
		self.boundwidth=0
		self.boundheight=0
		
	
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
		
		
	def o_turn(self):
		win=self.win
		gameWin=self.gameWin
		gameLost=self.gameLost
		oturn=self.oturn
		n=self.n
		pressure=False
		
		
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
		
		#Shrinks to the bounds
		temp=[]
		for i in range(self.ubound,self.dbound+1):
			temp.append([])
			for j in range(self.lbound,self.rbound+1):
				temp[i-self.ubound].append(self.win[i].sp[j])
		
		#checking 4 o in a row agressive
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
							if matrix[i][j]=="x" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]!="x" or matrix[i][j]=="*" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]!=" " or matrix[i][j]=="+" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]=="o":
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
		# first move
		if oturn:
			win[1].set_contr(1)
			self.mov[0]=1
			self.mov[1]=1
			oturn=False
					
		
		

	#checking if win
		for i in range(n):
			if gameWin==True:
				break
			for j in range(n):
				if i<n-4 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j)=="o" and win[i+2].get_sp(j)=="o" and win[i+3].get_sp(j)=="o" and win[i+4].get_sp(j)=="o":
					gameWin=True
					break
				if j<n-4 and win[i].get_sp(j)=="o" and win[i].get_sp(j+1)=="o" and win[i].get_sp(j+2)=="o" and win[i].get_sp(j+3)=="o" and win[i].get_sp(j+4)=="o":
					gameWin=True
					break
				if j<n-4 and i<n-4 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j+1)=="o" and win[i+2].get_sp(j+2)=="o" and win[i+3].get_sp(j+3)=="o" and win[i+4].get_sp(j+4)=="o":
					gameWin=True
					break
				if j>=4 and i<n-4 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j-1)=="o" and win[i+2].get_sp(j-2)=="o" and win[i+3].get_sp(j-3)=="o" and win[i+4].get_sp(j-4)=="o":
					gameWin=True
					break
		
		self.win=win
		self.gameWin=gameWin
		
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
		#if self.gameWin:
			#pressure=True
		temp=[]
		for i in range(self.ubound-1,self.dbound+2):
			temp.append([])
			for j in range(self.lbound-1,self.rbound+2):
				if i>=0 and i<n and j>=0 and j<n:
					temp[i-self.ubound+1].append(self.win[i].sp[j])
				else:
					temp[i-self.ubound+1].append(" ")
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
		#self.omov[0]-=self.ubound-1
		#self.omov[1]-=self.lbound-1
		if expand:
			self.mov[0]+=1
			self.mov[1]+=1
			#self.omov[0]+=1
			#self.omov[1]+=1
		self.movm.append([temp,[self.mov[0],self.mov[1]],[self.omov[0],self.omov[1]],pressure,"o"])
		
		#print(self.movm[-1])
		for i in self.movm[-1][0]:
			for j in i:
				print(j,end="")
			print("")
		if pressure:
			print("FORCED")
		print("O-Turn")
		print("O-Move:",self.movm[-1][1])
		print("X-Move:",self.movm[-1][2])
		
		
		if self.gameWin==True:
			index=0

			for i in range(len(self.movm)-1,0,-1):
				if not self.movm[i][3] and self.movm[i][4]=="x":
					index=i                 
					break
			for i in range(len(self.movm[index+1][0])):
				for j in range(len(self.movm[index+1][0][i])):
					if self.movm[index+1][0][i][j]=="x":
						self.movm[index+1][0][i][j]="o"
					elif self.movm[index+1][0][i][j]=="o":
						self.movm[index+1][0][i][j]="x"
			print("Laimejo-O:")
			for i in self.movm[index+1][0]:
				for j in i:
					print(j,end="")
				print("")
			print(self.movm[index+1][1],self.movm[index+1][2])
			temp=[]
			for i in range(len(self.movm[index+1][0])):
				temp.append([])
				for j in range(len(self.movm[index+1][0][0])):
					if self.movm[index+1][0][i][j]!="o"  and (i==self.movm[index+1][1][0]+1 and j==self.movm[index+1][1][1]+1 or i==self.movm[index+1][1][0]+2 and j==self.movm[index+1][1][1]+2 or i==self.movm[index+1][1][0]+3 and j==self.movm[index+1][1][1]+3 or i==self.movm[index+1][1][0]+4 and j==self.movm[index+1][1][1]+4 or i==self.movm[index+1][1][0]+1 and j==self.movm[index+1][1][1] or i==self.movm[index+1][1][0]+2 and j==self.movm[index+1][1][1] or i==self.movm[index+1][1][0]+3 and j==self.movm[index+1][1][1] or i==self.movm[index+1][1][0]+4 and j==self.movm[index+1][1][1] or i==self.movm[index+1][1][0]+1 and j==self.movm[index+1][1][1]-1 or i==self.movm[index+1][1][0]+2 and j==self.movm[index+1][1][1]-2 or i==self.movm[index+1][1][0]+3 and j==self.movm[index+1][1][1]-3 or i==self.movm[index+1][1][0]+4 and j==self.movm[index+1][1][1]-4 or  i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]-1 or i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]-2 or i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]-3 or  i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]-4 or i==self.movm[index+1][1][0]-1 and j==self.movm[index+1][1][1]-1 or i==self.movm[index+1][1][0]-2 and j==self.movm[index+1][1][1]-2 or i==self.movm[index+1][1][0]-3 and j==self.movm[index+1][1][1]-3 or i==self.movm[index+1][1][0]-4 and j==self.movm[index+1][1][1]-4 or i==self.movm[index+1][1][0]-1 and j==self.movm[index+1][1][1] or  i==self.movm[index+1][1][0]-2 and j==self.movm[index+1][1][1] or i==self.movm[index+1][1][0]-3 and j==self.movm[index+1][1][1] or i==self.movm[index+1][1][0]-4 and j==self.movm[index+1][1][1] or  i==self.movm[index+1][1][0]-1 and j==self.movm[index+1][1][1]+1 or  i==self.movm[index+1][1][0]-2 and j==self.movm[index+1][1][1]+2 or  i==self.movm[index+1][1][0]-3 and j==self.movm[index+1][1][1]+3 or i==self.movm[index+1][1][0]-4 and j==self.movm[index+1][1][1]+4 or  i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]+1 or i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]+2 or i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]+3 or  i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]+4 or  i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]):
						if  i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]:
							#print("Sutampa:",self.movm[index+1][1][0],self.movm[index+1][1][1])
							temp[i].append("*")
						elif self.movm[index+1][0][i][j]==" ":
							temp[i].append("+")
						else:
							temp[i].append(self.movm[index+1][0][i][j])
					else:
						if i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1] and (i==self.movm[index+1][1][0]+1 and j==self.movm[index+1][1][1]+1 or i==self.movm[index+1][1][0]+2 and j==self.movm[index+1][1][1]+2 or i==self.movm[index+1][1][0]+3 and j==self.movm[index+1][1][1]+3 or i==self.movm[index+1][1][0]+4 and j==self.movm[index+1][1][1]+4 or i==self.movm[index+1][1][0]+1 and j==self.movm[index+1][1][1] or i==self.movm[index+1][1][0]+2 and j==self.movm[index+1][1][1] or i==self.movm[index+1][1][0]+3 and j==self.movm[index+1][1][1] or i==self.movm[index+1][1][0]+4 and j==self.movm[index+1][1][1] or i==self.movm[index+1][1][0]+1 and j==self.movm[index+1][1][1]-1 or i==self.movm[index+1][1][0]+2 and j==self.movm[index+1][1][1]-2 or i==self.movm[index+1][1][0]+3 and j==self.movm[index+1][1][1]-3 or i==self.movm[index+1][1][0]+4 and j==self.movm[index+1][1][1]-4 or  i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]-1 or i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]-2 or i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]-3 or  i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]-4 or i==self.movm[index+1][1][0]-1 and j==self.movm[index+1][1][1]-1 or i==self.movm[index+1][1][0]-2 and j==self.movm[index+1][1][1]-2 or i==self.movm[index+1][1][0]-3 and j==self.movm[index+1][1][1]-3 or i==self.movm[index+1][1][0]-4 and j==self.movm[index+1][1][1]-4 or i==self.movm[index+1][1][0]-1 and j==self.movm[index+1][1][1] or  i==self.movm[index+1][1][0]-2 and j==self.movm[index+1][1][1] or i==self.movm[index+1][1][0]-3 and j==self.movm[index+1][1][1] or i==self.movm[index+1][1][0]-4 and j==self.movm[index+1][1][1] or  i==self.movm[index+1][1][0]-1 and j==self.movm[index+1][1][1]+1 or  i==self.movm[index+1][1][0]-2 and j==self.movm[index+1][1][1]+2 or  i==self.movm[index+1][1][0]-3 and j==self.movm[index+1][1][1]+3 or i==self.movm[index+1][1][0]-4 and j==self.movm[index+1][1][1]+4 or  i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]+1 or i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]+2 or i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]+3 or  i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1]+4 ):
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
			
			#print(temp1)
			f=open("mem.txt","wb")
			pickle.dump(self.mem+[temp1],f)
			f.close()
			memedit.clear()
			self.end=True
	
	
			
		self.xturn=True
			
				
	def x_turn(self):
		win=self.win
		gameLost=self.gameLost
		xturn=self.xturn
		n=self.n
		pressure=False
		
		
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
		
		#checking 4 x in a row agressive
		for i in range(n):
			if xturn==False:
				break
			for j in range(n):
				if i<n-3 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j)=="x" and  win[i+2].get_sp(j)=="x" and win[i+3].get_sp(j)=="x" and i+4<n  and win[i+4].get_sp(j)!="o"and win[i+4].get_sp(j)!="x" :
					win[i+4].set_sp(j)
					self.omov[0]=i+4
					self.omov[1]=j
					xturn=False
					break
				elif i<n-3 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j)=="x" and  win[i+2].get_sp(j)=="x" and win[i+3].get_sp(j)=="x" and i-1>=0 and win[i-1].get_sp(j)!="o"and win[i-1].get_sp(j)!="x":
					win[i-1].set_sp(j)
					self.omov[0]=i-1
					self.omov[1]=j
					xturn=False
					break
				if j<n-3 and win[i].get_sp(j)=="x" and win[i].get_sp(j+1)=="x" and win[i].get_sp(j+2)=="x" and win[i].get_sp(j+3)=="x" and j+4<n  and win[i].get_sp(j+4)!="o"and win[i].get_sp(j+4)!="x":
					win[i].set_sp(j+4)
					self.omov[0]=i
					self.omov[1]=j+4
					xturn=False
					break
				elif j<n-3 and win[i].get_sp(j)=="x" and win[i].get_sp(j+1)=="x" and win[i].get_sp(j+2)=="x" and win[i].get_sp(j+3)=="x" and j-1>=0 and win[i].get_sp(j-1)!="o"and win[i].get_sp(j-1)!="x":
					win[i].set_sp(j-1)
					self.omov[0]=i
					self.omov[1]=j-1
					xturn=False
					break
				if j<n-3 and i<n-3 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j+1)=="x" and win[i+2].get_sp(j+2)=="x" and win[i+3].get_sp(j+3)=="x" and i+4<n and j+4<n  and win[i+4].get_sp(j+4)!="o"and win[i+4].get_sp(j+4)!="x":
					win[i+4].set_sp(j+4)
					self.omov[0]=i+4
					self.omov[1]=j+4
					xturn=False
					break
				elif j<n-3 and i<n-3 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j+1)=="x" and win[i+2].get_sp(j+2)=="x" and win[i+3].get_sp(j+3)=="x" and i-1>=0 and j-1>=0 and win[i-1].get_sp(j-1)!="o"and win[i-1].get_sp(j-1)!="x":
					win[i-1].set_sp(j-1)
					self.omov[0]=i-1
					self.omov[1]=j-1
					xturn=False
					break
				if j>=3 and i<n-3 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j-1)=="x" and win[i+2].get_sp(j-2)=="x" and win[i+3].get_sp(j-3)=="x" and i+4<n and j-4>=0 and win[i+4].get_sp(j-4)!="o"and win[i+4].get_sp(j-4)!="x":
					win[i+4].set_sp(j-4)
					self.omov[0]=i+4
					self.omov[1]=j-4
					xturn=False
					break
				elif j>=3 and i<n-3 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j-1)=="x" and win[i+2].get_sp(j-2)=="x" and win[i+3].get_sp(j-3)=="x"  and i-1>=0 and j+1<n and win[i-1].get_sp(j+1)!="o"and win[i-1].get_sp(j+1)!="x":
					win[i-1].set_sp(j+1)
					self.omov[0]=i-1
					self.omov[1]=j+1
					xturn=False
					break
		
		
		#checking 4 o in a row defensive
		for i in range(n):
			if xturn==False:
				break
			for j in range(n):
				if i<n-3 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j)=="o" and  win[i+2].get_sp(j)=="o" and win[i+3].get_sp(j)=="o" and i+4<n  and win[i+4].get_sp(j)!="o"and win[i+4].get_sp(j)!="x" :
					win[i+4].set_sp(j)
					self.omov[0]=i+4
					self.omov[1]=j
					pressure=True
					xturn=False
					break
				elif i<n-3 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j)=="o" and  win[i+2].get_sp(j)=="o" and win[i+3].get_sp(j)=="o" and i-1>=0 and win[i-1].get_sp(j)!="o"and win[i-1].get_sp(j)!="x":
					win[i-1].set_sp(j)
					self.omov[0]=i-1
					self.omov[1]=j
					pressure=True
					xturn=False
					break
				if j<n-3 and win[i].get_sp(j)=="o" and win[i].get_sp(j+1)=="o" and win[i].get_sp(j+2)=="o" and win[i].get_sp(j+3)=="o" and j+4<n  and win[i].get_sp(j+4)!="o"and win[i].get_sp(j+4)!="x":
					win[i].set_sp(j+4)
					self.omov[0]=i
					self.omov[1]=j+4
					xturn=False
					pressure=True
					break
				elif j<n-3 and win[i].get_sp(j)=="o" and win[i].get_sp(j+1)=="o" and win[i].get_sp(j+2)=="o" and win[i].get_sp(j+3)=="o" and j-1>=0 and win[i].get_sp(j-1)!="o"and win[i].get_sp(j-1)!="x":
					win[i].set_sp(j-1)
					self.omov[0]=i
					self.omov[1]=j-1
					xturn=False
					pressure=True
					break
				if j<n-3 and i<n-3 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j+1)=="o" and win[i+2].get_sp(j+2)=="o" and win[i+3].get_sp(j+3)=="o" and i+4<n and j+4<n  and win[i+4].get_sp(j+4)!="o"and win[i+4].get_sp(j+4)!="x":
					win[i+4].set_sp(j+4)
					self.omov[0]=i+4
					self.omov[1]=j+4
					xturn=False
					pressure=True
					break
				elif j<n-3 and i<n-3 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j+1)=="o" and win[i+2].get_sp(j+2)=="o" and win[i+3].get_sp(j+3)=="o" and i-1>=0 and j-1>=0 and win[i-1].get_sp(j-1)!="o"and win[i-1].get_sp(j-1)!="x":
					win[i-1].set_sp(j-1)
					self.omov[0]=i-1
					self.omov[1]=j-1
					xturn=False
					pressure=True
					break
				if j>=3 and i<n-3 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j-1)=="o" and win[i+2].get_sp(j-2)=="o" and win[i+3].get_sp(j-3)=="o" and i+4<n and j-4>=0 and win[i+4].get_sp(j-4)!="o"and win[i+4].get_sp(j-4)!="x":
					win[i+4].set_sp(j-4)
					self.omov[0]=i+4
					self.omov[1]=j-4
					xturn=False
					pressure=True
					break
				elif j>=3 and i<n-3 and win[i].get_sp(j)=="o" and win[i+1].get_sp(j-1)=="o" and win[i+2].get_sp(j-2)=="o" and win[i+3].get_sp(j-3)=="o"  and i-1>=0 and j+1<n and win[i-1].get_sp(j+1)!="o"and win[i-1].get_sp(j+1)!="x":
					win[i-1].set_sp(j+1)
					self.omov[0]=i-1
					self.omov[1]=j+1
					xturn=False
					pressure=True
					break
			
		#agressive defense
		o=False
		b=False
		indexi=0
		indexj=0
		for matrix in self.mem:
			if xturn==False:
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
						win[indexi].set_sp(indexj)
						self.omov[0]=indexi
						self.omov[1]=indexj
						#print(indexi,indexj)
						xturn=False
						pressure=True
						break
						
		#agressive respond
		o=False
		b=False
		indexi=0
		indexj=0
		for matrix in self.mem:
			if xturn==False:
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
							if matrix[i][j]=="x" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]!="x" or matrix[i][j]=="*" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]!=" " or matrix[i][j]=="+" and win[self.ubound+istart+i-ubound].sp[self.lbound+jstart+j-lbound]=="o":
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
						win[indexi].set_sp(indexj)
						self.omov[0]=indexi
						self.omov[1]=indexj
						#print(indexi,indexj)
						xturn=False
						break
		
        #	checking 1 x
		if xturn:
			ocords=[]
			for i in range(n):
				for j in range(n):
					if win[i].get_sp(j)=="x" and (win[i+1].get_sp(j)==" " or win[i-1].get_sp(j)==" " or win[i].get_sp(j+1)==" " or win[i].get_sp(j-1)==" " or win[i-1].get_sp(j+1)==" " or win[i-1].get_sp(j-1)==" " or win[i+1].get_sp(j+1)==" " or win[i+1].get_sp(j-1)==" "):
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
				win[xcord[0]].set_sp(xcord[1])
				self.omov[0]=xcord[0]
				self.omov[1]=xcord[1]
				xturn=False
			else:
				for i in range(n):
					if xturn==False:
						break
					for j in range(n):
						if win[i].get_sp(j)=="o" and j+1<n and win[i].get_sp(j+1)!="o" and win[i].get_sp(j+1)!="x":
							win[i].set_sp(j+1)
							self.omov[0]=i
							self.omov[1]=j+1
							xturn=False
							break
						elif win[i].get_sp(j)=="o" and win[i].get_sp(j-1)!="o" and win[i].get_sp(j-1)!="x":
							win[i].set_sp(j-1)
							self.omov[0]=i
							self.omov[1]=j-1
							xturn=False
							break
	
		for i in range(n):
			if gameLost==True:
				break
			for j in range(n):
				if i<n-4 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j)=="x" and win[i+2].get_sp(j)=="x" and win[i+3].get_sp(j)=="x" and win[i+4].get_sp(j)=="x":
					gameLost=True
					break
				if j<n-4 and win[i].get_sp(j)=="x" and win[i].get_sp(j+1)=="x" and win[i].get_sp(j+2)=="x" and win[i].get_sp(j+3)=="x" and win[i].get_sp(j+4)=="x":
					gameLost=True
					break
				if j<n-4 and i<n-4 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j+1)=="x" and win[i+2].get_sp(j+2)=="x" and win[i+3].get_sp(j+3)=="x" and win[i+4].get_sp(j+4)=="x":
					gameLost=True
					break
				if j>=4 and i<n-4 and win[i].get_sp(j)=="x" and win[i+1].get_sp(j-1)=="x" and win[i+2].get_sp(j-2)=="x" and win[i+3].get_sp(j-3)=="x" and win[i+4].get_sp(j-4)=="x":
					gameLost=True
					break
		#print("X-MoveReal:",self.omov)
		self.win=win
		self.gameLost=gameLost
		self.xturn=xturn
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
		#if self.gameLost:
			#pressure=True
		temp=[]
		for i in range(self.ubound-1,self.dbound+2):
			temp.append([])
			for j in range(self.lbound-1,self.rbound+2):
				if i<n and i>=0 and j<n and j>=0:
					temp[i-self.ubound+1].append(self.win[i].sp[j])
				else:
					temp[i-self.ubound+1].append(" ")
					
		expands=0
		if expand:
			expands=1
		if self.boundwidth>self.lbound-expands:
			self.mov[1]+=1
		if self.boundheight>self.ubound-expands:
			self.mov[0]+=1
			
		self.boundheight=self.ubound
		self.boundwidth=self.lbound
		#self.mov[0]-=self.ubound-1
		#self.mov[1]-=self.lbound-1
		self.omov[0]-=self.ubound-1
		self.omov[1]-=self.lbound-1
		if expand:
			#self.mov[0]+=1
			#self.mov[1]+=1
			self.omov[0]+=1
			self.omov[1]+=1
		self.movm.append([temp,[self.mov[0],self.mov[1]],[self.omov[0],self.omov[1]],pressure,"x"])
		#print(self.movm)
		for i in self.movm[-1][0]:
			for j in i:
				print(j,end="")
			print("")
		if pressure:
			print("FORCED")
		print("X-Turn")
		print("O-Move:",self.movm[-1][1])
		print("X-Move:",self.movm[-1][2])
	
		
		
		if self.gameLost==True:
			index=0
			
			for i in range(len(self.movm)-1,0,-1):
				if not self.movm[i][3] and self.movm[i][4]=="o":
					index=i                 
					break
			print("Laimejo-X:")
			for i in self.movm[index+1][0]:
				for j in i:
					print(j,end="")
				print("")
			print(self.movm[index+1][1],self.movm[index+1][2])
			temp=[]
			for i in range(len(self.movm[index+1][0])):
				temp.append([])
				for j in range(len(self.movm[index+1][0][0])):
					if self.movm[index+1][0][i][j]!="o"  and (i==self.movm[index+1][2][0]+1 and j==self.movm[index+1][2][1]+1 or i==self.movm[index+1][2][0]+2 and j==self.movm[index+1][2][1]+2 or i==self.movm[index+1][2][0]+3 and j==self.movm[index+1][2][1]+3 or i==self.movm[index+1][2][0]+4 and j==self.movm[index+1][2][1]+4 or i==self.movm[index+1][2][0]+1 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+2 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+3 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+4 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+1 and j==self.movm[index+1][2][1]-1 or i==self.movm[index+1][2][0]+2 and j==self.movm[index+1][2][1]-2 or i==self.movm[index+1][2][0]+3 and j==self.movm[index+1][2][1]-3 or i==self.movm[index+1][2][0]+4 and j==self.movm[index+1][2][1]-4 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-1 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-2 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-3 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-4 or i==self.movm[index+1][2][0]-1 and j==self.movm[index+1][2][1]-1 or i==self.movm[index+1][2][0]-2 and j==self.movm[index+1][2][1]-2 or i==self.movm[index+1][2][0]-3 and j==self.movm[index+1][2][1]-3 or i==self.movm[index+1][2][0]-4 and j==self.movm[index+1][2][1]-4 or i==self.movm[index+1][2][0]-1 and j==self.movm[index+1][2][1] or  i==self.movm[index+1][2][0]-2 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]-3 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]-4 and j==self.movm[index+1][2][1] or  i==self.movm[index+1][2][0]-1 and j==self.movm[index+1][2][1]+1 or  i==self.movm[index+1][2][0]-2 and j==self.movm[index+1][2][1]+2 or  i==self.movm[index+1][2][0]-3 and j==self.movm[index+1][2][1]+3 or i==self.movm[index+1][2][0]-4 and j==self.movm[index+1][2][1]+4 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+1 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+2 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+3 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+4 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1] ):
						if  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]:
							temp[i].append("*")
						elif self.movm[index+1][0][i][j]==" ":
							temp[i].append("+")
						else:
							temp[i].append(self.movm[index+1][0][i][j])
					else:
						if i==self.movm[index+1][1][0] and j==self.movm[index+1][1][1] and (i==self.movm[index+1][2][0]+1 and j==self.movm[index+1][2][1]+1 or i==self.movm[index+1][2][0]+2 and j==self.movm[index+1][2][1]+2 or i==self.movm[index+1][2][0]+3 and j==self.movm[index+1][2][1]+3 or i==self.movm[index+1][2][0]+4 and j==self.movm[index+1][2][1]+4 or i==self.movm[index+1][2][0]+1 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+2 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+3 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+4 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]+1 and j==self.movm[index+1][2][1]-1 or i==self.movm[index+1][2][0]+2 and j==self.movm[index+1][2][1]-2 or i==self.movm[index+1][2][0]+3 and j==self.movm[index+1][2][1]-3 or i==self.movm[index+1][2][0]+4 and j==self.movm[index+1][2][1]-4 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-1 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-2 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-3 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]-4 or i==self.movm[index+1][2][0]-1 and j==self.movm[index+1][2][1]-1 or i==self.movm[index+1][2][0]-2 and j==self.movm[index+1][2][1]-2 or i==self.movm[index+1][2][0]-3 and j==self.movm[index+1][2][1]-3 or i==self.movm[index+1][2][0]-4 and j==self.movm[index+1][2][1]-4 or i==self.movm[index+1][2][0]-1 and j==self.movm[index+1][2][1] or  i==self.movm[index+1][2][0]-2 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]-3 and j==self.movm[index+1][2][1] or i==self.movm[index+1][2][0]-4 and j==self.movm[index+1][2][1] or  i==self.movm[index+1][2][0]-1 and j==self.movm[index+1][2][1]+1 or  i==self.movm[index+1][2][0]-2 and j==self.movm[index+1][2][1]+2 or  i==self.movm[index+1][2][0]-3 and j==self.movm[index+1][2][1]+3 or i==self.movm[index+1][2][0]-4 and j==self.movm[index+1][2][1]+4 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+1 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+2 or i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+3 or  i==self.movm[index+1][2][0] and j==self.movm[index+1][2][1]+4):
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
			self.end=True
		
		self.oturn=True
		
				
		
n=int(input("How many PC vs PC games? "))
for i in range(n):
	game=Game()
	while True:
		game.o_turn()
		#time.sleep(2)
		if game.end:
			print("pabaiga")
			break
		game.x_turn()
		if game.end:
			print("pabaiga")
			break

