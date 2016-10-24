import pickle
file=open("mem.txt","rb")
mem=pickle.load(file)
file.close()
for matrix in mem:
	for i in matrix:
		for j in i:
			print(j,end="")
		print("")
	print("")
	
input()