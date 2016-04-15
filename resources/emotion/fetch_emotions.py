#!/usr/bin/python
#coding:utf-8
import json
#import csv
import codecs
classPath="/Users/sx/Desktop/CSCI544/FinalProject/code/emotion/class_qiuyangye.txt"
classFile=open(classPath,'r')
class_list=[]
for line in classFile:
	class_list.append(line)
classFile.close()	
path="/Users/sx/Desktop/CSCI544/FinalProject/Weibo/emotions.json"
with open(path) as data_file:
	emotions=json.load(data_file)
outfile=codecs.open('emotions_qiuyangye.csv', 'w+', 'utf-8')
#csvwriter=csv.writer(outfile, delimiter=',')
outfile.write('value'+','+'category'+','+'icon'+','+'class')	
outfile.write('\n')
rows=1
for em in emotions:
	phrase=em['phrase']
	category=em['category']
	icon=em['icon']
	#print phrase[1:-1], ": ", category
	outfile.write(phrase[1:-1]+',')
	outfile.write(category+',')
	outfile.write(icon)
	if rows>=400:
		outfile.write(','+class_list[rows-400])	
	else:
		outfile.write('\n')
	rows=rows+1
data_file.close()
outfile.close()

