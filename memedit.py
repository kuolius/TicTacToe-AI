import pickle


def max(a,b):
	if a>b:
		return a
	else:
		return b
def min(a,b):
	if a<b:
		return a
	else:
		return b

def findStar(matrix):
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			if matrix[i][j]=="*":
				return [i,j]
					
def printMatrix(matrix):
	for i in matrix:
		for j in i:
			print(j,end="")
		print("")
		
def isXH(matrix):
	center=findStar(matrix)
	o=False
	for i in range(len(matrix[center[0]])):
		if matrix[center[0]][i]=="x":
			o=True
	return o

def isXV(matrix):
	center=findStar(matrix)
	o=False
	for i in range(len(matrix)):
		if matrix[i][center[1]]=="x":
			o=True
	return o
	
def isXD(matrix):
	center=findStar(matrix)
	o=False
	for i in range(1,min(center[0]+1,center[1]+1)):
		if matrix[center[0]-i][center[1]-i]=="x":
			o=True
	for i in range(1,min(len(matrix)-center[0],len(matrix[center[0]])-center[1])):
		if matrix[center[0]+i][center[1]+i]=="x":
			o=True
	return o

def isXOD(matrix):
	center=findStar(matrix)
	o=False
	for i in range(1,min(center[0]+1,len(matrix[center[0]])-center[1])):
		if matrix[center[0]-i][center[1]+i]=="x":
			o=True
	for i in range(1,min(len(matrix)-center[0],center[1]+1)):
		if matrix[center[0]+i][center[1]-i]=="x":
			o=True
	return o
def clearH(matrix):
	center=findStar(matrix)
	for i in range(len(matrix[center[0]])):
		if matrix[center[0]][i]!="*":
			matrix[center[0]][i]=" "
def clearV(matrix):
	center=findStar(matrix)
	for i in range(len(matrix)):
		if matrix[i][center[1]]!="*":
			matrix[i][center[1]]=" "
def clearD(matrix):
	center=findStar(matrix)
	for i in range(1,min(center[0]+1,center[1]+1)):
		matrix[center[0]-i][center[1]-i]=" "
	for i in range(1,min(len(matrix)-center[0],len(matrix[center[0]])-center[1])):
		matrix[center[0]+i][center[1]+i]=" "

def clearOD(matrix):
	center=findStar(matrix)
	for i in range(1,min(center[0]+1,len(matrix[center[0]])-center[1])):
		matrix[center[0]-i][center[1]+i]=" "
	for i in range(1,min(len(matrix)-center[0],center[1]+1)):
		matrix[center[0]+i][center[1]-i]=" "

def clearHiso(matrix):
	center=findStar(matrix)
	clear=False
	for i in range(1,len(matrix[center[0]])-center[1]):
		if not clear:
			if matrix[center[0]][center[1]+i]==" ":
				clear=True
		else:
			matrix[center[0]][center[1]+i]=" "
	clear=False
	for i in range(1,center[1]+1):
		if not clear:
			if matrix[center[0]][center[1]-i]==" ":
				clear=True
		else:
			matrix[center[0]][center[1]-i]=" "

def clearViso(matrix):
	center=findStar(matrix)
	clear=False
	for i in range(1,len(matrix)-center[0]):
		if not clear:
			if matrix[center[0]+i][center[1]]==" ":
				clear=True
		else:
			matrix[center[0]+i][center[1]]=" "
	clear=False
	for i in range(1,center[0]+1):
		if not clear:
			if matrix[center[0]-i][center[1]]==" ":
				clear=True
		else:
			matrix[center[0]-i][center[1]]=" "
	
def clearDiso(matrix):
	center=findStar(matrix)
	clear=False
	for i in range(1,min(center[0]+1,center[1]+1)):
		if not clear:
			if matrix[center[0]-i][center[1]-i]==" ":
				clear=True
		else:
			matrix[center[0]-i][center[1]-i]=" "
	clear=False
	for i in range(1,min(len(matrix)-center[0],len(matrix[center[0]])-center[1])):
		if not clear:
			if matrix[center[0]+i][center[1]+i]==" ":
				clear=True
		else:
			matrix[center[0]+i][center[1]+i]=" "
			
