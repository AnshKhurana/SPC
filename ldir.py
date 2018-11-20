from os import listdir,walk
from os.path import isfile,join
def getsubs(mypath):
    # mypath='/home/aman/Desktop/machine-learning-ex8'
    flist=[]
    # onlyfiles=[f for f in listdir(walk('/home/aman/Desktop/SPC')) if\
    #                               isfile(join(mypath,f))]
    # print(walk(mypath))
    for fname in walk(mypath):
        # print(fname)
        flist.extend([join(fname[0],f) for f in listdir(fname[0])])

        # print(fname[0])
        # x=2
    return flist
    # print(len(flist)==len(set(flist)))
