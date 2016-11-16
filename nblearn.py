import sys
import os
import re
import math

vocabulary=[]
def getFileName(folderName, rootDir):
    fileName = []
    spamFile=[]
    for root, dirs, files in os.walk(rootDir):
        r= root.split('/')
        if (r[len(r) - 1] == folderName):
            #print (r)
            for fN in files:
                if fN.endswith((".txt")):
                    fileName.append(os.path.join(root, fN))
    return fileName


def get_dict(fl,d):
    vocabulary=[]
    for file_path in fl:
        words = open(file_path, "r",encoding="latin1").read()
        #words = re.sub('[^a-zA-Z]', ' ', words).lower()
        for word in words.split():
            if word not in d:
                d[word]= 1
            else:
                d[word] = d.get(word)+1
    return d

def updatedCombined(dict1,dict2):
    for wordsdict1 in dict1.keys():
        if wordsdict1 not in dict2.keys():
            #print("nothing in common came across")
            dict2[wordsdict1]=0
    return dict2


def calculateProb(dictionary,distinctword,totalword):
    finalProbDict={}
    probTotalSpam= totalword + distinctword
    for dict in dictionary:
        numer=dictionary.get(dict) + 1
        probWord= math.log(numer) - math.log(probTotalSpam)
        finalProbDict[dict]=probWord
    return finalProbDict

def createModelFile(ph,h,t,p,count):
    out.write(str(ph) + " " + str(t) +" " + str(count) + "\n")
    for key, elem in p.items():
        out.write(str(h)+ " " + key + " " + str(elem) + "\n")

#Main Execution
out = open("nbmodel.txt", "w")
fileName = sys.argv[1]
spamFile = getFileName("spam", fileName)
totalSpamFile= len(spamFile)
hamFile = getFileName("ham", fileName)
totalHamFile= len(hamFile)
totalFilesOverall= totalHamFile + totalSpamFile
probabilitySpam= totalSpamFile / totalFilesOverall # probability of spam
probabilityham = totalHamFile / totalFilesOverall # probability of ham

spamdict={}
spamdict=get_dict(spamFile,spamdict)
hamdict={}
hamdict=get_dict(hamFile, hamdict)
finalham= updatedCombined(spamdict,hamdict)
uniquekeyham= len(finalham)
totalHamValue = sum(finalham.values())
finalspam= updatedCombined(hamdict,spamdict)
uniquekeyspam= len(finalspam)
totalSpamValue= sum(finalspam.values())
probSpam= calculateProb(finalspam,uniquekeyspam,totalSpamValue)   # dict with spam file's word probability calculated
probham= calculateProb(finalham,uniquekeyham,totalHamValue) # dict with ham file's word probability calculated
createModelFile("HamProbability","Ham",probabilityham, probham,uniquekeyham)
createModelFile("SpamProbability","Spam", probabilitySpam,probSpam,uniquekeyspam)