def clearDOiso(matrix):
	center=findStar(matrix)
	clear=False
	for i in range(1,min(center[0]+1,len(matrix[center[0]])-center[1])):
		if not clear:
			if matrix[center[0]-i][center[1]+i]==" ":
				clear=True
		else:
			matrix[center[0]-i][center[1]+i]=" "
	clear=False
	for i in range(1,min(len(matrix)-center[0],center[1]+1)):
		if not clear:
			if matrix[center[0]+i][center[1]-i]==" ":
				clear=True
		else:
			matrix[center[0]+i][center[1]-i]=" "

def clearIso(matrix):
	clearHiso(matrix)
	clearViso(matrix)
	clearDiso(matrix)
	clearDOiso(matrix)

def fit(temp):
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
	return temp1
	
def checkPH(matrix,center,pattern):
	star=None
	for i in range(len(pattern)):
		if pattern[i]=="*":
			star=i
			break
	ret=True
	if center[1]+len(pattern)-star-1<len(matrix[center[0]]) and center[1]-star>=0:
		for i in range(center[1]-star,center[1]+len(pattern)-star):
			if i==center[1]-star and (pattern[0]=="x" and matrix[center[0]][i]=="x" or pattern[0]=="*" and matrix[center[0]][i]=="*")  and center[1]-star-1>=0 and (matrix[center[0]][i-1]==" " or matrix[center[0]][i-1]=="x") or i==center[1]+len(pattern)-star-1 and (pattern[-1]=="x" and matrix[center[0]][i]=="x" or pattern[-1]=="*" and matrix[center[0]][i]=="*") and center[1]+len(pattern)-star<len(matrix[center[0]]) and  (matrix[center[0]][i+1]==" " or matrix[center[0]][i+1]=="x"):
				ret=ret and True
			elif i==center[1]-star and (pattern[0]=="x" and matrix[center[0]][i]=="x" or pattern[0]=="*" and matrix[center[0]][i]=="*") and center[1]-star-1>=0 and  (matrix[center[0]][i-1]!=" " and matrix[center[0]][i-1]!="x") or i==center[1]+len(pattern)-star-1 and (pattern[-1]=="x" and matrix[center[0]][i]=="x" or pattern[-1]=="*" and matrix[center[0]][i]=="*") and center[1]+len(pattern)-star<len(matrix[center[0]]) and  (matrix[center[0]][i+1]!=" " and matrix[center[0]][i+1]!="x"):
				return False
			else:
				ret=ret and (pattern[i-center[1]+star]==matrix[center[0]][i])
			#print(pattern[i-center[1]+star],matrix[center[0]][i],ret)
	else:
		return False
	return ret
	
def checkPV(matrix,center,pattern):
	star=None
	for i in range(len(pattern)):
		if pattern[i]=="*":
			star=i
			break
	ret=True
	
	if center[0]+len(pattern)-star-1<len(matrix) and center[0]-star>=0:
		for i in range(center[0]-star,center[0]+len(pattern)-star):
			if i==center[0]-star and (pattern[0]=="x" and matrix[i][center[1]]=="x" or pattern[0]=="*" and matrix[i][center[1]]=="*")  and center[0]-star-1>=0 and (matrix[i-1][center[1]]==" " or matrix[i-1][center[1]]=="x") or i==center[0]+len(pattern)-star-1 and (pattern[-1]=="x" and matrix[i][center[1]]=="x" or pattern[-1]=="*" and matrix[i][center[1]]=="*") and center[0]+len(pattern)-star<len(matrix) and (matrix[i+1][center[1]]==" " or matrix[i+1][center[1]]=="x"):
				ret=ret and True
			elif i==center[0]-star and (pattern[0]=="x" and matrix[i][center[1]]=="x" or pattern[0]=="*" and matrix[i][center[1]]=="*") and center[0]-star-1>=0 and (matrix[i-1][center[1]]!=" "and matrix[i-1][center[1]]!="x") or i==center[0]+len(pattern)-star-1 and (pattern[-1]=="x" and matrix[i][center[1]]=="x" or pattern[-1]=="*" and matrix[i][center[1]]=="*") and center[0]+len(pattern)-star<len(matrix) and (matrix[i+1][center[1]]!=" " and matrix[i+1][center[1]]!="x"):
				ret=False
				break
			else:
				ret=ret and (pattern[i-center[0]+star]==matrix[i][center[1]])
			#print(pattern[i-center[1]+star],matrix[center[0]][i],ret)
	else:
		return False
	return ret

