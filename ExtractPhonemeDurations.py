"""
Created on Thu Mar 03 12:17:18 2016

@author: Pooja
"""
import linecache
import numpy
from collections import OrderedDict

f = open('G:/Project/speech_database/audio-merge.TextGrid', 'r')
a=[]
k=0
""" Getting phonemes"""
for i,line in enumerate(f):
    flag=0
    for word in line.split():
        if(word == "\"PhonAlign\""):
            j=i+8
            while(1):
                line2=linecache.getline('G:/Project/speech_database/audio-merge.TextGrid',j)
                for word2 in line2.split():
                    if(word2=="xmin"):
                        flag=1
                        break
                    elif(word2=="="): 
                        continue
                    elif(word2=="\""):
                        continue
                    elif(word2=="text"):
                        continue
                    else:
                        a.append(word2)
                if(flag==1):
                    break
                else:
                    j=j+4
    if(flag==1):
        break
f.seek(0)
dict=OrderedDict()
min=[]
max=[]
""" Getting minimum duration of each phoneme"""
for i,line in enumerate(f):
    flag=0
    for word in line.split():
        if(word == "\"PhonAlign\""):
            j=i+6
            while(1):
                line2=linecache.getline('G:/Project/speech_database/audio-merge.TextGrid',j)
                for word2 in line2.split():
                    if(word2=="class"):
                        flag=1
                        break
                    elif(word2=="="): 
                        continue
                    elif(word2=="xmin"):
                        continue
                    else:
                        #word3=word2[1:-1]
                        min.append(word2)
                if(flag==1):
                    break
                else:
                    j=j+4
    if(flag==1):
        break
f.seek(0)
"""Getting max duration of phoneme"""
for i,line in enumerate(f):
    flag=0
    for word in line.split():
        if(word == "\"PhonAlign\""):
            j=i+7
            while(1):
                line2=linecache.getline('G:/Project/speech_database/audio-merge.TextGrid',j)
                for word2 in line2.split():
                    if(word2=="name"):
                        flag=1
                        break
                    elif(word2=="="): 
                        continue
                    elif(word2=="xmax"):
                        continue
                    else:
                        #word3=word2[1:-1]
                        max.append(word2)
                if(flag==1):
                    break
                else:
                    j=j+4
    if(flag==1):
        break
f.seek(0)
l=0
duration=[]
mindur=[]
maxdur=[]
wordvalues=OrderedDict()
duplicates=[]
"""Finding duration of a phoneme"""
for l in range(0,len(max),1):
    duration.append(float(max[l])-float(min[l]))
    l=l+1
k=-1
l=0
"""Just to get the unique word list"""
for l in range(0,len(a),1):
    wordvalues[a[l]]=duration[l]
"""Making a dictionary of words with min amd maxduration values"""
for i in range(0,len(a)):
    if i in duplicates:
        continue
    mindur=duration[i]
    maxdur=duration[i]
    l=i+1
    for l in range(i+1,len(a)):
        if(a[i]==a[l]):
            duplicates.append(l)
            if(duration[l]<mindur):
                mindur=duration[l]
            if(duration[l]>maxdur):
                maxdur=duration[l]
    dict[a[i]]=[mindur,maxdur]
intervals=[]
"""Generating intervals to plot"""
for k,v in dict.items():
    i=v[0]
    single=[]
    single.append(k)
    for i in numpy.arange(v[0],v[1]+0.01,0.1):
        temp=[]
        temp.append(i)
        temp.append(i+0.1)
        temp.append(0)
        single.append(temp)
    intervals.append(single)
i=0
k=0
"""Finding count to get the probabilities"""
for k in range(0,len(a)):
    flag=0
    i=0
    for i in range(0,len(intervals)):
        if(a[k]==intervals[i][0]):
            dur=duration[k]
            j=1
            for j in range(1,len(intervals[i])):
                if(intervals[i][j][0]<=dur<intervals[i][j][1]):
                    intervals[i][j][2]=intervals[i][j][2]+1
                    flag=1
                    break
                j=j+1
            if(flag==1):
                break
maxcount=[]
index=[]
start=[]
end=[]
i=0
for i in range(0,len(intervals)):
    j=1
    maxcount.append(intervals[i][j][2])
    index.append(1)
    for j in range(1,len(intervals[i])):
        if(intervals[i][j][2]>maxcount[i]):
            maxcount[i]=intervals[i][j][2]
            index[i]=j
finaldur=[]
i=0
for i in range(0,len(intervals)):
    finaldur.append((intervals[i][index[i]][0]+intervals[i][index[i]][1])/2)
totalset=[]
for i in range(0,len(intervals)):
    phoneme=intervals[i][0]
    phonemeset=[]
    phonemeset.append(phoneme)
    for j in range(0,len(a)):
        startend=[]
        if(phoneme==a[j]):
            startend.append(min[j])
            startend.append(max[j])
            startend.append(duration[j]/finaldur[i])
            phonemeset.append(startend)
    totalset.append(phonemeset)
print totalset
    
            
            
                
                    
            