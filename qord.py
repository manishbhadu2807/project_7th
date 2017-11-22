import os
os.chdir("/home/manish/project/JHWNL_1_2")
os.system("java -cp JHWNL.jar:.  Examples")
os.chdir("/home/manish/project")
file=open("correctd.txt","r")
query=file.read( )
query=query.partition('[')[-1].rpartition(']')[0]
print(query.split(", "))