def checkPD(matrix,center,pattern):
	star=None
	for i in range(len(pattern)):
		if pattern[i]=="*":
			star=i
			break
	ret=True
	if min(center[0],center[1])-star>=0 and center[0]+len(pattern)-star-1<len(matrix) and center[1]+len(pattern)-star-1<len(matrix[center[0]]):
		for i in range(len(pattern)):
			if i==0 and (pattern[0]=="x" and matrix[center[0]][i]=="x" or pattern[0]=="*" and matrix[center[0]][i]=="*")  and center[0]-star-1>=0 and center[1]-star-1>=0 and (matrix[center[0]-star-1][center[1]-star-1]==" " or matrix[center[0]-star-1][center[1]-star-1]=="x") or i==len(pattern)-1 and (pattern[-1]=="x" and matrix[center[0]][i]=="x" or pattern[-1]=="*" and matrix[center[0]][i]=="*") and center[0]+len(pattern)-star<len(matrix) and center[1]+len(pattern)-star<len(matrix[center[0]]) and (matrix[center[0]+len(pattern)-star][center[1]+len(pattern)-star]==" " or matrix[center[0]+len(pattern)-star][center[1]+len(pattern)-star]=="x"):
				ret=ret and True
			elif i==0 and (pattern[0]=="x" and matrix[center[0]][i]=="x" or pattern[0]=="*" and matrix[center[0]][i]=="*") and center[0]-star-1>=0 and center[1]-star-1>=0 and (matrix[center[0]-star-1][center[1]-star-1]!=" " and matrix[center[0]-star-1][center[1]-star-1]!="x") or i==len(pattern)-1 and (pattern[-1]=="x" and matrix[center[0]][i]=="x" or pattern[-1]=="*" and matrix[center[0]][i]=="*") and center[0]+len(pattern)-star<len(matrix) and center[1]+len(pattern)-star<len(matrix[center[0]]) and (matrix[center[0]+len(pattern)-star][center[1]+len(pattern)-star]!=" " and matrix[center[0]+len(pattern)-star][center[1]+len(pattern)-star]!="x"):
				ret=False
				break
			else:
				ret=ret and (pattern[i]==matrix[center[0]-star+i][center[1]-star+i])
	else:
		return False
	return ret
	
def checkPOD(matrix,center,pattern):
	star=None
	for i in range(len(pattern)):
		if pattern[i]=="*":
			star=i
			break
	ret=True
	if center[0]-star>=0 and center[1]+star<len(matrix[center[0]]) and center[0]+len(pattern)-star-1<len(matrix) and center[1]-len(pattern)+star+1>=0:
		for i in range(len(pattern)):
			if i==0 and (pattern[0]=="x" and matrix[center[0]][i]=="x" or pattern[0]=="*" and matrix[center[0]][i]=="*") and center[0]-star-1>=0 and center[1]+star+1<len(matrix[center[0]]) and (matrix[center[0]-star-1][center[1]+star+1]==" " or matrix[center[0]-star-1][center[1]+star+1]=="x" )or i==len(pattern)-1 and (pattern[-1]=="x" and matrix[center[0]][i]=="x" or pattern[-1]=="*" and matrix[center[0]][i]=="*") and center[0]+len(pattern)-star<len(matrix) and center[1]-len(pattern)+star<len(matrix[center[0]]) and (matrix[center[0]+len(pattern)-star][center[1]-len(pattern)+star]==" " or matrix[center[0]+len(pattern)-star][center[1]-len(pattern)+star]=="x"):
				ret=ret and True
			elif i==0 and (pattern[0]=="x" and matrix[center[0]][i]=="x" or pattern[0]=="*" and matrix[center[0]][i]=="*")  and center[0]-star-1>=0 and center[1]+star+1<len(matrix[center[0]]) and (matrix[center[0]-star-1][center[1]+star+1]!=" " and matrix[center[0]-star-1][center[1]+star+1]!="x" )or i==len(pattern)-1 and (pattern[-1]=="x" and matrix[center[0]][i]=="x" or pattern[-1]=="*" and matrix[center[0]][i]=="*") and center[0]+len(pattern)-star<len(matrix) and center[1]-len(pattern)+star<len(matrix[center[0]]) and (matrix[center[0]+len(pattern)-star][center[1]-len(pattern)+star]!=" " and matrix[center[0]+len(pattern)-star][center[1]-len(pattern)+star]!="x"):
				ret=False
				break
			else:
				ret=ret and (pattern[i]==matrix[center[0]-star+i][center[1]+star-i])
	else:
		return False
	return ret
	
