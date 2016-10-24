import socket
import threading
import time
import pickle
import sys

HOST = '192.168.1.71'            
PORT = 50007             

HOST=input("Which ip address you would like to list? ")
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
except:
	print("Ip address or port number is not valid!")
	print("Press any key to exit...")
	input()
	sys.exit()\
	
	
s.listen(2)

print("Server has been started on ",HOST,":",PORT,sep=" ")
print("Write 'exit' to terminate current server.")

con=[]
paired=[]
usr=0
pairs=0
terminate=False
FPS=25
serverDown=False

def delete(i):
	del con[i]
	if usr>i:
		for j in range(i,usr):
			con[j].set(j)


class Con(threading.Thread):
	def __init__(self,conn,addr,i):
		threading.Thread.__init__(self)
		self.conn=conn
		self.addr=addr
		self.rez=[]
		self.paired=False
		self.i=i
		self.pos=0
		self.turn=0
		self.move=None
		self.contr=None
		self.ex=False
		self.isReady=True
		self.ext=False
		self.MS=None
		self.MR=None
		self.mRunning=True
		self.mleft=False
	def run(self):
		global usr
		NS=0
		while True:
			#print(self.pos)
			#time.sleep(2/FPS)
			if serverDown:
				break
			try:
				self.conn.sendall(pickle.dumps([self.contr,self.MR,self.pos,self.turn,self.ex,self.ext,self.mleft]))
				self.MR=None
			except:
				print("Connection has been terminated with:",self.addr)
				self.conn.close()
				break
			self.conn.settimeout(1/(FPS*2))
			try:
				self.rez=pickle.loads(self.conn.recv(1024))
				if self.rez[0]!=None:
					self.contr=None
				if self.rez[2]!=None:
					self.move=self.rez[2]
					#print(self.move)
				if self.rez[3]:
					self.pos=0
					self.turn=0
					self.move=None
					self.contr=None
					self.ex=True
				self.isReady=self.rez[4]
				if not self.paired:
					self.ex=False
				if len(self.rez)==6 and not self.rez[5]:
					self.ext=False
				if not self.rez[6]:
					self.mRunning=False
				if self.rez[1]!=None:
					self.MS=self.rez[1]
				#print("connected")
				NS=0
			except socket.timeout:
				#print("No response from: ",self.addr)
				NS+=1
			except ConnectionResetError:
				print("Connection has been terminated with: ",self.addr)
				self.conn.close()
				break
			except:
				print("Connection has been terminated with1: ",self.addr)
				self.conn.close()
				break
			if NS>=25:
				self.conn.close()
				break
			
			
			#print(self.rez)
		usr-=1
		delete(self.i)
	def set(self,i):
		self.i=i
		
			
			

class Check(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global pairs
		while True:
			time.sleep(1/FPS)
			if serverDown:
				break
			if usr>1:
				for i in range(usr):
					for j in range(usr):
						if i!=j and not con[i].paired and not con[j].paired and con[j].isReady and con[i].isReady:
							paired.append(Paired(con[i],con[j],pairs))
							paired[pairs].start()
							pairs+=1
							con[i].paired=True
							con[j].paired=True
							print("Match started.",paired[pairs-1])

			

class Look(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global usr
		global s
		while True:
			time.sleep(1/FPS)
			if terminate:
				break
			if serverDown:
				break
			s.settimeout(1/FPS)
			try:
				conn, addr = s.accept()
			except socket.timeout:
				continue
			con.append(Con(conn,addr,usr))
			print("Connected:",  addr)
			#print(con)
			con[usr].start()
			usr+=1
			

class Paired(threading.Thread):
	def __init__(self,p1,p2,i):
		threading.Thread.__init__(self)
		self.p1=p1
		self.p2=p2
		self.i=i
	def run(self):
		#global pairs
		#print("start")
		self.p1.pos=1
		self.p1.turn=1
		self.p2.pos=2
		self.p2.turn=2
		while True:
			time.sleep(1/FPS)
			if self.p1.turn==1 and self.p1.move!=None:
				self.p1.turn=2
				self.p2.turn=1
				self.p2.contr=self.p1.move
				self.p1.move=None
			if self.p2.turn==1 and self.p2.move!=None:
				self.p2.turn=2
				self.p1.turn=1
				self.p1.contr=self.p2.move
				self.p2.move=None
		
			if self.p1.ex or self.p2.ex:
				#print(self.p1.ex,self.p2.ex)
				self.p1.ex=False
				self.p2.ex=False
				self.p1.paired=False
				self.p2.paired=False
				break
				
			if not self.p1.isAlive():
				#print("Player-1 has left")
				self.p2.ext=True
				self.p2.turn=0
				self.p2.pos=0
				self.p2.move=None
				self.p2.contr=None
				self.p2.paired=False
				break
			if not self.p2.isAlive():
				#print("Player-2 has left")
				self.p1.turn=0
				self.p1.pos=0
				self.p1.move=None
				self.p1.contr=None
				self.p1.ext=True
				self.p1.paired=False
				break
			
			if self.p1.MS!=None:
				self.p2.MR=self.p1.MS
				self.p1.MS=None
			if self.p2.MS!=None:
				self.p1.MR=self.p2.MS
				self.p2.MS=None
				
			if not self.p1.mRunning:
				self.p2.mleft=True
			if not self.p2.mRunning:
				self.p1.mleft=True
			if serverDown:
				break

		print("Match has ended.")
		delete_pair(self.i)
					
	def set(self,i):
		self.i=i
				
def delete_pair(i):
	#print(paired)
	#print(i)
	#print(pairs)
	global pairs
	pairs-=1
	del paired[i]
	if pairs>i:
		for j in range(i,pairs):
			paired[j].set(j)	
			
class Commander(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.com=""
	def run(self):
		global serverDown
		while True:
			self.com=input()
			if self.com=="exit":
				print("Shutting down server...")
				serverDown=True
				break
			elif self.com=="show matches":
				print(paired)
			elif self.com=="show players":
				print(con)
			else:
				print("Unknown command.")
			

look=Look()
check=Check()
commander=Commander()
look.start()
check.start()
commander.start()







