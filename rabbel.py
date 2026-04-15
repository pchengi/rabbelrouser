#!/usr/bin/python
import copy
import argparse
import os
import sys

mystrlist=[]
constraintlist=[]

def coordstochars(coordlist):
    charlist=[]
    coordct=0
    for coords in coordlist:
        coordct+=1
        row=coords[0]
        col=coords[1]
        chr=mystrlist[row][col]
        charlist.append(chr)
    return charlist

def checkfile(myfile):
    if debug:
        print("received %s to be checked."%myfile)
    try:
        if not os.path.getsize(myfile):
            print("file %s is empty"%myfile)
            sys.exit(-1)
    except OSError:
        print("file %s not found"%myfile)
        sys.exit(-1)
    return 0
def blah(elements,coords,traversed):
    firsttrav=traversed[:1][0]
    lasttrav=traversed[-1:][0]
    row=firsttrav[0]
    col=firsttrav[1]
    try:
        if constraintlist[row][col] == 'S':
            return
    except:
        pass
    row=lasttrav[0]
    col=lasttrav[1]
    try:
        if constraintlist[row][col] == 'D':
            return
    except:
        pass
    lent=len(traversed)
    charlist=coordstochars(traversed)
    if lent>1:
        comb=''
        for ch in charlist:
            comb+=ch
        if comb in avoidstarts:
            rejects.append(comb)
            return
    if lent>2:
        vowelcount=0
        last,last2,last3=charlist[-3:]
        rej=''
        for val in last,last2,last3:
            rej+=val
            if val in vowels:
                vowelcount+=1
        if vowelcount>2:
            rejects.append(rej)
            return
        rej=''
        if last == last2 == last3:
            rej+=last
            rej+=last2
            rej+=last3
            rejects.append(rej)
            return
        if lent >=minchainlen:
            yield traversed
    for neighbor in elements[coords]:
        newtraversed=copy.deepcopy(traversed)
        if neighbor not in newtraversed:
            if len(newtraversed) <maxchainlen:
                newtraversed.append(neighbor)
                for result in blah(elements,neighbor,newtraversed):
                    yield result
            else:
                return
aparser=argparse.ArgumentParser()
aparser.add_argument('--input','-i',type=str,default=None,required=True)
aparser.add_argument('--constraints','-c',type = str, default = None)
aparser.add_argument('--max-length','-M', type = int, default = 0, required = True)
aparser.add_argument('--min-length','-m', type = int, default = 3)
aparser.add_argument('-d', '--debug', default=False,action='store_true')
args=aparser.parse_args()
inpfile=args.input
debug=args.debug
avoidstarts=[]
constraints=args.constraints
maxchainlen = args.max_length
minchainlen = args.min_length
checkfile(inpfile)
with open(inpfile) as inp:
    lines=inp.readlines()
maxrows=0
maxcols=0
for line in lines:
    maxrows+=1
    l=line.split('\n')[0]
    mychars=l.split(',')
    if maxcols == 0:
        maxcols=len(mychars)
    mystrlist.append(mychars)
if debug:
    print("Finished reading input file")
    print(maxrows,maxcols)
with open('avoidstarts','r') as inp:
    lines=inp.readlines()
for line in lines:
    word=line.split('\n')[0]
    if not word in avoidstarts:
        avoidstarts.append(word)

if not constraints is None:
    if debug:
        print('checking constraints file')
    checkfile(constraints)
    with open(constraints) as inp:
        lines=inp.readlines()
    rows=0
    cols=0
    validchars=['N','D','S']
    for line in lines:
        rows+=1
        l=line.split('\n')[0]
        mychars=l.split(',')
        if len(mychars) != maxcols:
            print("Column count mismatch in provided constraints file %s"%constraints)
            sys.exit(-1)
        if debug:
            print(mychars)
        for testval in mychars:
            if not testval in validchars:
                print("Invalid character %s found in provided constraints file %s"%(testval,constraints))
                sys.exit(-1)
        constraintlist.append(mychars)
    if rows != maxrows:
        print(rows)
        print("Row count mismatch in provided constraints file %s"%constraints)
        sys.exit(-1)

vowels=['A','E','I','O','U','Ä','Ö','Å']
elements={}
for row in range(0,maxrows):
    for col in range(0,maxcols):
        elements[(row,col)]=[]
        if row+1<maxrows:
            elements[(row,col)].append((row+1,col))
        if row+1<maxrows and col+1<maxcols:
            elements[(row,col)].append((row+1,col+1))
        if row+1<maxrows and col-1>=0:
            elements[(row,col)].append((row+1,col-1))
        if row-1>=0:
            elements[(row,col)].append((row-1,col))
        if row-1>=0 and col-1>=0:
            elements[(row,col)].append((row-1,col-1))
        if row-1>=0 and col+1<maxcols:
            elements[(row,col)].append((row-1,col+1))
        if col+1<maxcols :
            elements[(row,col)].append((row,col+1))
        if col-1>=0 :
            elements[(row,col)].append((row,col-1))
seen=set()
rejects=[]    
for row in range(0,maxrows):
    for col in range(0,maxcols):
        traversed=[]
        traversed.append((row,col))
        for results in blah(elements,(row,col),traversed):
            charlist=coordstochars(results)
            assembled=''
            for ch in charlist:
                assembled+=ch
            if assembled not in seen:
                print(assembled)
                seen.add(assembled)
            #if not assembled in allresults:
            #    allresults.append(assembled)

#for result in allresults:
#    print(result)
if debug:
    print("num rejects=%d"%(len(rejects)))