def ORPH(matrix,center,combs):
	ret=False
	for i in combs:
			ret=ret or checkPH(matrix,center,i)
	return ret
	
def ORPV(matrix,center,combs):
	ret=False
	for i in combs:
			ret=ret or checkPV(matrix,center,i)
	return ret
	
def ORPD(matrix,center,combs):
	ret=False
	for i in combs:
			ret=ret or checkPD(matrix,center,i)
	return ret

def ORPOD(matrix,center,combs):
	ret=False
	for i in combs:
			ret=ret or checkPOD(matrix,center,i)
	return ret
	
def findXH(matrix):
	x=0
	center=findStar(matrix)
	for i in range(len(matrix[center[0]])):
		if matrix[center[0]][i]=="x":
			x+=1
	return x
def findXV(matrix):
	x=0
	center=findStar(matrix)
	for i in range(len(matrix)):
		if matrix[i][center[1]]=="x":
			x+=1
	return x
def findXD(matrix):
	x=0
	center=findStar(matrix)
	for i in range(1,min(center[0]+1,center[1]+1)):
		if matrix[center[0]-i][center[1]-i]=="x":
			x+=1
	for i in range(1,min(len(matrix)-center[0],len(matrix[center[0]])-center[1])):
		if matrix[center[0]+i][center[1]+i]=="x":
			x+=1
	return x
def findXOD(matrix):
	x=0
	center=findStar(matrix)
	for i in range(1,min(center[0]+1,len(matrix[center[0]])-center[1])):
		if matrix[center[0]-i][center[1]+i]=="x":
			x+=1
	for i in range(1,min(len(matrix)-center[0],center[1]+1)):
		if matrix[center[0]+i][center[1]-i]=="x":
			x+=1
	return x

def validH2(matrix):
	center=findStar(matrix)
	if ORPH(matrix,center,[["+","x","+","x","*","+"],["+","*","x","+","x","+"],["+","x","x","+","*","+"],["+","*","+","x","x","+"],["+","x","+","*","x","+"],["+","x","*","+","x","+"],["+","x","x","*","+"],["+","*","x","x","+"],["+","x","*","x","+"]]):
		return True
	else:
		return False
		
def validV2(matrix):
	center=findStar(matrix)
	if ORPV(matrix,center,[["+","x","+","x","*","+"],["+","*","x","+","x","+"],["+","x","x","+","*","+"],["+","*","+","x","x","+"],["+","x","+","*","x","+"],["+","x","*","+","x","+"],["+","x","x","*","+"],["+","*","x","x","+"],["+","x","*","x","+"]]):
		return True
	else:
		return False

def validD2(matrix):
	center=findStar(matrix)
	if ORPD(matrix,center,[["+","x","+","x","*","+"],["+","*","x","+","x","+"],["+","x","x","+","*","+"],["+","*","+","x","x","+"],["+","x","+","*","x","+"],["+","x","*","+","x","+"],["+","x","x","*","+"],["+","*","x","x","+"],["+","x","*","x","+"]]):
		return True
	else:
		return False
		
def validOD2(matrix):
	center=findStar(matrix)
	if ORPOD(matrix,center,[["+","x","+","x","*","+"],["+","*","x","+","x","+"],["+","x","x","+","*","+"],["+","*","+","x","x","+"],["+","x","+","*","x","+"],["+","x","*","+","x","+"],["+","x","x","*","+"],["+","*","x","x","+"],["+","x","*","x","+"]]):
		return True
	else:
		return False
		
