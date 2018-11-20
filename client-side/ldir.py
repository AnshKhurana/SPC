from os import listdir,walk
from os.path import isfile,join
mypath='/home/aman/Desktop/c++_progs'
flist=[]
# onlyfiles=[f for f in listdir(walk('/home/aman/Desktop/SPC')) if\
#                               isfile(join(mypath,f))]
# print(walk(mypath))
for fname in walk(mypath):
    # print(fname)
    flist.extend([join(fname[0],f) for f in listdir(fname[0]) if\
                              isfile(join(fname[0],f))])

    # print(fname[0])
    # x=2
print(flist)