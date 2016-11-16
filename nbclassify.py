import sys
import os
import re
import math

array=[]
Spamdict={}
Hamdict={}
hamProb=[]
spamProb=[]
out= open("nboutput.txt", "w")

with open('nbmodel.txt' ,"r") as fil:
    for f in fil:
        if "HamProbability" in f:
            val=f.strip().split(' ')
            hamProb=val[1]

        elif "SpamProbability" in f:
            val1=f.strip().split(' ')
            spamProb=val1[1]
        else:
            val2=f.strip().split(' ')
            if (val2[0] == "Spam"):
                Spamdict[val2[1]]=val2[2]
            elif (val2[0] == "Ham"):
                Hamdict[val2[1]]=val2[2]
def check(files):
    for f in files:
        words= open(f,"r",encoding="latin1").read()
        ham_prio=0
        spam_prio=0
        for word in words.split():
            if word in Hamdict.keys():
                wordHamP=(float(Hamdict.get(word)))
                ham_prio += wordHamP
            if word in Spamdict.keys():
                wordSpamP= (float(Spamdict.get(word)))
                spam_prio += wordSpamP
        finalHam = ham_prio + math.log(float(hamProb))
        finalSpam = spam_prio + math.log(float(spamProb))
        if finalHam > finalSpam:
            out.write("ham " + f + "\n")
        else:
            out.write("spam " + f + "\n")

def getFiles(path):
    fileName = []
    for root, dirs, files in os.walk(path):
        for fN in files:
            if fN.endswith((".txt")):
                fileName.append(os.path.join(root, fN))
    return fileName


fileName = sys.argv[1]
files=getFiles(fileName)
check(files)