def validH3(matrix):
	center=findStar(matrix)
	if ORPH(matrix,center,[["x","x","x","+","*"],["x","x","x","+","*","+"],["*","+","x","x","x"],["+","*","+","x","x","x"],["x","x","x","*","+"],["+","*","x","x","x"],["x","x","*","x","+"],["+","x","*","x","x"],["x","*","x","x","+"],["+","x","x","*","x"],["*","x","x","x","+"],["+","x","x","x","*"],["x","+","x","x","*"],["x","+","x","x","*","+"],["*","x","x","+","x"],["+","*","x","x","+","x"],["x","+","x","*","x"],["x","+","x","*","x","+"],["+","x","+","x","*","x"],["+","x","+","x","*","x","+"],["x","*","x","+","x"],["x","*","x","+","x","+"],["+","x","*","x","+","x"],["+","x","*","x","+","x","+"],["x","+","*","x","x"],["x","+","*","x","x","+"],["+","x","+","*","x","x"],["+0","x","+","*","x","x","+"],["x","x","*","+","x"],["x","x","*","+","x","+"],["+","x","x","*","+","x"],["+","x","x","*","+","x","+"],["x","*","+","x","x"],["x","*","+","x","x","+"],["+","x","*","+","x","x"],["+","x","*","+","x","x","+"],["x","x","+","*","x"],["x","x","+","*","x","+"],["+","x","x","+","*","x"],["+","x","x","+","*","x","+"],["*","x","+","x","x"],["+","*","x","+","x","x"],["x","x","+","x","*"],["x","x","+","x","*","+"]]):
		return True
	else:
		return False
		
def validV3(matrix):
	center=findStar(matrix)
	if ORPV(matrix,center,[["x","x","x","+","*"],["x","x","x","+","*","+"],["*","+","x","x","x"],["+","*","+","x","x","x"],["x","x","x","*","+"],["+","*","x","x","x"],["x","x","*","x","+"],["+","x","*","x","x"],["x","*","x","x","+"],["+","x","x","*","x"],["*","x","x","x","+"],["+","x","x","x","*"],["x","+","x","x","*"],["x","+","x","x","*","+"],["*","x","x","+","x"],["+","*","x","x","+","x"],["x","+","x","*","x"],["x","+","x","*","x","+"],["+","x","+","x","*","x"],["+","x","+","x","*","x","+"],["x","*","x","+","x"],["x","*","x","+","x","+"],["+","x","*","x","+","x"],["+","x","*","x","+","x","+"],["x","+","*","x","x"],["x","+","*","x","x","+"],["+","x","+","*","x","x"],["+0","x","+","*","x","x","+"],["x","x","*","+","x"],["x","x","*","+","x","+"],["+","x","x","*","+","x"],["+","x","x","*","+","x","+"],["x","*","+","x","x"],["x","*","+","x","x","+"],["+","x","*","+","x","x"],["+","x","*","+","x","x","+"],["x","x","+","*","x"],["x","x","+","*","x","+"],["+","x","x","+","*","x"],["+","x","x","+","*","x","+"],["*","x","+","x","x"],["+","*","x","+","x","x"],["x","x","+","x","*"],["x","x","+","x","*","+"]]):
		return True
	else:
		return False
		
def validD3(matrix):
	center=findStar(matrix)
	if ORPD(matrix,center,[["x","x","x","+","*"],["x","x","x","+","*","+"],["*","+","x","x","x"],["+","*","+","x","x","x"],["x","x","x","*","+"],["+","*","x","x","x"],["x","x","*","x","+"],["+","x","*","x","x"],["x","*","x","x","+"],["+","x","x","*","x"],["*","x","x","x","+"],["+","x","x","x","*"],["x","+","x","x","*"],["x","+","x","x","*","+"],["*","x","x","+","x"],["+","*","x","x","+","x"],["x","+","x","*","x"],["x","+","x","*","x","+"],["+","x","+","x","*","x"],["+","x","+","x","*","x","+"],["x","*","x","+","x"],["x","*","x","+","x","+"],["+","x","*","x","+","x"],["+","x","*","x","+","x","+"],["x","+","*","x","x"],["x","+","*","x","x","+"],["+","x","+","*","x","x"],["+0","x","+","*","x","x","+"],["x","x","*","+","x"],["x","x","*","+","x","+"],["+","x","x","*","+","x"],["+","x","x","*","+","x","+"],["x","*","+","x","x"],["x","*","+","x","x","+"],["+","x","*","+","x","x"],["+","x","*","+","x","x","+"],["x","x","+","*","x"],["x","x","+","*","x","+"],["+","x","x","+","*","x"],["+","x","x","+","*","x","+"],["*","x","+","x","x"],["+","*","x","+","x","x"],["x","x","+","x","*"],["x","x","+","x","*","+"]]):
		return True
	else:
		return False
		
def validOD3(matrix):
	center=findStar(matrix)
	if ORPOD(matrix,center,[["x","x","x","+","*"],["x","x","x","+","*","+"],["*","+","x","x","x"],["+","*","+","x","x","x"],["x","x","x","*","+"],["+","*","x","x","x"],["x","x","*","x","+"],["+","x","*","x","x"],["x","*","x","x","+"],["+","x","x","*","x"],["*","x","x","x","+"],["+","x","x","x","*"],["x","+","x","x","*"],["x","+","x","x","*","+"],["*","x","x","+","x"],["+","*","x","x","+","x"],["x","+","x","*","x"],["x","+","x","*","x","+"],["+","x","+","x","*","x"],["+","x","+","x","*","x","+"],["x","*","x","+","x"],["x","*","x","+","x","+"],["+","x","*","x","+","x"],["+","x","*","x","+","x","+"],["x","+","*","x","x"],["x","+","*","x","x","+"],["+","x","+","*","x","x"],["+0","x","+","*","x","x","+"],["x","x","*","+","x"],["x","x","*","+","x","+"],["+","x","x","*","+","x"],["+","x","x","*","+","x","+"],["x","*","+","x","x"],["x","*","+","x","x","+"],["+","x","*","+","x","x"],["+","x","*","+","x","x","+"],["x","x","+","*","x"],["x","x","+","*","x","+"],["+","x","x","+","*","x"],["+","x","x","+","*","x","+"],["*","x","+","x","x"],["+","*","x","+","x","x"],["x","x","+","x","*"],["x","x","+","x","*","+"]]):
		return True
	else:
		return False
		
		

		
def valid(matrix):
	
	if findXH(matrix)>2 or findXV(matrix)>2 or findXD(matrix)>2 or findXOD(matrix)>2:
		if ORPH(matrix,findStar(matrix),[["+","x","x","x","*","+"],["+","*","x","x","x","+"],["+","x","x","*","x","+"],["+","x","*","x","x","+"],["x","x","x","x","*"],["*","x","x","x","x"],["x","x","x","*","x"],["x","*","x","x","x"],["x","x","*","x","x"],["x","x","x","x","*","+"],["+","*","x","x","x","x"],["+","x","x","x","*","x"],["x","x","x","*","x","+"],["+","x","x","x","*","x","+"],["+","x","*","x","x","x"],["x","*","x","x","x","+"],["+","x","*","x","x","x","+"],["x","x","*","x","x","+"],["+","x","x","*","x","x"],["+","x","x","*","x","x","+"]]) or ORPV(matrix,findStar(matrix),[["+","x","x","x","*","+"],["+","*","x","x","x","+"],["+","x","x","*","x","+"],["+","x","*","x","x","+"],["x","x","x","x","*"],["*","x","x","x","x"],["x","x","x","*","x"],["x","*","x","x","x"],["x","x","*","x","x"],["x","x","x","x","*","+"],["+","*","x","x","x","x"],["+","x","x","x","*","x"],["x","x","x","*","x","+"],["+","x","x","x","*","x","+"],["+","x","*","x","x","x"],["x","*","x","x","x","+"],["+","x","*","x","x","x","+"],["x","x","*","x","x","+"],["+","x","x","*","x","x"],["+","x","x","*","x","x","+"]]) or ORPD(matrix,findStar(matrix),[["+","x","x","x","*","+"],["+","*","x","x","x","+"],["+","x","x","*","x","+"],["+","x","*","x","x","+"],["x","x","x","x","*"],["*","x","x","x","x"],["x","x","x","*","x"],["x","*","x","x","x"],["x","x","*","x","x"],["x","x","x","x","*","+"],["+","*","x","x","x","x"],["+","x","x","x","*","x"],["x","x","x","*","x","+"],["+","x","x","x","*","x","+"],["+","x","*","x","x","x"],["x","*","x","x","x","+"],["+","x","*","x","x","x","+"],["x","x","*","x","x","+"],["+","x","x","*","x","x"],["+","x","x","*","x","x","+"]]) or ORPOD(matrix,findStar(matrix),[["+","x","x","x","*","+"],["+","*","x","x","x","+"],["+","x","x","*","x","+"],["+","x","*","x","x","+"],["x","x","x","x","*"],["*","x","x","x","x"],["x","x","x","*","x"],["x","*","x","x","x"],["x","x","*","x","x"],["x","x","x","x","*","+"],["+","*","x","x","x","x"],["+","x","x","x","*","x"],["x","x","x","*","x","+"],["+","x","x","x","*","x","+"],["+","x","*","x","x","x"],["x","*","x","x","x","+"],["+","x","*","x","x","x","+"],["x","x","*","x","x","+"],["+","x","x","*","x","x"],["+","x","x","*","x","x","+"]]):
				return True
		x=0
		if validH3(matrix) or validH2(matrix):
			x+=1
		if validV3(matrix) or validV2(matrix):
			x+=1
		if validD3(matrix) or validD2(matrix):
			x+=1
		if validOD3(matrix) or validOD2(matrix):
			x+=1
		if x>=2:
			return True
		else:
			return False
	else:
		x=0
		if findXH(matrix)==2 and validH2(matrix):
			x+=1
		if findXV(matrix)==2 and validV2(matrix):
			x+=1
		if findXD(matrix)==2 and validD2(matrix):
			x+=1
		if findXOD(matrix)==2 and validOD2(matrix):
			x+=1
		if x>=2 :
			return True
		else:
			return False
#matrix=[["x"," ","x"," ","x","+","+"],[" ","x","x","x"," "," "," "],["+","x","*","x","x"," ","+"],[" ","x","x","x"," "," "," "],["+"," ","+","+","+"," "," "]]
#print(checkPOD(matrix,findStar(matrix),["x","x","*","x"]))
#file=open("mem.txt","rb")
#mem=pickle.load(file)
#file.close()
#matrix=mem[-2]
#printMatrix(matrix)
#print(valid(matrix))
#clearIso(matrix)
#printMatrix(matrix)
#input()
def clear():
	file=open("mem.txt","rb")
	mem=pickle.load(file)
	file.close()
	for i in range(len(mem)):
		#printMatrix(mem[i])
		clearIso(mem[i])
		if not isXH(mem[i]):
			clearH(mem[i])
		if not isXV(mem[i]):
			clearV(mem[i])
		if not isXD(mem[i]):
			clearD(mem[i])
		if not isXOD(mem[i]):
			clearOD(mem[i])
		mem[i]=fit(mem[i])
		#printMatrix(mem[i])
		#print("X Y",len(mem[i][0]),len(mem[i]))
		#print

	n=len(mem)
	for i in range(n):
		if i>=n:
			break
			#continue
		j=i+1
		while True:
			if j>=n:
				break
			if i!=j and mem[i]==mem[j]:
				del mem[j]
				n-=1
			else:
				j+=1
	n=len(mem)
	i=0
	while i<n:
		if not valid(mem[i]):
			#printMatrix(mem[i])
			#print("")
			del mem[i]
			n-=1
		else:
			#printMatrix(mem[i])
			#print("")
			i+=1
				#pass
	#for i in mem:
		#printMatrix(i)
		#print("")
	file=open("mem.txt","wb")
	pickle.dump(mem,file)
	file.close()

	
#clear()